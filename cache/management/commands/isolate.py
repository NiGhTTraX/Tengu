from django.core.management.base import BaseCommand, CommandError

from inv.models import *
from dogma.models import *

import sys
from queue import Queue


class Command(BaseCommand):
  args = "typeID"
  help = "Deletes everything but the given typeID and everything related to it"

  def gatherEffects(self, effects, effectIDs, expressions, attributeIDs):
    for effect in effects:
      effectIDs.add(effect.pk)

      if effect.preExpression:
        expressions.put(effect.preExpression)
      if effect.postExpression:
        expressions.put(effect.postExpression)

      if effect.dischargeAttributeID:
        attributeIDs.add(effect.dischargeAttributeID.pk)
      if effect.falloffAttributeID:
        attributeIDs.add(effect.falloffAttributeID.pk)
      if effect.durationAttributeID:
        attributeIDs.add(effect.durationAttributeID.pk)
      if effect.rangeAttributeID:
        attributeIDs.add(effect.rangeAttributeID.pk)
      if effect.trackingSpeedAttributeID:
        attributeIDs.add(effect.trackingSpeedAttributeID.pk)
      if effect.fittingUsageChanceAttributeID:
        attributeIDs.add(effect.fittingUsageChanceAttributeID.pk)

  def gatherExpressions(self, expressions, expressionIDs, attributeIDs, typeIDs,
                        groupIDs):
    while not expressions.empty():
      e = expressions.get()
      expressionIDs.add(e.pk)

      if e.arg1:
        expressions.put(e.arg1)
      if e.arg2:
        expressions.put(e.arg2)

      if e.expressionAttributeID:
        attributeIDs.add(e.expressionAttributeID.pk)
      """
      if e.expressionGroupID:
        groupIDs.add(e.expressionGroupID.pk)
      if e.expressionTypeID:
        typeIDs.add(e.expressionTypeID.pk)
      """

  def handle(self, *args, **options):
    try:
      typeID = int(args[0])
    except ValueError:
      self.stderr.write("Invalid typeID")
      sys.exit(1)
    except IndexError:
      self.stderr.write("Must provide a typeID")
      sys.exit(1)

    try:
      item = Item.objects.get(pk=typeID)
    except Item.DoesNotExist:
      self.stderr.write("Item %d does not exist" % typeID)
      sys.exit(1)


    marketGroupIDs = []
    mg = item.marketGroupID
    while mg is not None:
      marketGroupIDs.append(mg.pk)
      mg = mg.parentGroupID

    groupIDs = set([item.groupID.pk, 1])
    categoryIDs = set([item.groupID.categoryID.pk, 1])

    typeIDs = set([item.pk, 1373])
    # add the character types
    newTypeIDs = set(typeIDs)

    expressions = Queue()
    expressionIDs = set()
    attributeIDs = set(item.attributes.all().values_list(
        "attributeID", flat=True)) | set([161,162,38,4])
    effectIDs = set()

    while True:
      effects = []
      for typeID in newTypeIDs:
        i = Item.objects.get(pk=typeID)
        effects.extend(i.effects.all())

      self.gatherEffects(effects, effectIDs, expressions, attributeIDs)
      if expressions.empty():
        break

      oldTypeIDs = set(typeIDs)
      self.gatherExpressions(expressions, expressionIDs, attributeIDs, typeIDs,
      groupIDs)
      newTypeIDs = typeIDs - oldTypeIDs
      if not newTypeIDs:
        break

    unitIDs = Attribute.objects.filter(pk__in=attributeIDs).values_list(
        "unitID", flat=True)

    operandIDs = Expression.objects.filter(pk__in=expressionIDs).values_list(
        "operandID", flat=True)

    self.stdout.write("Isolating items...")
    Item.objects.exclude(pk__in=typeIDs).delete()

    self.stdout.write("Isolating market groups...")
    MarketGroup.objects.exclude(pk__in=marketGroupIDs).delete()

    self.stdout.write("Isolating groups...")
    Group.objects.exclude(pk__in=groupIDs).delete()

    self.stdout.write("Isolating categories...")
    Category.objects.exclude(pk__in=categoryIDs).delete()

    self.stdout.write("Isolating attributes...")
    Attribute.objects.exclude(pk__in=attributeIDs).delete()

    self.stdout.write("Isolating expressions...")
    Expression.objects.exclude(pk__in=expressionIDs).delete()

    self.stdout.write("Isolating effects...")
    Effect.objects.exclude(pk__in=effectIDs).delete()

    #self.stdout.write("Isolating units...")
    #Unit.objects.exclude(pk__in=operandIDs).delete()

    self.stdout.write("Isolating operands...")
    Operand.objects.exclude(pk__in=operandIDs).delete()

    self.stdout.write("Finished.")

    self.stdout.write("\n-- Stats --")
    self.stdout.write("Items: %d" % Item.objects.count())
    self.stdout.write("Groups: %d" % Group.objects.count())
    self.stdout.write("MarketGroups: %d" % MarketGroup.objects.count())
    self.stdout.write("Categories: %d" % Category.objects.count())
    self.stdout.write("Effects: %d" % Effect.objects.count())
    self.stdout.write("Attributes: %d" % Attribute.objects.count())
    self.stdout.write("Expressions: %d" % Expression.objects.count())
    self.stdout.write("TypeEffects: %d" % TypeEffects.objects.count())
    self.stdout.write("TypeAttributes: %d" % TypeAttributes.objects.count())
    self.stdout.write("Unit: %d" % Unit.objects.count())
    self.stdout.write("Operand: %d" % Operand.objects.count())

