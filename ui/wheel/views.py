from django.template.loader import render_to_string


def renderFit(fit):
  # TODO: get fit from fitting server
  rfit = {
      "slots": {
        "highSlots": 8,
        "medSlots": 8,
        "lowSlots": 8,
        "rigSlots": 5,
        "subSlots": 5,
        "turretSlots": 8,
        "missileSlots": 8
      }
  }

  return render_to_string("wheel.html", {"fit": fit, "rfit": rfit})

