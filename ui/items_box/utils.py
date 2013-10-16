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

