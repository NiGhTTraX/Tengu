from django.db import models
from django.contrib.auth.models import User

from service.utils import base_encode


class Fit(models.Model):
  PRIVATE = 0
  LINK = 1
  CORPORATION = 2
  ALLIANCE = 3
  VISIBILITY_CHOICES = (
      (ALLIANCE, "ALLIANCE"),
      (CORPORATION, "CORPORATION"),
      (LINK, "BY LINK"),
      (PRIVATE, "PRIVATE")
  )

  fitName = models.CharField(max_length = 200)
  fitDescription = models.TextField(null = True)
  shipID = models.ForeignKey("inv.Item")

  userID = models.ForeignKey(User, null = True)
  sessionID = models.CharField(max_length = 32, null = True) # For anonymous users.

  public = models.BooleanField(default = False)
  visibility = models.IntegerField(choices = VISIBILITY_CHOICES,
                                   default = PRIVATE)

  highs = models.CharField(max_length = 2000, null = True)
  meds = models.CharField(max_length = 2000, null = True)
  lows = models.CharField(max_length = 2000, null = True)
  rigs = models.CharField(max_length = 2000, null = True)
  subsystems = models.CharField(max_length = 2000, null = True)
  drones = models.CharField(max_length = 2000, null = True)
  charges = models.CharField(max_length = 2000, null = True)

  created = models.DateTimeField(auto_now_add = True)
  modified = models.DateTimeField(auto_now = True)

  views = models.IntegerField(default = 0)
  rating = models.IntegerField(default = 0)

  @property
  def url(self):
    return base_encode(self.pk)


class Profile(models.Model):
  user = models.OneToOneField(User)

  apiKeyID = models.IntegerField(null = True)
  apiVCode = models.CharField(max_length = 64, null = True)
  charID = models.IntegerField(null = True)

  charName = models.CharField(max_length = 100, null = True)
  corporation = models.CharField(max_length = 100, null = True)
  alliance = models.CharField(max_length = 100, null = True)

  fits = models.ManyToManyField(Fit, related_name="fits")
  favorites = models.ManyToManyField(Fit, related_name="favorites")

