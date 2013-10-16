from django.template.loader import render_to_string

from cache import DjangoCacheHandler, DjangoDataHandler
from eos import Eos
from raven import RFit


def renderFit(fit):
  # Set up Eos.
  Eos(DjangoDataHandler(), DjangoCacheHandler(), makeDefault=True)

  # Set up Raven.
  rfit = RFit(fit.shipID.pk)

  return render_to_string("wheel.html", {"fit": fit, "rfit": rfit})

