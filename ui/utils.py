# Utility functions
from inv.models import MarketGroup, Item


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

