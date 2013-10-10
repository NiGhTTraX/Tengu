from django.db import models


class Operand(models.Model):
  operandID = models.IntegerField(primary_key=True)
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
  unitID = models.IntegerField(primary_key=True)
  unitName = models.CharField(max_length=100)
  displayName = models.CharField(max_length=50)
  description = models.CharField(max_length=1000)
  # unused fields
  descriptionID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  displayNameID = models.IntegerField(null=True)


class Attribute(models.Model):
  attributeID = models.IntegerField(primary_key=True)
  attributeName = models.CharField(max_length=200)
  description = models.CharField(max_length=1000)
  defaultValue = models.FloatField()
  published = models.BooleanField()
  displayName = models.CharField(max_length=100)
  unitID = models.ForeignKey(Unit, db_column="unitID", null=True,
      on_delete=models.DO_NOTHING)
  stackable = models.BooleanField()
  highIsGood = models.BooleanField()
  # unused fields
  attributeCategory = models.IntegerField(null=True)
  iconID = models.IntegerField(null=True)
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
  expressionID = models.IntegerField(primary_key=True)
  expressionName = models.TextField()
  description = models.TextField(null=True)
  expressionValue = models.TextField(null=True)
  expressionAttributeID = models.ForeignKey(Attribute,
      db_column="expressionAttributeID", null=True, on_delete=models.DO_NOTHING)
  operandID = models.ForeignKey(Operand, db_column="operandID",
      on_delete=models.DO_NOTHING)
  arg1 = models.ForeignKey("self", db_column="arg1", related_name="+",
      null=True, on_delete=models.DO_NOTHING)
  arg2 = models.ForeignKey("self", db_column="arg2", related_name="+",
      null=True, on_delete=models.DO_NOTHING)
  # unused fields
  expressionGroupID = models.ForeignKey("inv.Group",
      db_column="expressionGroupID", null=True, on_delete=models.DO_NOTHING)
  expressionTypeID = models.ForeignKey("inv.Item",
      db_column="expressionTypeID", null=True, on_delete=models.DO_NOTHING)


class Modifier(models.Model):
  modifierID = models.IntegerField(primary_key=True)
  state = models.IntegerField()
  context = models.IntegerField()
  sourceAttributeID = models.IntegerField()
  targetAttributeID = models.IntegerField()
  operator = models.IntegerField()
  location = models.IntegerField()
  filterType = models.IntegerField(null=True)
  filterValue = models.IntegerField(null=True)


class Effect(models.Model):
  effectID = models.IntegerField(primary_key=True)
  effectName = models.CharField(max_length=100)
  preExpression = models.ForeignKey(Expression, db_column="preExpression",
      related_name="+", null=True, on_delete=models.DO_NOTHING)
  postExpression = models.ForeignKey(Expression, db_column="postExpression",
      related_name="+", null=True, on_delete=models.DO_NOTHING)
  description = models.CharField(max_length=1000, null=True)
  isOffensive = models.BooleanField()
  isAssistance = models.BooleanField()
  durationAttributeID = models.ForeignKey(Attribute,
      db_column="durationAttributeID", related_name="+", null=True,
      on_delete=models.DO_NOTHING)
  trackingSpeedAttributeID = models.ForeignKey(Attribute,
      db_column="trackingSpeedAttributeID", related_name="+", null=True,
      on_delete=models.DO_NOTHING)
  dischargeAttributeID = models.ForeignKey(Attribute,
      db_column="dischargeAttributeID", related_name="+", null=True,
      on_delete=models.DO_NOTHING)
  rangeAttributeID = models.ForeignKey(Attribute, db_column="rangeAttributeID",
      related_name="+", null=True, on_delete=models.DO_NOTHING)
  falloffAttributeID = models.ForeignKey(Attribute,
      db_column="falloffAttributeID", related_name="+", null=True,
      on_delete=models.DO_NOTHING)
  disallowAutoRepeat = models.NullBooleanField()
  published = models.SmallIntegerField()
  displayName = models.CharField(max_length=100)
  # unused fields
  effectCategory = models.SmallIntegerField(null=True)
  displayNameID = models.IntegerField(null=True)
  descriptionID = models.IntegerField(null=True)
  guid = models.CharField(max_length=60, null=True)
  iconID = models.IntegerField(null=True)
  dataID = models.IntegerField(null=True)
  isWarpSafe = models.NullBooleanField()
  rangeChance = models.NullBooleanField()
  electronicChance = models.NullBooleanField()
  propulsionChance = models.NullBooleanField()
  distribution = models.SmallIntegerField(null=True)
  sfxName = models.CharField(max_length=20, null=True)
  npcUsageChanceAttributeID = models.SmallIntegerField(null=True)
  npcActivationChanceAttributeID = models.SmallIntegerField(null=True)
  fittingUsageChanceAttributeID = models.SmallIntegerField(null=True)

  buildStatus = models.IntegerField(null=True)
  modifiers = models.ManyToManyField(Modifier, through="EffectModifiers")

  def __str__(self):
    return self.preExpression.expressionName


class TypeEffects(models.Model):
  typeID = models.ForeignKey("inv.Item", db_column="typeID")
  effectID = models.ForeignKey(Effect, db_column="effectID")
  isDefault = models.BooleanField()


class EffectModifiers(models.Model):
  effectID = models.ForeignKey(Effect, on_delete=models.DO_NOTHING)
  modifierID = models.ForeignKey(Modifier, on_delete=models.DO_NOTHING)

