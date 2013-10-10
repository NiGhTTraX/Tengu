"""Data and cache handler tests.

These tests load fixtures with a small subset of _real_ data. The database will
only contain the Raven type, with all of its associated attributes, effects and
modifiers. Nothing more. This makes it easy to test against real data, without
having to manually insert it at the beginning of the tests.

Since the cache generation process is deterministic and returns the same data
every time, it makes sense to only load the fixtures once and initialize the Eos
engine at the beginning of this module. Doing this will result in greatly
improved performance.

Django wraps tests in a transaction and then rolls it back, so the database is
not modified between tests. This way we're guaranteed that each test will use
the untouched data created by Eos at the beginning.
"""

from django.test import TestCase
from django.core.cache import cache
from django.core.management import call_command

from inv.models import *
from dogma.models import *
from cache.models import *

from cache import DjangoDataHandler, DjangoCacheHandler
from cache.utils import disableSynchronous

from eos import Eos
from eos.data.cache.handler.exception import TypeFetchError, AttributeFetchError, EffectFetchError, ModifierFetchError


class TestItem(object):
  """Use this class to test the cache generator."""
  typeID = 12274
  attributes = [4, 9, 30, 50, 182, 204, 213, 277, 422, 633, 161, 162, 38]
  effects = [11, 16, 763, 889]
  modifiers = [1, 2]
  effectWithModifiers = 889
  modifiersForEffect = [1]


class TestCharacter(object):
  """Use this class to test for the creation of new effects that are attached to
  a character."""
  typeID = 1373
  attributes = [4, 212, 161, 162, 38]
  effects = [890]
  modifiers = [3, 4, 5, 6]
  effectWithModifiers = 890
  modifiersForEffect = [3,4,5,6]


DATA_HANDLER = None
CACHE_HANDLER = None
EOS = None


def setUpModule():
  # If using sqlite3, disable the synchronous mode for faster performance.
  disableSynchronous.disable()

  # Load fixtures.
  call_command("loaddata", "dogma.json", verbosity=0)
  call_command("loaddata", "inv.json", verbosity=0)
  call_command("loaddata", "metadata.json", verbosity=0)

  # Set up Eos.
  global DATA_HANDLER, CACHE_HANDLER, EOS
  DATA_HANDLER = DjangoDataHandler()
  CACHE_HANDLER = DjangoCacheHandler(verbose=False)
  EOS = Eos(dataHandler=DATA_HANDLER, cacheHandler=CACHE_HANDLER,
      storagePath="/tmp/")


class TestNumQueries(TestCase):

  def setUp(self):
    self.cacheHandler = CACHE_HANDLER

    # Clear the cache before every test.
    cache.clear()

  def test_cache_generator(self):
    """Test the number of queries executed during cache generation."""
    # Clear the tables.
    Modifier.objects.all().delete()
    Effect.objects.all().delete()
    Item.objects.all().delete()
    Metadata.objects.filter(fieldName="fingerprint").delete()

    # Load the fixtures again.
    call_command("loaddata", "dogma.json", verbosity=0)
    call_command("loaddata", "inv.json", verbosity=0)

    expectedNumQueries = 2 + \
                         7 + \
                         1 + \
                         0 + \
                         1 + \
                         len(TestItem.effects) + len(TestCharacter.effects)+ \
                         1 + \
                         8 + \
                         1

    with self.assertNumQueries(expectedNumQueries):
      """
      Cache generation will execute lots of queries as follows:

      First, the data version is checked with the cache fingerprint. This will
      result in 2 queries, 1 for each.

      Since there is no fingerprint, cache generation will commence. The next
      step is to fetch all the necessary data. Only 1 query should be executed
      for each table, in a total of 7 queries corresponding to the 7 tables.

      Next, while the cache generator processes the data, no extra queries
      should be performed to fetch parts of the objects.

      The last step is updating the cache itself. Here is where the majority of
      queries will be executed, as follows:

      updateModifiers():
      - 1 bulk insert to create all the modifiers.

      updateAttributes():
      - 0 queries performed for attributes.

      updateEffects():
      - 1 query to retrieve existing effects.
      - effectCount queries to update info for all effects, 1 for each.
      - 1 bulk query to update the modifiers of all effects, 1 for each.

      updateItems():
      - 1 query to get the items.
      - 1 query to get the effects of all the items.
      - 1 query to get the attributes of all the items.
      - 2 queries to update the items, 1 for each item.
      - 1 bulk query to add new effects.
      - 1 bulk query to add new attributes.


      There's 1 final query to update the fingerprint.
      """
      EOS = Eos(dataHandler=DATA_HANDLER, cacheHandler=CACHE_HANDLER,
          storagePath="/tmp/")

  def test_one_item(self):
    expectedNumQueries = 1 + \
                         1 + \
                         len(TestItem.effects) + \
                         len(TestItem.effects) + \
                         len(TestItem.modifiers) + \
                         1
    with self.assertNumQueries(expectedNumQueries):
      """
      Since nothing is in the cache yet, data has to be retrieved from the
      database. This will issue a whole lot of queries as follows:

      - 1 query to retrieve the item itself.
      - 1 query to retrieve its list of effects.
      - effectCount queries to retrieve the effects themselves.
      - effectCount queries to retrieve the list of modifiers, 1 for each effect.
      - modifierCount queries to retrieve the modifiers themselves.
      - 1 query to retrieve the item's attributes.
      """
      self.cacheHandler.getType(TestItem.typeID)

    # Since the data is now in cache, no more queries will be issued.
    with self.assertNumQueries(0):
      self.cacheHandler.getType(TestItem.typeID)

  def test_one_effect(self):
    expectedNumQueries = 2 + len(TestItem.modifiersForEffect)
    with self.assertNumQueries(expectedNumQueries):
      """
      Since nothing is in the cache yet, data has to be retrieved from the
      database. This will issue a few queries as follows:

      - 1 query to retrieve the effect itself.
      - 1 query to retrieve the list of modifiers.
      - modifierCount queries to retrieve the modifiers themselves.
      """
      self.cacheHandler.getEffect(TestItem.effectWithModifiers)

    # Since the data is now in cache, no more queries will be issued.
    with self.assertNumQueries(0):
      self.cacheHandler.getEffect(TestItem.effectWithModifiers)

  def test_one_modifier(self):
    with self.assertNumQueries(1):
      # Since the cache is empty, this will issue one query to get the modifier
      # from the database.
      self.cacheHandler.getModifier(TestItem.modifiers[0])

    # Since the data is now in cache, no more queries will be issued.
    with self.assertNumQueries(0):
      self.cacheHandler.getModifier(TestItem.modifiers[0])

  def test_one_attribute(self):
    with self.assertNumQueries(1):
      # Since the cache is empty, this will issue one query to get the attribute
      # from the database.
      self.cacheHandler.getAttribute(TestItem.attributes[0])

    # Since the data is now in cache, no more queries will be issued.
    with self.assertNumQueries(0):
      self.cacheHandler.getAttribute(TestItem.attributes[0])

  def test_fingerprint(self):
    with self.assertNumQueries(1):
      # Since the cache is empty, this will issue one query to get the
      # fingerprint from the database.
      self.cacheHandler.getFingerprint()

    # Since the data is now in cache, no more queries will be issued.
    with self.assertNumQueries(0):
      self.cacheHandler.getFingerprint()

  def test_one_item_which_expires(self):
    self.cacheHandler.getType(TestItem.typeID)

    # Invalidate the item cache.
    cache.delete("type_%d" % TestItem.typeID)

    with self.assertNumQueries(3):
      """
      Since the item expired, we have to hit the database again to retrieve it.
      This will result in a few queries as follows:

      - 1 query to get the item.
      - 1 query to get the list of effects.
      - 1 query to get the item's attributes.

      Since everything else remained cached, no other queries will be issued.
      """
      self.cacheHandler.getType(TestItem.typeID)

  def test_one_item_with_parts_expiring(self):
    self.cacheHandler.getType(TestItem.typeID)

    # Invalidate parts of the item.
    cache.delete("attribute_%d" % TestItem.attributes[0])
    cache.delete("effect_%d" % TestItem.effects[0])
    cache.delete("modifier_%d" % TestItem.modifiers[0])

    with self.assertNumQueries(0):
      """
      Even though parts of the item have been invalidated, this will result in
      no extra queries.
      """
      self.cacheHandler.getType(TestItem.typeID)

  def test_one_item_which_expires_along_with_parts(self):
    self.cacheHandler.getType(TestItem.typeID)

    # Invalidate parts of the item.
    cache.delete("attribute_%d" % TestItem.attributes[0])
    cache.delete("effect_%d" % TestItem.effectWithModifiers)
    for modifierID in TestItem.modifiersForEffect:
      cache.delete("modifier_%d" % modifierID)

    # And the item itself.
    cache.delete("type_%d" % TestItem.typeID)

    expectedNumQueries = 1 + \
                         1 + \
                         1 + \
                         len(TestItem.modifiersForEffect) + \
                         1

    with self.assertNumQueries(expectedNumQueries):
      """
      The item has expired so it must be retrieved again. Because parts of it
      also expired, this will result in a few queries as follows:

      - 1 query to get the item.
      - 1 query to get the list of effects.
      - effectCount query to get the expired effect.
      - modifierCount query to get the expired modifiers.
      - 1 query to get the item's attributes.
      """
      self.cacheHandler.getType(TestItem.typeID)

  def test_full_cache_clear(self):
    self.cacheHandler.getType(TestItem.typeID)

    # Everything is retrieved from the cache, so no database hits.
    with self.assertNumQueries(0):
      self.cacheHandler.getType(TestItem.typeID)

    # Invalidate cache.
    cache.clear()

    # Cache is empty again, exact number of queries as the first time will be
    # issued.
    expectedNumQueries = 1 + \
                         1 + \
                         len(TestItem.effects) + \
                         len(TestItem.effects) + \
                         len(TestItem.modifiers) + \
                         1
    with self.assertNumQueries(expectedNumQueries):
      self.cacheHandler.getType(TestItem.typeID)


class TestCacheValidity(TestCase):

  def setUp(self):
    self.cacheHandler = CACHE_HANDLER
    self.dataHandler = DATA_HANDLER

    # Clear the cache before every test.
    cache.clear()

  def test_data_version(self):
    self.assertEqual(self.dataHandler.getVersion(), "555149")

    Metadata.objects.all().delete()
    self.assertEqual(self.dataHandler.getVersion(), None)

  def test_item(self):
    # Check that the test item exists.
    item = Item.objects.get(pk=TestItem.typeID)

    # Check that it has all the required attributes and effects.
    self.assertQuerysetEqual(item.attributes.values_list("attributeID", flat=True),
                             TestItem.attributes, ordered=False, transform=int)
    self.assertQuerysetEqual(item.effects.values_list("effectID", flat=True),
                             TestItem.effects, ordered=False, transform=int)

    # Check that all modifiers have been created.
    modifiers = EffectModifiers.objects.filter(effectID_id__in=TestItem.effects)
    self.assertQuerysetEqual(modifiers.values_list("modifierID", flat=True),
                             TestItem.modifiers, ordered=False, transform=int)

  def test_character(self):
    # Check that the test character item exists.
    item = Item.objects.get(pk=TestCharacter.typeID)

    # Check that it has all the required attributes and effects.
    self.assertQuerysetEqual(item.attributes.values_list("attributeID", flat=True),
                             TestCharacter.attributes, ordered=False, transform=int)
    self.assertQuerysetEqual(item.effects.values_list("effectID", flat=True),
                             TestCharacter.effects, ordered=False, transform=int)

    # Check that all modifiers have been created.
    modifiers = EffectModifiers.objects.filter(effectID_id__in=TestCharacter.effects)
    self.assertQuerysetEqual(modifiers.values_list("modifierID", flat=True),
                             TestCharacter.modifiers, ordered=False, transform=int)

  def test_invalid_type(self):
    self.assertRaises(TypeFetchError, self.cacheHandler.getType, 0)

  def test_invalid_effect(self):
    self.assertRaises(EffectFetchError, self.cacheHandler.getEffect, 0)

  def test_invalid_attribute(self):
    self.assertRaises(AttributeFetchError, self.cacheHandler.getAttribute, 0)

  def test_invalid_modifier(self):
    self.assertRaises(ModifierFetchError, self.cacheHandler.getModifier, 0)

