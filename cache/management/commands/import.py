from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.core.cache import cache
from django.conf import settings

from cache.utils import disableSynchronous
from cache import DjangoDataHandler, DjangoCacheHandler
from eos.data.dataHandler import JsonDataHandler
from eos import Eos

from inv.models import *
from dogma.models import *
from cache.models import *

import json
import sys
import os
from optparse import make_option


TABLES_TO_FILES = {
    "dogma_attribute": "dgmattribs.json",
    "dogma_effect": "dgmeffects.json",
    "dogma_expression": "dgmexpressions.json",
    "dogma_typeattributes": "dgmtypeattribs.json",
    "dogma_typeeffects": "dgmtypeeffects.json",
    "dogma_unit": "dgmunits.json",
    "inv_category": "invcategories.json",
    "inv_group": "invgroups.json",
    "inv_item": "invtypes.json",
    "inv_marketgroup": "marketProxy_GetMarketGroups.json",
    "dogma_operand": "dogma_GetOperandsForChar.json",
    "cache_metadata": "metadata.json"
}

FILES_TO_MODELS = {
    "dgmattribs.json": Attribute,
    "dgmeffects.json": Effect,
    "dgmexpressions.json": Expression,
    "dgmtypeattribs.json": TypeAttributes,
    "dgmtypeeffects.json": TypeEffects,
    "dgmunits.json": Unit,
    "invcategories.json": Category,
    "invgroups.json": Group,
    "invtypes.json": Item,
    "marketProxy_GetMarketGroups.json": MarketGroup,
    "dogma_GetOperandsForChar.json": Operand,
    "metadata.json": Metadata
}

class Command(BaseCommand):
  args = "<tableName tableName ...>"
  help = "Imports Phobos dumps into the database and runs the cache generator"

  option_list = BaseCommand.option_list + (
      make_option("--dumpPath",
          default = os.path.join(os.path.expanduser("~"), "Phobos", "dump"),
          dest = "dumpPath",
          help = "Path to Phobos dump files"),

      make_option("--handler",
          default = "django",
          dest = "dataHandler",
          help = "Data handler to use"),

      make_option("--noImport",
          default = False,
          dest = "noImport",
          help = "Only generate the cache"),

      make_option("--noGenerate",
          default = False,
          dest = "noGenerate",
          help = "Don't generate the cache"),
  )

  def handle(self, *args, **options):
    settings.DEBUG = False  # disable debug mode

    cursor = connection.cursor()
    tables = args

    if not tables:
      tables = TABLES_TO_FILES.keys()  # default, import all the tables.

    with disableSynchronous():  # faster inserts for sqlite3
      if not options["noImport"]:
        for tableName in tables:
          try:
            fileName = TABLES_TO_FILES[tableName]
          except KeyError:
            self.stderr.write("Table %s does not exist" % tableName)
            continue

          self.importTable(os.path.join(options["dumpPath"], fileName), tableName,
          cursor)

      if options["noImport"] and not options["noGenerate"]:
        if options["dataHandler"] == "django":
          dataHandler = DjangoDataHandler()
        elif options["dataHandler"] == "json":
          dataHandler = JsonDataHandler(options["dumpPath"])
        else:
          self.stderr.write("Invalid data handler %s" % options["dataHandler"])
          sys.exit(1)

        self.stdout.write("Clearing the modifiers tables...")
        cursor.execute("DELETE FROM dogma_modifier;")
        cursor.execute("DELETE FROM dogma_effectmodifiers;")

        self.stdout.write("Clearing cache...")
        Metadata.objects.filter(fieldName="fingerprint").delete()
        cache.clear()

        self.stdout.write("Running cache generator...")
        Eos(dataHandler, DjangoCacheHandler(), storagePath="/tmp/")

    self.stdout.write("Finished.")

  def importTable(self, fileName, tableName, cursor):
    """Imports a JSON file into the database.

    This uses raw SQL instead of the Django ORM. You should never do this. But
    because Django is being silly when assigning values to ForeignKey fields, we
    have to do this. The alternative would be to rename the foreign key fields
    in the Phobos dumps to include '_id' at the end. That's just bollocks.

    Args:
      fileName: The name of the JSON file to be loaded. The data should be in the
      form of a a list of dictionaries, where each dictionary maintains the order
      of the keys.

      tableName: The name of the table the data should be imported into.

      cursor: database cursor instance.
    """
    if cursor is None:
      return

    with open(fileName, "r") as fin:
      try:
        data = json.loads(fin.read())
      except ValueError:
        self.stderr.write("Error decoding file %s" % fileName)
        sys.exit()

      self.stdout.write("Importing %s(%d) into %s" % (fileName, len(data), tableName))

      names = ",".join(data[0].keys())  # column names
      placeholder = ",".join(["?"] * len(data[0].keys()))  # placeholder used to
                                                           # replace with values
      values = []

      for row in data:
        if len(row.values()) != len(data[0].keys()):
          self.stderr.write("Something is wrong with %s", row)
          sys.exit()

        values.append(tuple(row.values()))

      try:
        # Truncate the table first.
        cursor.execute("DELETE FROM %s" % tableName)

        # Now do a bulk insert.
        cursor.executemany("INSERT INTO %s (%s) VALUES (%s)" % (tableName, names, placeholder),
            values)
      except sqlite3.Error as e:
        self.stderr.write("Error importing into %s", tableName)
        self.stderr.write(e.message)
        sys.exit()

