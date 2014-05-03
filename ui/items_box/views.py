from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.core.cache import cache

from inv.models import MarketGroup, Item
from ui.items_box.utils import getCPUandPGandSlot

from inv.const import CATEGORIES_ITEMS

import json
import hashlib


