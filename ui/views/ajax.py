from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.cache import cache

from dogma.models import TypeAttributes
from inv.models import MarketGroup, Item
from ui.utils import getCPUandPG

from inv.const import CATEGORIES_ITEMS, CATEGORIES_SHIPS

import json



def updateWidgets(request):
  """Updates the stats widgets in the right sidebar.

  This function retrieves the position and status of the stats widget via a GET
  request and stores them in cookies. The contents are dumped in JSON format.
  """
  if not request.is_ajax():
    raise Http404

  if request.method != "POST":
    raise Http404

  if "widgets[]" not in request.POST or "widgetStatuses[]" not in request.POST:
    raise Http404

  widgets = json.dumps(request.POST.getlist("widgets[]"))
  widgetStatuses = json.dumps(request.POST.getlist("widgetStatuses[]"))
  if not widgets or not widgetStatuses:
    raise Http404

  response = HttpResponse("updated")
  response.set_cookie("widgets", widgets, max_age = 30 * 24 * 3600)
  response.set_cookie("widgetStatuses", widgetStatuses,
      max_age = 30 * 24 * 3600)

  return response

def updateMarketTree(request):
  """Updates the market tree expanded groups."""
  if not request.is_ajax():
    raise Http404

  if request.method != "POST":
    raise Http404

  groups = json.dumps(request.POST.getlist("expandedGroups[]"))
  response = HttpResponse("updated")
  response.set_cookie("expandedMarketGroups", groups, max_age = 30 * 24 * 3600)
  return response

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
    # Augment with CPU and PG info.
    items = getCPUandPG(itemQuery)

    # Store the list in cache.
    cache.set("items_%d" % marketGroupID, items)

  return render_to_response("items.html", locals())

def searchItems(request, typeName):
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

  items = cache.get("search_%s" % typeName)

  if items is None:
    # List wasn't in cache, let's fetch it from the database.
    itemQuery = Item.objects.filter(typeName__icontains=typeName, published=True,
        categoryID_id__in=CATEGORIES_ITEMS)

    # Augment with CPU and PG info.
    items = getCPUandPG(itemQuery)

    # Now store it in cache.
    cache.set("search_%s" % typeName, items)

  return render_to_response("items.html", locals())

