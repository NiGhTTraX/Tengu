from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

from ui.utils import buildMarketTree, getSlots
from dogma.models import TypeAttributes
from inv.models import MarketGroup, Item
from service.models import Fit
from service.utils import base_decode

import json


MARKET_GROUPS_ITEMS = [
    11,     # Ammunition and Charges
    157,    # Drones
    24,     # Implants and Boosters
    9,      # Ship Equipment
    955     # Ship Modifications
]
MARKET_GROUP_SHIPS = 4
MARKET_GROUPS_SHIPS = MarketGroup.objects.filter(
    parentGroupID = MARKET_GROUP_SHIPS).order_by("marketGroupName").values_list(
        "marketGroupID", flat=True)


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

def __getMarketTree(request, marketGroupsToGet, includeItems = False):
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
    marketGroups.extend(buildMarketTree(MarketGroup.objects.get(pk=group),
                                        includeItems))
  return marketGroups

def __getExpandedGroups(request):
  # Now get which ones should be expanded.
  expandedGroups = []
  if "expandedMarketGroups" in request.COOKIES:
    cookie = json.loads(request.COOKIES["expandedMarketGroups"])
    expandedGroups = [long(x) for x in cookie]

  return expandedGroups

@ensure_csrf_cookie
def home(request, fitURL = None):
  """Home page view."""
  siteName = settings.SITE_NAME

  # Get the stats widgets.
  widgets = __getWidgets(request)

  # Get the left sidebar resize handler.
  resizeHandlerTop = __getResizeHandler(request)

  # Get the market groups.
  marketGroupsItems = __getMarketTree(request, MARKET_GROUPS_ITEMS)
  marketGroupsShips = __getMarketTree(request, MARKET_GROUPS_SHIPS, True)
  expandedGroups = __getExpandedGroups(request)

  # Are we viewing a fit?
  if fitURL:
    fitID = base_decode(fitURL)
    try:
      fit = Fit.objects.get(pk = fitID)

      # Get slots.
      slots = getSlots(fit.shipID)
    except Fit.DoesNotExist:
      fit = None

  return render(request, 'index.html', locals())

