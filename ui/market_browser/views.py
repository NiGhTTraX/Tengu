from django.core.cache import cache
from django.shortcuts import render, render_to_response
from inv.models import MarketGroup, Item
import json
from inv.const import MARKET_GROUPS_ITEMS, MARKET_GROUPS_SHIPS


GROUP = 0
ITEM = 1
INCREASE_INDENT = 2
DECREASE_INDENT = 3

def getMarketBrowser(request):
  # Build the market tree for items and ships respectively.
  itemsTree = __buildMarketTreeForGroups(MARKET_GROUPS_ITEMS)
  shipsTree = __buildMarketTreeForGroups(MARKET_GROUPS_SHIPS, True)

  constants = {
      "INCREASE_INDENT": INCREASE_INDENT,
      "DECREASE_INDENT": DECREASE_INDENT,
      "ITEM": ITEM,
      "GROUP": GROUP
  }

  return render(request, "market_browser.html", locals())


def __buildMarketTreeForGroups(groups, includeItems=False):
  # Get all the MarketGroup instances in one query.
  marketGroups = MarketGroup.objects.filter(
      marketGroupID__in=groups).order_by("marketGroupName")

  tree = []

  # Construct the market tree by extending it
  # with the tree for each group.
  for group in marketGroups:
    tree.extend(__buildMarketTree(group, includeItems))

  return tree


def __buildMarketTree(marketGroup, includeItems, level = 0):
  if marketGroup is None:
    return []

  subgroups = MarketGroup.objects.filter(
      parentGroupID = marketGroup).order_by("marketGroupName")

  # Add the group it
  result = [(GROUP, level, marketGroup, bool(subgroups) or includeItems)]

  if not subgroups:
    if includeItems:
      items = Item.objects.filter(marketGroupID = marketGroup, published = True)

      # Increase the level of indentation, add the items, and then decrease the
      # level of indentation.
      result.append((INCREASE_INDENT, level + 1, marketGroup.pk))
      result.extend([(ITEM, level + 1, item) for item in items])
      result.append((DECREASE_INDENT, 0, 0))

    return result

  # Increase the level of indentation, add the subtree, and then decrease the
  # level of indentation.
  result.append((INCREASE_INDENT, level + 1, marketGroup.pk))
  for group in subgroups:
    result.extend(__buildMarketTree(group, includeItems, level + 1))
  result.append((DECREASE_INDENT, 0, 0))

  return result

