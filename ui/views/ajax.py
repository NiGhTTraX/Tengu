from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from dogma.models import TypeAttributes
from inv.models import MarketGroup, Item
from ui.utils import getCPUandPG

import json


CATEGORIES_ITEMS = [
    7,      # Modules
    8,      # Charges
    18,     # Drones
    20,     # Implants
    32      # Subsystems
]
CATEGORIES_SHIPS = [6]

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
  """Retreives items from a market group."""
  if not request.is_ajax():
    raise Http404

  try:
    marketGroup = MarketGroup.objects.get(pk=marketGroupID)
  except MarketGroup.DoesNotExist:
    raise Http404

  itemQuery = Item.objects.filter(marketGroupID = marketGroup,
                                  published=True).order_by("typeName")
  items = __getCPUandPG(itemQuery)

  return render_to_response("items.html", locals())

def searchItems(request, typeName):
  """Searches for items by name.

  You have to check if the items belong to a valid market group i.e. the ones
  being displayed in the market tree. To do this, you have to resolve the
  category ID which is linked to by the group ID.
  """
  if not request.is_ajax():
    raise Http404

  itemQuery = Item.objects.filter(typeName__icontains=typeName, published=True,
      groupID__categoryID__in=CATEGORIES_ITEMS)
  items = __getCPUandPG(itemQuery)
  return render_to_response("items.html", locals())

