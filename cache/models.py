from django.db import models

# Create your models here.
class Metadata(models.Model):
  fieldName = models.CharField(max_length=20)
  fieldValue = models.CharField(max_length=20)

