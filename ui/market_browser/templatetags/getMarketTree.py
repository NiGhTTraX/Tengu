from django import template
from django.core.cache import cache

from inv.models import MarketGroup
from ui.market_tree.utils import MarketTree

import json


register = template.Library()


@register.inclusion_tag("market_tree.html")
def getMarketTree(marketGroupsToGet, includeItems = False):
  """Gets the market tree structure and status.

  First, check if the tree is in cache. If so, return it directly. Otherwise,
  fetch it from the database and then store it in cache.

  Args:
    request: Django request.
    marketGroupsToGet: A list of integer ids.
    includeItems: Boolean value specifying wether or not to include items under
    leaf nodes.

  Returns:
    A serialized market tree in the form of a list of tuples. See
    ui.utils.MarketTree for more details.
  """
  marketTree = []

  # Get all the MarketGroup instances in one query.
  marketGroups = MarketGroup.objects.filter(marketGroupID__in=marketGroupsToGet).order_by("marketGroupName")

  for group in marketGroups:
    tree = cache.get("marketTree_%d_%d" % (group.pk, int(includeItems)))
    if tree is None:
      tree = MarketTree(group, includeItems).build()
      cache.set("marketTree_%d_%d" % (group.pk, int(includeItems)), tree)

    marketTree.extend(tree)


  return {
      "marketTree": marketTree,
      "constants": {
          "INCREASE_INDENT": MarketTree.INCREASE_INDENT,
          "DECREASE_INDENT": MarketTree.DECREASE_INDENT,
          "GROUP": MarketTree.GROUP,
          "ITEM": MarketTree.ITEM
      }
  }

