from django.template.loader import render_to_string

from ui.utils import getSlots
from raven import RFit

import json
import urllib


def getWidgets(request):
  """Return the positions and statuses of the stats widgets.

  Args:
    request: Django request

  Returns:
    A list of dictionaries with 2 keys, name and visible.
    visble is True if the widget is expanded, False otherwise.
    name is the name of the template, minus the .html extension (needs to be
    added in the template).
  """
  widgets = ["stats_defense", "stats2"]
  statsWidgets = [{"name": w, "visible": True} for w in widgets]

  if "statsWidgets" in request.COOKIES:
    try:
      cookie = urllib.parse.unquote(request.COOKIES["statsWidgets"])
      cookie = json.loads(cookie)
      if sorted([w["name"] for w in cookie]) != sorted(widgets): # sanity check
        raise ValueError
      statsWidgets = cookie
    except ValueError: pass

  return statsWidgets

def renderFit(request, fit):
  """Renders the necessary templates for a fit.

  Args:
    request: Django request instance, required for the widgets cookie.
    fit: Fit instance. The view assumes the fit exists and that the user is
    allowed to view it.

  Returns:
    A dictionary in the form {
      wheel: Wheel view of the fit.
      stats: The stats widgets.
    }
  """
  slots = getSlots(fit.shipID)
  wheelView = render_to_string("fit.html", {"fit": fit, "slots": slots})

  widgets = getWidgets(request)
  rfit = RFit(fit.shipID.pk)
  stats = render_to_string("stats.html", {
    "fit": rfit,
    "widgets": widgets
  })

  return {
      "wheel": wheelView,
      "stats": stats
  }

