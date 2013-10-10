from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.models import get_current_site
from django.core.cache import cache

from ui.utils import MarketTree, getSlots
from dogma.models import TypeAttributes
from inv.models import MarketGroup, Item
from service.models import Fit
from service.utils import base_decode
from service.views.api import getFit
from ui.views.render import renderFit, getWidgets

from inv.const import MARKET_GROUPS_ITEMS, MARKET_GROUPS_SHIPS

import json


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

  return marketTree

def __getExpandedGroups(request):
  # Now get which ones should be expanded.
  expandedGroups = []
  if "expandedMarketGroups" in request.COOKIES:
    cookie = json.loads(request.COOKIES["expandedMarketGroups"])
    expandedGroups = [int(x) for x in cookie]

  return expandedGroups

@ensure_csrf_cookie
def home(request, fitURL = None):
  """Home page view."""
  siteName = get_current_site(request).name

  # Get the stats widgets.
  widgets = getWidgets(request)

  # Get the left sidebar resize handler.
  resizeHandlerTop = __getResizeHandler(request)

  # Get the market groups.
  marketGroupsItems = __getMarketTree(request, MARKET_GROUPS_ITEMS)
  marketGroupsShips = __getMarketTree(request, MARKET_GROUPS_SHIPS, True)
  expandedGroups = __getExpandedGroups(request)

  # Unpack some constants
  INCREASE_INDENT = MarketTree.INCREASE_INDENT
  DECREASE_INDENT = MarketTree.DECREASE_INDENT
  GROUP = MarketTree.GROUP
  ITEM = MarketTree.ITEM

  # Are we viewing a fit?
  if fitURL:
    fitID = base_decode(fitURL)
    fit = getFit(request, fitID)
    if not fit:
      raise Http404

    renders = renderFit(request, fit)

  """
  Some views require the session key. In order to get the key, a session must
  exist. Django only creates a new session when it is marked as modified, so we
  check if a session exists and in case it doesn't, we create one.
  """
  if request.session.session_key is None:
    request.session.modified = True

  return render(request, 'index.html', locals())

