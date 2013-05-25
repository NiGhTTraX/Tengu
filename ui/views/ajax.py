from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response
from dogma.models import TypeAttributes
from inv.models import MarketGroup, Item
import json


CATEGORIES_ITEMS = [
    7,      # Modules
    8,      # Charges
    18,     # Drones
    20,     # Implants
    32      # Subsystems
]
CATEGORIES_SHIPS = [6]

ATTRIBUTE_CPU = 50
ATTRIBUTE_PG = 30


def __getCPUandPG(itemsIter):
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
    except ObjectDoesNotExist:
      pass

    items.append((item, cpu, pg))

  return items

def updateWidgets(request):
  """Updates the stats widgets in the right sidebar.

  This function retrieves the position and status of the stats widget via a GET
  request and stores them in cookies. The contents are dumped in JSON format.
  """
  if not request.is_ajax():
    raise Http404

  if request.method != "GET":
    raise Http404

  if "widgets[]" not in request.GET or "widgetStatuses[]" not in request.GET:
    raise Http404

  widgets = json.dumps(request.GET.getlist("widgets[]"))
  widgetStatuses = json.dumps(request.GET.getlist("widgetStatuses[]"))
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

  if request.method != "GET":
    raise Http404

  groups = json.dumps(request.GET.getlist("expandedGroups[]"))
  response = HttpResponse("updated")
  response.set_cookie("expandedMarketGroups", groups, max_age = 30 * 24 * 3600)
  return response

def getItems(request, marketGroupID):
  """Retreives items from a market group."""
  if not request.is_ajax():
    raise Http404

  try:
    marketGroup = MarketGroup.objects.get(pk=marketGroupID)
  except ObjectDoesNotExist:
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

def searchShipsAndFits(request, name):
  """Searches for ships and fits.

  First, get the ships that will include links to create new fittings. Then get
  all the existing fits that contain the provided keywords.
  """
  if not request.is_ajax():
    raise Http404

  fits = []
  # First, get the ships.
  itemQuery = Item.objects.filter(typeName__icontains=name, published=True,
      groupID__categoryID__in=CATEGORIES_SHIPS)
  fits = [(0, item) for item in itemQuery]

  # Then, the fits.
  # TODO

  return render_to_response("ships.html", locals())

def getFits(request, typeID):
  """Get fits by ship type ID.

  First, get the ship itself that will have a link to create a new fitting for
  that ship. Then get all the existing fittings that use that ship.
  """
  if not request.is_ajax():
    raise Http404

  fits = []
  # First, get the ship.
  item = Item.objects.get(typeID=typeID)
  fits = [(0, item)]

  # Then, the fits.
  # TODO

  return render_to_response("ships.html", locals())

