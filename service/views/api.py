from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from service.models import Fit
from ui.utils import getSlots

import json


def getFit(request, fitID):
  """Get a fit by ID.

  This needs to check if the user is allowed to view the specified fit. Users
  can only view non-public fits if they are created by them.

  Returns:
    Fit instance or None in case the fit doesn't exist or the user isn't allowed
    to view it.
  """
  try:
    fit = Fit.objects.get(pk = fitID)
  except Fit.DoesNotExist:
    return None

  # Check if the user is allowed to view this fit.
  if not fit.public:
    if fit.userID and fit.userID != request.user.pk:
      return None
    elif fit.sessionID != request.session.session_key:
      return None

  return fit

def viewFit(request, fitID, returnType = "json"):
  """Get a fit by ID and render it using the fit template.

  Args:
    returnType: can be:
      "html": will render the fit template and return the HTML.
      "json": will return a JSON object including fit details and the HTML.

  Returns:
    HTML or JSON. See the args section for returnType.
  """
  fit = getFit(request, fitID)
  if not fit:
    raise Http404

  slots = getSlots(fit.shipID)
  template = render_to_string("fit.html", {"fit": fit, "slots": slots})

  if returnType == "html":
    return template

  if returnType == "json":
    fitURL = fit.url
    response = {
        "fitID": fitID,
        "fitURL": fitURL,
        "shipName": fit.shipID.typeName,
        "html": template
    }

    return HttpResponse(json.dumps(response), mimetype="application/json")

  # Invalid return type.
  raise Http404

