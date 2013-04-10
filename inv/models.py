from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class MarketGroup(models.Model):
  marketGroupID = models.AutoField(primary_key=True)
  parentGroupID = models.ForeignKey("self", db_column="parentGroupID")
  marketGroupName = models.CharField(max_length=200)
  description = models.CharField(max_length=3000)
  iconID = models.IntegerField()
  hasTypes = models.BooleanField()
  descriptionID = models.IntegerField()
  dataID = models.IntegerField()
  graphicID = models.IntegerField()
  marketGroupNameID = models.IntegerField()

  def __str__(self):
    try:
      return str(self.parentGroupID) + "/" + self.marketGroupName
    except ObjectDoesNotExist:
      return self.marketGroupName


class Category(models.Model):
  categoryID = models.AutoField(primary_key=True)
  categoryName = models.CharField(max_length=100)
  description = models.CharField(max_length=3000)
  published = models.BooleanField()
  # unusued fields
  dataID = models.IntegerField(null=True)
  categoryNameID = models.IntegerField(null=True)
  iconID = models.IntegerField(null=True)


  def __str__(self):
    return self.categoryName


class Group(models.Model):
  groupID = models.AutoField(primary_key=True)
  categoryID = models.ForeignKey(Category, db_column="categoryID")
  groupName = models.CharField(max_length=100)
  description = models.CharField(max_length=3000)
  # unused fields
  groupNameID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  IconID = models.IntegerField()
  useBasePrice = models.BooleanField()
  allowManufacture = models.BooleanField()
  allowRecycler = models.BooleanField()
  anchored = models.BooleanField()
  anchorable = models.BooleanField()
  fittableNonSingleton = models.BooleanField()
  published = models.BooleanField()

  def __str__(self):
    return self.groupName


class Item(models.Model):
  typeID = models.AutoField(primary_key=True)
  groupID = models.ForeignKey(Group, db_column="GroupID")
  typeName = models.CharField(max_length=100)
  description = models.CharField(max_length=3000)
  mass = models.FloatField()
  volume = models.FloatField()
  capacity = models.FloatField()
  published = models.BooleanField()
  marketGroupID = models.ForeignKey(MarketGroup, db_column="marketGroupID")
  # unused fields
  radius = models.FloatField()
  portionSize = models.IntegerField()
  basePrice = models.FloatField()
  chanceOfDuplicating = models.FloatField()
  IconID = models.IntegerField()
  soundID = models.IntegerField()
  copyTypeID = models.IntegerField()
  graphicID = models.IntegerField()
  typeNameID = models.IntegerField()
  descriptionID = models.IntegerField()
  raceID = models.IntegerField()
  dataID = models.IntegerField()

  attributes = models.ManyToManyField("dogma.Attribute",
      through="dogma.TypeAttributes")

  effects = models.ManyToManyField("dogma.Effect", through="dogma.TypeEffects")

  def __str__(self):
    return self.typeName

