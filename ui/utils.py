# Utility functions
from django.core.cache import cache

from inv.models import MarketGroup, Item
from dogma.models import TypeAttributes

from dogma.const import *


class MarketTree(object):
  GROUP = 0  # object is a MarketGroup instance.
  ITEM = 1  # object is an Item instance.
  INCREASE_INDENT = 2
  DECREASE_INDENT = 3

  def __init__(self, marketGroup, includeItems = False):
    """
    Args:
      marketGroup: MarketGroup instance.
      includeItems: Whether to just return groups, or include items as well.
    """
    self.marketGroup = marketGroup
    self.includeItems = includeItems

  def build(self):
    """Return a serialized tree of the market groups.

    Returns:
      A list of tuples in the form (type, level, object, isLeaf).
    """
    return self.__build(self.marketGroup, self.includeItems)

  def __build(self, marketGroup, includeItems, level = 0):
    if marketGroup is None:
      return []

    subgroups = MarketGroup.objects.filter(
        parentGroupID = marketGroup).order_by("marketGroupName")

    # Add the group itself.
    result = [(self.GROUP, level, marketGroup, bool(subgroups) or includeItems)]

    if not subgroups:
      if includeItems:
        items = Item.objects.filter(marketGroupID = marketGroup, published = True)

        # Increase the level of indentation, add the items, and then decrease the
        # level of indentation.
        result.append((self.INCREASE_INDENT, level + 1, marketGroup.pk))
        result.extend([(self.ITEM, level + 1, item) for item in items])
        result.append((self.DECREASE_INDENT, 0, 0))

      return result

    # Increase the level of indentation, add the subtree, and then decrease the
    # level of indentation.
    result.append((self.INCREASE_INDENT, level + 1, marketGroup.pk))
    for group in subgroups:
      result.extend(self.__build(group, includeItems, level + 1))
    result.append((self.DECREASE_INDENT, 0, 0))

    return result


def getCPUandPG(itemsIter):
  """Returns a list of (item, cpu, pg) tuples.

  Args:
    itemsIter: An iterable over the items.
  """
  items = []

  for item in itemsIter:
    cpu = pg = None
    try:
      cpu = TypeAttributes.objects.get(typeID=item, attributeID=ATTRIBUTE_CPU)
      pg = TypeAttributes.objects.get(typeID=item, attributeID=ATTRIBUTE_PG)
    except TypeAttributes.DoesNotExist:
      pass

    items.append((item, cpu, pg))

  return items


def getSlots(ship):
  """Get the number of slots for a given ship.

  Returns:
    A dictionary.
  """
  try:
    highSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_HIGHSLOTS).value)
    medSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_MEDSLOTS).value)
    lowSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_LOWSLOTS).value)
  except TypeAttributes.DoesNotExist:
    # This is a T3 ship.
    highSlots = medSlots = lowSlots = 0

  try:
    rigSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_RIGSLOTS).value)
  except TypeAttributes.DoesNotExist:
    rigSlots = 0

  try:
    subSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_SUBSYSTEMS).value)
  except TypeAttributes.DoesNotExist:
    subSlots = 0

  # Get missile and turret slots.
  try:
    missileSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_MISSILESLOTS).value)
  except TypeAttributes.DoesNotExist:
    missileSlots = 0

  try:
    turretSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_TURRETSLOTS).value)
  except TypeAttributes.DoesNotExist:
    turretSlots = 0

  return {
      "highSlots": highSlots,
      "medSlots": medSlots,
      "lowSlots": lowSlots,
      "rigSlots": rigSlots,
      "subSlots": subSlots,
      "turretSlots": turretSlots,
      "missileSlots": missileSlots
  }

