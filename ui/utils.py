# Utility functions
from inv.models import MarketGroup, Item

def buildMarketTree(marketGroup = None, level = 0):
  """Return a tree of the market groups."""
  if marketGroup is None:
    return []

  subgroups = MarketGroup.objects.filter(parentGroupID =
      marketGroup).order_by("marketGroupName")

  result = [(0, level, marketGroup, bool(subgroups))]

  if not subgroups:
    return result

  result.append((1, level + 1, marketGroup.marketGroupID))
  for group in subgroups:
    result.extend(buildMarketTree(group, level + 1))
  result.append((-1, 0, 0))

  return result

