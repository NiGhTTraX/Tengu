from django.http import Http404, HttpResponse
from django.shortcuts import render
import json


def home(request):
  # Get the stats widgets positions.
  widgetPositions = ["stats1", "stats2"]
  widgetStatuses = [True] * len(widgetPositions)

  if "widgets" in request.COOKIES and "widgetStatuses" in request.COOKIES:
    try:
      widgetPositions = json.loads(request.COOKIES["widgets"])
      cookie = json.loads(request.COOKIES["widgetStatuses"])
      widgetStatuses = [x == "true" for x in cookie]
    except ValueError: pass

  widgets = zip(widgetPositions, widgetStatuses)

  return render(request, 'index.html', locals())

def updateWidgetPositions(request):
  if not request.is_ajax():
    raise Http404

  if request.method != "GET":
    raise Http404

  print request.GET
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
