# Utility functions
from inv.models import MarketGroup, Item
from dogma.models import TypeAttributes

from dogma.const import *


def buildMarketTree(marketGroup = None, includeItems = False, level = 0):
  """Return a tree of the market groups.

  Args:
    marketGroup: MarketGroup instance or integer.
    includeItems: Whether to just return groups, or include items as well.
    level: Level of indentation.

  Returns:
    A list of tuples.
  """
  if marketGroup is None:
    return []

  subgroups = MarketGroup.objects.filter(parentGroupID =
      marketGroup).order_by("marketGroupName")

  result = [(0, level, marketGroup, bool(subgroups) or includeItems)]

  if not subgroups:
    if includeItems:
      items = Item.objects.filter(marketGroupID = marketGroup, published = True)
      result.append((1, level + 1, marketGroup.marketGroupID))
      result.extend([(2, level + 1, item) for item in items])
      result.append((-1, 0, 0))
    return result

  result.append((1, level + 1, marketGroup.marketGroupID))
  for group in subgroups:
    result.extend(buildMarketTree(group, includeItems, level + 1))
  result.append((-1, 0, 0))

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
    turretSlots = int(TypeAttributes.objects.get(typeID=ship,
        attributeID=ATTRIBUTE_TURRETSLOTS).value)
  except TypeAttributes.DoesNotExist:
    # This is a T3 ship.
    missileSlots = turretSlots = 0

  return {
      "highSlots": highSlots,
      "medSlots": medSlots,
      "lowSlots": lowSlots,
      "rigSlots": rigSlots,
      "subSlots": subSlots,
      "turretSlots": turretSlots,
      "missileSlots": missileSlots
  }

