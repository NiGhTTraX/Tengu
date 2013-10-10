from inv.models import Item, Group
from dogma.models import Attribute, TypeAttributes, Effect, TypeEffects, Expression
from cache.models import Metadata

from eos.data.dataHandler import DataHandler


class DjangoDataHandler(DataHandler):

  def getInvtypes(self):
    return Item.objects.values("typeID", "groupID", "mass", "volume",
        "capacity", "radius", "marketGroupID", "published")

  def getInvgroups(self):
    return Group.objects.values("groupID", "categoryID", "fittableNonSingleton",
        "published")

  def getDgmattribs(self):
    return Attribute.objects.values("attributeID", "defaultValue", "stackable",
        "highIsGood", "maxAttributeID", "categoryID", "published")

  def getDgmtypeattribs(self):
    return TypeAttributes.objects.values("typeID", "attributeID", "value")

  def getDgmeffects(self):
    return Effect.objects.values("effectID", "isOffensive", "isAssistance",
        "durationAttributeID", "trackingSpeedAttributeID",
        "dischargeAttributeID", "rangeAttributeID", "falloffAttributeID",
        "effectCategory", "fittingUsageChanceAttributeID", "preExpression",
        "postExpression", "published")

  def getDgmtypeeffects(self):
    return TypeEffects.objects.values("typeID", "effectID", "isDefault")

  def getDgmexpressions(self):
    return Expression.objects.values("expressionID", "expressionValue",
        "operandID", "arg1", "arg2", "expressionGroupID", "expressionTypeID",
        "expressionAttributeID")

  def getVersion(self):
    try:
      version = Metadata.objects.get(fieldName="clientBuild").fieldValue
    except Metadata.DoesNotExist:
      return None

    return version

