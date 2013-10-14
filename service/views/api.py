from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from service.models import Fit

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

