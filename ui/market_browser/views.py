from django.core.cache import cache
from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse
from inv.models import MarketGroup, Item
import json
import hashlib
from inv.const import MARKET_GROUPS_ITEMS, MARKET_GROUPS_SHIPS
from inv.const import CATEGORIES_ITEMS
from dogma.models import TypeAttributes
from dogma.const import *


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


def getItems(request, marketGroupID):
  """Retreives items from a market group.

  First, check whether the list is in cache, returning it directly if it is.
  Otherwise, retrieve the items from the database and then store them in cache.
  """
  if not request.is_ajax():
    raise Http404

  try:
    marketGroupID = int(marketGroupID)
  except ValueError:
    raise Http404

  items = cache.get("items_%d" % marketGroupID)

  if items is None:
    # List wasn't in cache, let's get it from the database.
    try:
      marketGroup = MarketGroup.objects.get(pk=marketGroupID)
    except MarketGroup.DoesNotExist:
      raise Http404

    itemQuery = Item.objects.filter(marketGroupID = marketGroup,
                                    published=True).order_by("typeName")
    # Augment with CPU, PG and slot info.
    items = getCPUandPGandSlot(itemQuery)

    # Store the list in cache.
    cache.set("items_%d" % marketGroupID, items)

  return render_to_response("items.html", locals())


def searchItems(request, keywords):
  """Searches for items by name.

  First, check whether the list is in cache, returning it directly if it is.
  Otherwise, retrieve the items from the database and then store them in cache.

  You have to check if the items belong to a valid market group i.e. the ones
  being displayed in the market tree. To do this, you have to check the
  categoryID, which is a foreign key. Thus, we use categoryID_id to save a
  query. This column, while normally not in the invTypes table, is set by Eos
  during cache generation.
  """
  if not request.is_ajax():
    raise Http404

  hashValue = hashlib.md5(keywords.encode()).hexdigest()
  items = cache.get("search_%s" % hashValue)

  if items is None:
    # List wasn't in cache, let's fetch it from the database.
    itemQuery = Item.objects.filter(typeName__icontains=keywords, published=True,
        categoryID_id__in=CATEGORIES_ITEMS)

    # Augment with CPU, PG and slot info.
    items = getCPUandPGandSlot(itemQuery)

    # Now store it in cache.
    cache.set("search_%s" % hashValue, items)

  return render_to_response("items.html", locals())


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

