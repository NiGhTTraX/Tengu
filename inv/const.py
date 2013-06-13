# Inventory constants.
from inv.models import MarketGroup


MARKET_GROUPS_ITEMS = [
    11,     # Ammunition and Charges
    157,    # Drones
    24,     # Implants and Boosters
    9,      # Ship Equipment
    955     # Ship Modifications
]
MARKET_GROUP_SHIPS = 4
MARKET_GROUPS_SHIPS = MarketGroup.objects.filter(
    parentGroupID = MARKET_GROUP_SHIPS).order_by("marketGroupName").values_list(
        "marketGroupID", flat=True)

CATEGORIES_ITEMS = [
    7,      # Modules
    8,      # Charges
    18,     # Drones
    20,     # Implants
    32      # Subsystems
]
CATEGORIES_SHIPS = [6]

