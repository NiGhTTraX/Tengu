from django.core.cache import cache

# Since some of the Django models have the same name as the Eos models, we'll
# import them under different names.
from inv.models import Item
from dogma.models import TypeAttributes, TypeEffects, EffectModifiers
from dogma.models import Attribute as DjangoAttribute
from dogma.models import Effect as DjangoEffect
from dogma.models import Modifier as DjangoModifier
from cache.models import Metadata

from eos.data.cache.handler import CacheHandler
from eos.data.cache.object import *
from eos.data.cache.handler.exception import TypeFetchError, AttributeFetchError, EffectFetchError, ModifierFetchError

from math import ceil
import itertools


class DjangoCacheHandler(CacheHandler):
  """Django cache handler.

  If the requested data is in the cache, return it directly. Otherwise, fetch it
  from the database, constructing it if neccessary, and then store it in the
  cache for future requests.

  You should take caution when calling the cache constructor. This process is
  not atomic, so calling it multiple times might result in errors such as
  primary key duplication and the like. Make sure you only run the process once,
  preferably before deployment.

  Some tables (such as the modifiers table) should be cleared before the cache
  generator runs.
  """

  def __init__(self, verbose=True):
    self.verbose = verbose

  def __printStatus(self, prefix, current, total):
    """Prints out a real time progress bar.

    Args:
      prefix: A string that will precede the progress bar.
      current: Current progress.
      total: Total progress.
    """
    BAR_LENGTH = 80 - len(prefix) - 9
    progress = (current + 1) / total
    complete = ceil(BAR_LENGTH * progress)
    left = BAR_LENGTH - complete

    done = "#" * complete
    todo = "-" * left
    s = "{0}: <{1}{2}> {3}%".format(prefix, done, todo, ceil(progress * 100))

    if current == total - 1:
      s += "\n"
    if current:
      s = "\r" + s

    print(s, end="")

  def getType(self, typeID):
    type_ = cache.get("type_%d" % typeID)

    if type_ is None:
      # Item wasn't in cache, let's retrieve it and store it there.
      try:
        item = Item.objects.get(pk=typeID)
      except Item.DoesNotExist as e:
        raise TypeFetchError(typeID) from e

      effs = item.effects.all().values_list("effectID", flat=True)
      effects = tuple(self.getEffect(effectID) for effectID in effs)

      attribs = TypeAttributes.objects.filter(typeID = typeID).values(
          "attributeID", "value")
      attributes = {a["attributeID"]: a["value"] for a in attribs}

      type_ = Type(typeId=typeID,
                   groupId=item.groupID_id,  # to save a query
                   categoryId=item.categoryID_id,  # to save query
                   durationAttributeId=item.durationAttributeID,
                   dischargeAttributeId=item.dischargeAttributeID,
                   rangeAttributeId=item.rangeAttributeID,
                   falloffAttributeId=item.falloffAttributeID,
                   trackingSpeedAttributeId=item.trackingSpeedAttributeID,
                   fittableNonSingleton=item.fittableNonSingleton,
                   attributes=attributes,
                   effects=effects)

      # Store it in cache.
      cache.set("type_%d" % typeID, type_)

    return type_

  def getAttribute(self, attrID):
    attribute = cache.get("attribute_%d" % attrID)

    if attribute is None:
      # Attribute wasn't in cache, let's retrieve it and store it there.
      try:
        attribute = DjangoAttribute.objects.get(pk = attrID)
      except DjangoAttribute.DoesNotExist as e:
        raise AttributeFetchError(attrID) from e

      attribute = Attribute(attributeId=attrID,
                            maxAttributeId=attribute.maxAttributeID,
                            defaultValue=attribute.defaultValue,
                            highIsGood=attribute.highIsGood,
                            stackable=attribute.stackable)

      # Store it in cache.
      cache.set("attribute_%d" % attrID, attribute)

    return attribute

  def getEffect(self, effectID):
    effect = cache.get("effect_%d" % effectID)

    if effect is None:
      # Effect wasn't in cache, let's retrieve it and store it there.
      try:
        effect = DjangoEffect.objects.get(pk = effectID)
      except DjangoEffect.DoesNotExist as e:
        raise EffectFetchError(effectID) from e

      modifs = effect.modifiers.all().values_list("modifierID", flat=True)
      modifiers = tuple(self.getModifier(modifierID) for modifierID in modifs)

      effect = Effect(effectId=effectID,
                      categoryId=effect.effectCategory,
                      isOffensive=effect.isOffensive,
                      isAssistance=effect.isAssistance,
                      fittingUsageChanceAttributeId=effect.fittingUsageChanceAttributeID,
                      buildStatus=effect.buildStatus,
                      modifiers=modifiers)

      # Store it in cache.
      cache.set("effect_%d" % effectID, effect)

    return effect

  def getModifier(self, modifierID):
    modifier = cache.get("modifier_%d" % modifierID)

    if modifier is None:
      # Effect wasn't in cache, let's retrieve it and store it there.
      try:
        modif = DjangoModifier.objects.get(pk = modifierID)
      except DjangoModifier.DoesNotExist as e:
        raise ModifierFetchError(modifierID) from e

      modifier = Modifier(modifierId=modifierID,
                          state=modif.state,
                          context=modif.context,
                          sourceAttributeId=modif.sourceAttributeID,
                          operator=modif.operator,
                          targetAttributeId=modif.targetAttributeID,
                          location=modif.location,
                          filterType=modif.filterType,
                          filterValue=modif.filterValue)

      # Store it in cache.
      cache.set("modifier_%d" % modifierID, modifier)

    return modifier

  def getFingerprint(self):
    """Get memory cache fingerprint."""
    fingerprint = cache.get("fingerprint")

    if fingerprint is None:
      # Fingerprint wasn't in cache, let's retrieve it and store it there.
      try:
        fingerprint = Metadata.objects.get(fieldName="fingerprint").fieldValue
      except Metadata.DoesNotExist:
        return None

      # Store it in cache.
      cache.set("fingerprint", fingerprint)

    return fingerprint

  def __updateItems(self, data, verbose):
    """Updates the items cache."""

    # Get all the items from the database.
    # Use prefetch_related to only do 2 queries for fetching the effects and
    # attributes.
    items = Item.objects.prefetch_related("effects", "attributes").in_bulk(
        [typeRow["typeId"] for typeRow in data])

    typeeffects = []
    typeattributes = []

    k = len(data)
    for i, typeRow in enumerate(data):
      if verbose:
        self.__printStatus("items", i, k)

      typeID = typeRow["typeId"]
      effects = tuple(self.getEffect(effID) for effID in typeRow["effects"])

      # Update the database.
      item = items[typeID]
      item.categoryID_id = typeRow["categoryId"]  # to save a query
      item.durationAttributeID = typeRow["durationAttributeId"]
      item.dischargeAttributeID = typeRow["dischargeAttributeId"]
      item.rangeAttributeID = typeRow["rangeAttributeId"]
      item.falloffAttributeID = typeRow["falloffAttributeId"]
      item.trackingSpeedAttributeID = typeRow["trackingSpeedAttributeId"]
      item.fittableNonSingleton = typeRow["fittableNonSingleton"]
      item.save()

      # Add any new effects that were created by Eos.
      newEffects = set(typeRow["effects"])
      newEffects.difference_update(set([e.effectID for e in item.effects.all()]))

      typeeffects.append(
          [TypeEffects(typeID_id=typeID, effectID_id=effectID, isDefault=False)
              for effectID in newEffects])

      # Add any new attributes that were created by Eos.
      # There should always be at least 3 new attributes (mass, volume, radius).
      existingAttributes = {a.attributeID: True for a in item.attributes.all()}

      typeattributes.append(
          [TypeAttributes(typeID_id=typeID, attributeID_id=attributeID, value=value)
              for attributeID, value in typeRow["attributes"].items() if attributeID not in existingAttributes])

      # Construct the Type object and store it in cache.
      type_ = Type(typeId=typeID,
                   groupId=typeRow["groupId"],
                   categoryId=typeRow["categoryId"],
                   durationAttributeId=typeRow["durationAttributeId"],
                   dischargeAttributeId=typeRow["dischargeAttributeId"],
                   rangeAttributeId=typeRow["rangeAttributeId"],
                   falloffAttributeId=typeRow["falloffAttributeId"],
                   trackingSpeedAttributeId=typeRow["trackingSpeedAttributeId"],
                   fittableNonSingleton=typeRow["fittableNonSingleton"],
                   attributes=typeRow["attributes"],
                   effects=effects)
      cache.set("type_%d" % typeID, type_)

    # Do bulk inserts for type effects and attributes.
    TypeEffects.objects.bulk_create(itertools.chain.from_iterable(typeeffects))
    TypeAttributes.objects.bulk_create(itertools.chain.from_iterable(typeattributes))

  def __updateAttributes(self, data, verbose):
    """Updates the attributes cache."""
    k = len(data)
    for i, attrRow in enumerate(data):
      if verbose:
        self.__printStatus("attributes", i, k)

      attributeID = attrRow["attributeId"]

      # Create the Attribute object and store it in cache.
      attribute = Attribute(attributeId=attributeID,
                            maxAttributeId=attrRow["maxAttributeId"],
                            defaultValue=attrRow["defaultValue"],
                            highIsGood=attrRow["highIsGood"],
                            stackable=attrRow["stackable"])
      cache.set("attribute_%d" % attributeID, attribute)

  def __updateEffects(self, data, verbose):
    """Updates the effects cache.

    This makes the assumption that any effect present in the database has not
    had its modifiers constructed. This allows adding the list of modifiers to
    the corresponding field directly. If there were any modifiers already there,
    then we would possibly add duplicates.

    Using the above asumption we can save a query by not having to clear the
    list of modifiers for each effect.
    """
    # Get all the effects in one query.
    effects = DjangoEffect.objects.in_bulk([effectRow["effectId"] for effectRow in data])
    effectmodifiers = []
    k = len(data)

    for i, effectRow in enumerate(data):
      if verbose:
        self.__printStatus("effects", i, k)

      effectID = effectRow["effectId"]

      modifiers = tuple(self.getModifier(modifierID) for modifierID in effectRow["modifiers"])

      # Update the database.
      try:
        eff = effects[effectID]
      except KeyError:
        # This is a new effect created by Eos, so let's store it.
        eff = DjangoEffect()
        eff.pk = effectID
        eff.categoryID = effectRow["effectCategory"]
        eff.isOffensive = effectRow["isOffensive"]
        eff.isAssistance = effectRow["isAssistance"]
        eff.fittingUsageChanceAttributeID = effectRow["fittingUsageChanceAttributeId"]
        eff.published = True

      eff.buildStatus = effectRow["buildStatus"]
      eff.save()

      effectmodifiers.append(
          [EffectModifiers(effectID_id=effectID, modifierID_id=modifierID)
              for modifierID in effectRow["modifiers"]])

      # Construct the Effect object and store it in cache.
      effect = Effect(effectId=effectID,
                      categoryId=effectRow["effectCategory"],
                      isOffensive=effectRow["isOffensive"],
                      isAssistance=effectRow["isAssistance"],
                      fittingUsageChanceAttributeId=effectRow["fittingUsageChanceAttributeId"],
                      buildStatus=effectRow["buildStatus"],
                      modifiers=modifiers)
      cache.set("effect_%d" % effectID, effect)

    # Do a bulk insert for effect modifiers.
    EffectModifiers.objects.bulk_create(itertools.chain.from_iterable(
        effectmodifiers))

  def __updateModifiers(self, data, verbose):
    """Updates the modifiers cache.

    This assumes that the modifiers table is empty. Otherwise, we would get
    primary key duplicates.

    Using the above assumption we can skip clearing the table before starting
    the update. That would've proven a difficulty if using sqlite3, since due to
    a Django bug, you can't delete more than 999 objects at a time.
    """
    modifs = []
    k = len(data)

    for i, modifierRow in enumerate(data):
      if verbose:
        self.__printStatus("modifiers", i, k)

      modifierID = modifierRow["modifierId"]

      modifier = DjangoModifier(modifierID=modifierID,
                                state=modifierRow["state"],
                                context=modifierRow["context"],
                                sourceAttributeID=modifierRow["sourceAttributeId"],
                                operator=modifierRow["operator"],
                                targetAttributeID=modifierRow["targetAttributeId"],
                                location=modifierRow["location"],
                                filterType=modifierRow["filterType"],
                                filterValue=modifierRow["filterValue"])
      modifs.append(modifier)


      # Construct the Modifier object and store it in cache.
      modifier = Modifier(modifierId=modifierID,
                          state=modifierRow["state"],
                          context=modifierRow["context"],
                          sourceAttributeId=modifierRow["sourceAttributeId"],
                          operator=modifierRow["operator"],
                          targetAttributeId=modifierRow["targetAttributeId"],
                          location=modifierRow["location"],
                          filterType=modifierRow["filterType"],
                          filterValue=modifierRow["filterValue"])
      cache.set("modifier_%d" % modifierID, modifier)

    # Do a bulk insert into the database.
    DjangoModifier.objects.bulk_create(modifs)

  def updateCache(self, data, fingerprint):
    """Updates database and memory caches.

    Since Eos takes its data directly from the database and then transforms it,
    we'll update the database to contain the new information, while also storing
    it in the cache.

    Args:
      data: Dictionary with data to update.
      fingerprint: String with fingerprint.
    """
    # Clear the cache.
    cache.clear()

    # Then update it.
    # Order of calls is important.
    self.__updateModifiers(data["modifiers"], self.verbose)
    self.__updateAttributes(data["attributes"], self.verbose)
    self.__updateEffects(data["effects"], self.verbose)
    self.__updateItems(data["types"], self.verbose)

    # Update the fingerprint.
    Metadata(fieldName="fingerprint", fieldValue=fingerprint).save()
    cache.set("fingerprint", fingerprint)

