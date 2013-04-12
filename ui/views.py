from django.http import Http404, HttpResponse
from django.shortcuts import render
from ui.utils import buildMarketTree
from inv.models import MarketGroup
import json


def __getWidgets(request):
  """Return the positions and statuses of the stats widgets.

  Args:
    request: Django request

  Returns:
    A list of tuples in the form (widget_name, widget_status). widget_status is
    True if the widget is expanded, False otherwise. widget_name is the name of
    the template, minus the .html extension (needs to be added in the template).

  Excepts:
    ValueError.
  """
  widgetPositions = ["stats1", "stats2"]
  widgetStatuses = [True] * len(widgetPositions)

  if "widgets" in request.COOKIES and "widgetStatuses" in request.COOKIES:
    try:
      cookie = json.loads(request.COOKIES["widgets"])
      if sorted(cookie) != sorted(widgetPositions): # sanity check
        raise ValueError
      widgetPositions = cookie

      cookie = json.loads(request.COOKIES["widgetStatuses"])
      widgetStatuses = [x == "true" for x in cookie]
    except ValueError: pass

  return zip(widgetPositions, widgetStatuses)

def __getResizeHandler(request):
  """Returns the left sidebar resize handler position."""
  resizeHandlerTop = None
  if "leftSidebarResizeHandle" in request.COOKIES:
    try:
      resizeHandlerTop = int(request.COOKIES["leftSidebarResizeHandle"])
    except ValueError: pass

  return resizeHandlerTop

def __getMarketTree(request, marketGroupsToGet):
  """Gets the market tree structure and status.

  Params:
    request: Django request.
    marketGroupsToGet: A list of integer ids.

  Returns:
    A list of two elements. The first is the market tree and the second is the
    expanded groups.
  """
  marketGroups = []
  for group in marketGroupsToGet:
    marketGroups.extend(buildMarketTree(MarketGroup.objects.get(pk=group)))

  # Now get which ones should be expanded.
  expandedGroups = []
  if "expandedMarketGroups" in request.COOKIES:
    cookie = json.loads(request.COOKIES["expandedMarketGroups"])
    expandedGroups = [long(x) for x in cookie]

  return [marketGroups, expandedGroups]


def home(request):
  """Home page view."""
  # Get the stats widgets.
  widgets = __getWidgets(request)

  # Get the left sidebar resize handler.
  resizeHandlerTop = __getResizeHandler(request)

  # Get the market groups.
  marketGroupsToGet = [
      211,    # Ammunition and Charges
      157,    # Drones
      24,     # Implants and Boosters
      9,      # Ship Equipment
      955     # Ship Modifications
  ]
  [marketGroups, expandedGroups] = __getMarketTree(request, marketGroupsToGet)

  return render(request, 'index.html', locals())

def updateWidgetPositions(request):
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

def updateLeftSidebarResizeHandler(request):
  """Updates the left sidebar resize handler."""
  if not request.is_ajax():
    raise Http404

  if request.method != "GET":
    raise Http404

  if "top" not in request.GET:
    raise Http404

  top = 0
  try:
    top = int(request.GET["top"])
  except ValueError:
    raise Http404

  response = HttpResponse("updated")
  response.set_cookie("leftSidebarResizeHandle", top, max_age = 30 * 24 * 3600)

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

