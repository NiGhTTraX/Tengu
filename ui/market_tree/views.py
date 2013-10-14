from django.http import Http404, HttpResponse

import json


def updateMarketTree(request):
  """Updates the market tree expanded groups."""
  if not request.is_ajax():
    raise Http404

  if request.method != "POST":
    raise Http404

  groups = json.dumps(request.POST.getlist("expandedGroups[]"))
  response = HttpResponse("updated")
  response.set_cookie("expandedMarketGroups", groups, max_age = 30 * 24 * 3600)

  return response

