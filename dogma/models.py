from django.db import models


class Operand(models.Model):
  operandID = models.AutoField(primary_key=True)
  description = models.CharField(max_length=1000)
  format = models.CharField(max_length=100)
  pythonFormat = models.CharField(max_length=100)
  # unused fields
  resultCategoryID = models.IntegerField(null=True)
  operandKey = models.CharField(max_length=20)
  arg1categoryID = models.IntegerField(null=True)
  arg2categoryID = models.IntegerField(null=True)

  def __str__(self):
    return "%s(%s)" % (self.operandKey, self.operandID)


class Unit(models.Model):
  unitID = models.AutoField(primary_key=True)
  unitName = models.CharField(max_length=100)
  displayName = models.CharField(max_length=50)
  description = models.CharField(max_length=1000)
  # unused fields
  descriptionID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  displayNameID = models.IntegerField(null=True)


class Attribute(models.Model):
  attributeID = models.AutoField(primary_key=True)
  attributeName = models.CharField(max_length=200)
  description = models.CharField(max_length=1000)
  defaultValue = models.FloatField()
  published = models.BooleanField()
  displayName = models.CharField(max_length=100)
  unitID = models.ForeignKey(Unit, db_column="unitID")
  stackable = models.BooleanField()
  highIsGood = models.BooleanField()
  # unused fields
  categoryID = models.IntegerField(null=True)
  attributeCategory = models.IntegerField(null=True)
  IconID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  maxAttributeID = models.IntegerField(null=True)
  attributeIdx = models.IntegerField(null=True)
  chargeRechargeTimeID = models.IntegerField(null=True)
  categoryID = models.IntegerField(null=True)
  displayNameID = models.IntegerField(null=True)

  def __str__(self):
    return self.attributeName


class TypeAttributes(models.Model):
  typeID = models.ForeignKey("inv.Item", db_column="typeID")
  attributeID = models.ForeignKey(Attribute, db_column="attributeID")
  value = models.FloatField()

  def __str__(self):
    return "%s: %f" % (self.attributeID.attributeName, self.value)


class Expression(models.Model):
  expressionID = models.AutoField(primary_key=True)
  expressionName = models.TextField()
  description = models.TextField()
  expressionValue = models.TextField()
  expressionAttributeID = models.ForeignKey(Attribute,
      db_column="expressionAttributeID")
  operandID = models.ForeignKey(Operand, db_column="operandID")
  arg1 = models.ForeignKey("self", db_column="arg1", related_name="+")
  arg2 = models.ForeignKey("self", db_column="arg2", related_name="+")
  # unused fields
  expressionGroupID = models.ForeignKey("inv.Group",
      db_column="expressionGroupID")
  expressionTypeID = models.ForeignKey("inv.Item",
      db_column="expressionTypeID")

  def __str__(self):
    return self.expressionName


class Effect(models.Model):
  effectID = models.AutoField(primary_key=True)
  effectName = models.CharField(max_length=100)
  preExpression = models.ForeignKey(Expression, db_column="preExpression",
      related_name="+")
  postExpression = models.ForeignKey(Expression, db_column="postExpression",
      related_name="+")
  description = models.CharField(max_length=1000)
  isOffensive = models.BooleanField()
  isAssistance = models.BooleanField()
  durationAttributeID = models.ForeignKey(Attribute,
      db_column="durationAttributeID", related_name="+")
  trackingSpeedAttributeID = models.ForeignKey(Attribute,
      db_column="trackingSpeedAttributeID", related_name="+")
  dischargeAttributeID = models.ForeignKey(Attribute,
      db_column="dischargeAttributeID", related_name="+")
  rangeAttributeID = models.ForeignKey(Attribute, db_column="rangeAttributeID",
      related_name="+")
  falloffAttributeID = models.ForeignKey(Attribute,
      db_column="falloffAttributeID", related_name="+")
  disallowAutoRepeat = models.BooleanField()
  published = models.SmallIntegerField()
  displayName = models.CharField(max_length=100)
  # unused fields
  effectCategory = models.SmallIntegerField(null=True)
  displayNameID = models.IntegerField(null=True)
  descriptionID = models.IntegerField(null=True)
  guid = models.CharField(max_length=60, null=True)
  IconID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  isWarpSafe = models.BooleanField()
  rangeChance = models.BooleanField()
  electronicChance = models.BooleanField()
  propulsionChance = models.BooleanField()
  distribution = models.SmallIntegerField(null=True)
  sfxName = models.CharField(max_length=20, null=True)
  npcUsageChanceAttributeID = models.SmallIntegerField(null=True)
  npcActivationChanceAttributeID = models.SmallIntegerField(null=True)
  fittingUsageChanceAttributeID = models.SmallIntegerField(null=True)

  def __str__(self):
    return self.preExpression.expressionName

class TypeEffects(models.Model):
  typeID = models.ForeignKey("inv.Item", db_column="typeID")
  effectID = models.ForeignKey(Effect, db_column="effectID")
  IsDefault = models.BooleanField()
