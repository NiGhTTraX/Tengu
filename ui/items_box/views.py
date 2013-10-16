from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.core.cache import cache

from inv.models import MarketGroup, Item
from ui.items_box.utils import getCPUandPGandSlot

from inv.const import CATEGORIES_ITEMS

import json
import hashlib


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

