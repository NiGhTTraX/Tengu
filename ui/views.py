from django.http import Http404, HttpResponse
from django.shortcuts import render
from ui.utils import buildMarketTree
from inv.models import MarketGroup
import json


def home(request):
  # Get the stats widgets positions.
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

  widgets = zip(widgetPositions, widgetStatuses)

  # Get the left sidebar resize handler position.
  resizeHandlerTop = None
  if "leftSidebarResizeHandle" in request.COOKIES:
    try:
      resizeHandlerTop= int(request.COOKIES["leftSidebarResizeHandle"])
    except ValueError: pass

  # Get the market groups.
  marketGroups = []
  marketGroupsToGet = [
      211,    # Ammunition and Charges
      157,    # Drones
      24,     # Implants and Boosters
      9,      # Ship Equipment
      955     # Ship Modifications
  ]

  for group in marketGroupsToGet:
    marketGroups.extend(buildMarketTree(MarketGroup.objects.get(pk=group)))

  # Now get which ones should be expanded.
  expandedGroups = []
  if "expandedMarketGroups" in request.COOKIES:
    cookie = json.loads(request.COOKIES["expandedMarketGroups"])
    expandedGroups = [long(x) for x in cookie]

  return render(request, 'index.html', locals())

def updateWidgetPositions(request):
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
  if not request.is_ajax():
    raise Http404

  if request.method != "GET":
    raise Http404

  groups = json.dumps(request.GET.getlist("expandedGroups[]"))
  response = HttpResponse("updated")
  response.set_cookie("expandedMarketGroups", groups, max_age = 30 * 24 * 3600)
  return response

