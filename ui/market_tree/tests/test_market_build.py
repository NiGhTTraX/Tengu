from django.core.cache import cache
from django.test import TestCase

from inv.models import MarketGroup, Item
from ui.market_tree.utils import MarketTree


class MarketTreeBuilderTest(TestCase):
  def setUp(self):
    self.dummyGroup = MarketGroup(pk=1)
    self.dummyItem = Item(pk=1, typeName="dummy", published=True)

    cache.clear()

  def test_simple_group(self):
    """One parent group with 2 subgroups."""
    parentGroup = self.dummyGroup
    parentGroup.save()
    expected = []

    childGroup1 = MarketGroup.objects.all()[0]
    childGroup1.pk = 2
    childGroup1.parentGroupID = parentGroup
    childGroup1.save()

    childGroup2 = MarketGroup.objects.all()[0]
    childGroup2.pk = 3
    childGroup2.parentGroupID = parentGroup
    childGroup2.save()

    expected.append((MarketTree.GROUP, 0, parentGroup, True))
    expected.append((MarketTree.INCREASE_INDENT, 1, parentGroup.pk))
    expected.append((MarketTree.GROUP, 1, childGroup1, False))
    expected.append((MarketTree.GROUP, 1, childGroup2, False))
    expected.append((MarketTree.DECREASE_INDENT, 0, 0))

    actual = MarketTree(parentGroup).build()
    self.assertEqual(expected, actual)

  def test_lots_of_subgroups(self):
    """One parent group with 100 subgroups."""
    parentGroup = self.dummyGroup
    parentGroup.save()
    expected = []

    expected.append((MarketTree.GROUP, 0, parentGroup, True))
    expected.append((MarketTree.INCREASE_INDENT, 1, parentGroup.pk))

    for i in range(100):
      childGroup = MarketGroup.objects.all()[0]
      childGroup.pk = i + 2
      childGroup.parentGroupID = parentGroup
      childGroup.save()
      expected.append((MarketTree.GROUP, 1, childGroup, False))

    expected.append((MarketTree.DECREASE_INDENT, 0, 0))

    actual = MarketTree(parentGroup).build()
    self.assertEqual(expected, actual)

  def test_multiple_levels(self):
    """One parent group with 10 nested subgroups."""
    parentGroup = self.dummyGroup
    parentGroup.save()
    expected = []

    expected.append((MarketTree.GROUP, 0, parentGroup, True))
    expected.append((MarketTree.INCREASE_INDENT, 1, parentGroup.pk))

    # Insert 9 nested subgroups.
    for i in range(9):
      childGroup = MarketGroup.objects.all()[i]
      childGroup.pk = i + 2
      childGroup.parentGroupID = MarketGroup.objects.all()[i]
      childGroup.save()
      expected.append((MarketTree.GROUP, i + 1, childGroup, True))
      expected.append((MarketTree.INCREASE_INDENT, i + 2, childGroup.pk))

    # Insert the last subgroup on level 10.
    childGroup = MarketGroup.objects.all()[9]
    childGroup.pk = 11
    childGroup.parentGroupID = MarketGroup.objects.all()[9]
    childGroup.save()
    expected.append((MarketTree.GROUP, 10, childGroup, False))

    # End all the subgroups, except the last which has no children.
    for i in range(9):
      expected.append((MarketTree.DECREASE_INDENT, 0, 0))
    # End the parent.
    expected.append((MarketTree.DECREASE_INDENT, 0, 0))

    actual = MarketTree(parentGroup).build()
    self.assertEqual(expected, actual)

  def test_include_items_simple(self):
    """One parent group with 1 item."""
    parentGroup = self.dummyGroup
    parentGroup.save()

    item = self.dummyItem
    item.marketGroupID = parentGroup
    item.save()

    expected = []
    expected.append((MarketTree.GROUP, 0, parentGroup, True))
    expected.append((MarketTree.INCREASE_INDENT, 1, parentGroup.pk))
    expected.append((MarketTree.ITEM, 1, item))
    expected.append((MarketTree.DECREASE_INDENT, 0, 0))

    actual = MarketTree(parentGroup, True).build()
    self.assertEqual(expected, actual)

  def test_include_items_complex(self):
    """One parent group with no items and one subgroup with 1 item."""
    parentGroup = self.dummyGroup
    parentGroup.save()

    childGroup = MarketGroup.objects.all()[0]
    childGroup.pk = 2
    childGroup.parentGroupID = parentGroup
    childGroup.save()

    item = self.dummyItem
    item.marketGroupID = childGroup
    item.save()

    expected = []
    expected.append((MarketTree.GROUP, 0, parentGroup, True))
    expected.append((MarketTree.INCREASE_INDENT, 1, parentGroup.pk))
    expected.append((MarketTree.GROUP, 1, childGroup, True))
    expected.append((MarketTree.INCREASE_INDENT, 2, childGroup.pk))
    expected.append((MarketTree.ITEM, 2, item))
    expected.append((MarketTree.DECREASE_INDENT, 0, 0))
    expected.append((MarketTree.DECREASE_INDENT, 0, 0))

    actual = MarketTree(parentGroup, True).build()
    self.assertEqual(expected, actual)

