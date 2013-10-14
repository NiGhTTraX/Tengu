from django.core.cache import cache

from inv.models import MarketGroup, Item

import json


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


def getExpandedGroups(request):
  # Now get which ones should be expanded.
  expandedGroups = []
  if "expandedMarketGroups" in request.COOKIES:
    cookie = json.loads(request.COOKIES["expandedMarketGroups"])
    expandedGroups = [int(x) for x in cookie]

  return expandedGroups

