from django.http import Http404, HttpResponse
from django.shortcuts import render
import json


def home(request):
  # Get the stats widgets positions.
  widgetPositions = ["stats1.html", "stats2.html"]

  if "widgetPositions" in request.COOKIES:
    try:
      widgetPositions = json.loads(request.COOKIES["widgetPositions"])
    except ValueError:
      pass

  return render(request, 'index.html', locals())

def updateWidgetPositions(request):
  if not request.is_ajax():
    raise Http404

  if request.method != "GET":
    raise Http404

  widgetPositions = json.dumps(request.GET.getlist("widgetPositions[]"))
  if not widgetPositions:
    raise Http404

  response = HttpResponse("updated")
  response.set_cookie("widgetPositions", widgetPositions,
      max_age = 30 * 24 * 3600)
  return response
