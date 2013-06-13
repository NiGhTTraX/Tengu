from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.db.models import Q

from service.models import Fit
from ui.utils import getSlots
from inv.models import Item

import json
CATEGORIES_SHIPS = [6]


def __getVisibilityQuery(request):
  """Create the visibility query for fits.

  A user can only view the fits created by him or any public fit. You should
  first construct your query using this function and then append any other
  queries.

  If the user is anonymous then he/she can only view public fits.

  TODO: Get alliance and corporation fits.

  Returns:
    Q instance.
  """
  if request.user.pk:
    return Q(userID = request.user.pk) | Q(public=True)

  return Q(sessionID = request.session.session_key) | Q(public=True)

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
  q = __getVisibilityQuery(request)
  q &= Q(fitName__icontains=name) | Q(shipID__typeName__icontains=name)
  fits.extend([(1, fit.shipID, fit) for fit in Fit.objects.filter(q)])

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
  try:
    item = Item.objects.get(typeID=typeID)
    fits = [(0, item)]
  except Item.DoesNotExist:
    raise Http404

  # Then, the fits.
  q = __getVisibilityQuery(request) & Q(shipID=typeID)
  fits.extend([(1, fit.shipID, fit) for fit in Fit.objects.filter(q)])

  return render_to_response("ships.html", locals())

def newFit(request, typeID):
  """Creates a new fit with the given ship.

  Returns:
    JSON response containing fitID, fitURL, shipName and the html.
  """
  if not request.is_ajax():
    raise Http404

  try:
    ship = Item.objects.get(pk = typeID)
  except Item.DoesNotExist:
    raise Http404

  # Create a new Fit object and store it.
  fit = Fit()
  fit.shipID = ship
  fit.fitName = ship.typeName

  fit.userID = request.user.pk
  if not request.user.pk:
    # Anonymous users will have their fits stored by their session key.
    # Anonymous fits will be deleted on a regular basis.
    fit.sessionID = request.session.session_key

  fit.save()
  fitID = fit.pk

  # Get the URL for this new fit.
  fitURL = fit.url

  # Get slots.
  slots = getSlots(typeID)

  template = render_to_string("fit.html", {"fit": fit, "slots": slots})

  response = {
      "fitID": fitID,
      "fitURL": fitURL,
      "shipName": ship.typeName,
      "html": template
  }

  return HttpResponse(json.dumps(response), mimetype="application/json")

def getFit(request, fitID):
  """Get a fit by ID and render it.

  Returns:
    JSON response containing fitID, fitURL, shipName and the html.
  """
  if not request.is_ajax():
    raise Http404

  try:
    fit = Fit.objects.get(pk = fitID)
  except Fit.DoesNotExist:
    raise Http404

  if fit.userID:
    if fit.userID != request.user.pk:
      return HttpResponseForbidden()
  elif fit.sessionID != request.session.session_key:
    return HttpResponseForbidden()

  fitURL = fit.url

  # Get slots.
  slots = getSlots(fit.shipID)

  template = render_to_string("fit.html", {"fit": fit, "slots": slots})

  response = {
      "fitID": fitID,
      "fitURL": fitURL,
      "shipName": fit.shipID.typeName,
      "html": template
  }

  return HttpResponse(json.dumps(response), mimetype="application/json")

