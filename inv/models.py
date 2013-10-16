from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class MarketGroup(models.Model):
  marketGroupID = models.IntegerField(primary_key=True)
  parentGroupID = models.ForeignKey("self", db_column="parentGroupID",
      null=True, on_delete=models.DO_NOTHING)
  marketGroupName = models.CharField(max_length=200, null=True)
  description = models.CharField(max_length=3000, null=True)
  iconID = models.IntegerField(null=True)
  hasTypes = models.NullBooleanField()
  descriptionID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  graphicID = models.IntegerField(null=True)
  marketGroupNameID = models.IntegerField(null=True)


class Category(models.Model):
  categoryID = models.IntegerField(primary_key=True)
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
  groupID = models.IntegerField(primary_key=True)
  categoryID = models.ForeignKey(Category, db_column="categoryID",
      on_delete=models.DO_NOTHING)
  groupName = models.CharField(max_length=100, null=True)
  description = models.CharField(max_length=3000, null=True)
  # unused fields
  groupNameID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  iconID = models.IntegerField(null=True)
  useBasePrice = models.NullBooleanField()
  allowManufacture = models.NullBooleanField()
  allowRecycler = models.NullBooleanField()
  anchored = models.NullBooleanField()
  anchorable = models.NullBooleanField()
  fittableNonSingleton = models.NullBooleanField()
  published = models.NullBooleanField()

  def __str__(self):
    return self.groupName


class Item(models.Model):
  typeID = models.IntegerField(primary_key=True)
  groupID = models.ForeignKey(Group, db_column="groupID", null=True,
      on_delete=models.DO_NOTHING)
  typeName = models.CharField(max_length=100, db_index=True, null=True)
  description = models.CharField(max_length=3000, null=True)
  mass = models.FloatField(null=True)
  volume = models.FloatField(null=True)
  capacity = models.FloatField(null=True)
  published = models.NullBooleanField()
  marketGroupID = models.ForeignKey(MarketGroup, db_column="marketGroupID",
      null=True, on_delete=models.DO_NOTHING)
  # unused fields
  radius = models.FloatField(null=True)
  portionSize = models.IntegerField(null=True)
  basePrice = models.FloatField(null=True)
  chanceOfDuplicating = models.FloatField(null=True)
  iconID = models.IntegerField(null=True)
  soundID = models.IntegerField(null=True)
  copyTypeID = models.IntegerField(null=True)
  graphicID = models.IntegerField(null=True)
  typeNameID = models.IntegerField(null=True)
  descriptionID = models.IntegerField(null=True)
  raceID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)

  attributes = models.ManyToManyField("dogma.Attribute",
      through="dogma.TypeAttributes")
  effects = models.ManyToManyField("dogma.Effect",
      through="dogma.TypeEffects")

  categoryID = models.ForeignKey(Category, null = True,
      on_delete=models.DO_NOTHING)
  durationAttributeID = models.IntegerField(null=True)
  dischargeAttributeID = models.IntegerField(null=True)
  rangeAttributeID = models.IntegerField(null=True)
  falloffAttributeID = models.IntegerField(null=True)
  trackingSpeedAttributeID = models.IntegerField(null=True)
  fittableNonSingleton = models.NullBooleanField()

  HIGH = 1
  MED = 2
  LOW = 3
  RIG = 4
  SUB = 5
  SLOT_CHOICES = (
      (HIGH, "High"),
      (MED, "Medium"),
      (LOW, "Low"),
      (RIG, "Rig"),
      (SUB, "Subsystem")
  )
  slot = models.IntegerField(choices = SLOT_CHOICES, null=True)

  MISSILE = 1
  TURRET = 2
  HARDPOINT_CHOICES = (
      (MISSILE, "Missle launcher"),
      (TURRET, "Turret bay")
  )
  hardpoint = models.IntegerField(choices = HARDPOINT_CHOICES, null=True)

  def __str__(self):
    return self.typeName

