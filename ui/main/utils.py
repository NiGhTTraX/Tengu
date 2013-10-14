# Utility functions
from django.core.cache import cache

from inv.models import MarketGroup, Item
from dogma.models import TypeAttributes

from dogma.const import *


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

