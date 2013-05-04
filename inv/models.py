from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class MarketGroup(models.Model):
  marketGroupID = models.AutoField(primary_key=True)
  parentGroupID = models.ForeignKey("self", db_column="parentGroupID", null=True)
  marketGroupName = models.CharField(max_length=200, null=True)
  description = models.CharField(max_length=3000, null=True)
  iconID = models.IntegerField(null=True)
  hasTypes = models.NullBooleanField()
  descriptionID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  graphicID = models.IntegerField(null=True)
  marketGroupNameID = models.IntegerField(null=True)


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
  groupID = models.ForeignKey(Group, db_column="GroupID", null=True)
  typeName = models.CharField(max_length=100, null=True)
  description = models.CharField(max_length=3000, null=True)
  mass = models.FloatField(null=True)
  volume = models.FloatField(null=True)
  capacity = models.FloatField(null=True)
  published = models.NullBooleanField()
  marketGroupID = models.ForeignKey(MarketGroup, db_column="marketGroupID",
      null=True)
  # unused fields
  radius = models.FloatField(null=True)
  portionSize = models.IntegerField(null=True)
  basePrice = models.FloatField(null=True)
  chanceOfDuplicating = models.FloatField(null=True)
  IconID = models.IntegerField(null=True)
  soundID = models.IntegerField(null=True)
  copyTypeID = models.IntegerField(null=True)
  graphicID = models.IntegerField(null=True)
  typeNameID = models.IntegerField(null=True)
  descriptionID = models.IntegerField(null=True)
  raceID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)

  attributes = models.ManyToManyField("dogma.Attribute",
      through="dogma.TypeAttributes")

  effects = models.ManyToManyField("dogma.Effect", through="dogma.TypeEffects")

  def __str__(self):
    return self.typeName

