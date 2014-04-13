from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.models import get_current_site
from django.core.cache import cache

from ui.wheel.views import renderFit
from dogma.models import TypeAttributes
from inv.models import MarketGroup, Item
from service.utils import base_decode
from service.models import Fit
from service.views import getFit

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


@ensure_csrf_cookie
def home(request, fitURL = None):
  """Home page view."""
  siteName = get_current_site(request).name

  # Get the left sidebar resize handler.
  resizeHandlerTop = __getResizeHandler(request)

  marketGroupsItems = MARKET_GROUPS_ITEMS
  marketGroupsShips = MARKET_GROUPS_SHIPS

  if fitURL:
    fitID = base_decode(fitURL)
    fit = getFit(request, fitID)
    if fit is None:
      raise Http404

    wheel = renderFit(fit)

  """
  Some views require the session key. In order to get the key, a session must
  exist. Django only creates a new session when it is marked as modified, so we
  check if a session exists and in case it doesn't, we create one.
  """
  if request.session.session_key is None:
    request.session.modified = True

  return render(request, "index.html", locals())

