from inv.models import Item
from dogma.models import TypeAttributes
from dogma.const import *


def getCPUandPGandSlot(itemsIter):
  """Adds extra information to the given list of items.

  Returns:
    A list of tuples in the form (item, cpu, pg, classes).

    - cpu and pg are the unbonused values of the CPU and PG attributes for that
    item.

    - classes is space delimited list of CSS classes representing the slot and
    hardpoint type of the item.

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

    classes = []
    if item.slot == Item.HIGH:
      classes.append("high")
    if item.slot == Item.MED:
      classes.append("med")
    if item.slot == Item.LOW:
      classes.append("low")
    if item.slot == Item.RIG:
      classes.append("rig")
    if item.slot == Item.SUB:
      classes.append("sub")
    if item.hardpoint == Item.MISSILE:
      classes.append("missile")
    if item.hardpoint == Item.TURRET:
      classes.append("turret")

    items.append((item, cpu, pg, " ".join(classes)))

  return items

