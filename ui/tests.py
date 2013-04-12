from django.test import TestCase
from inv.models import MarketGroup
from ui.utils import buildMarketTree


class MarketTreeBuilderTest(TestCase):
  def setUp(self):
    self.dummyGroup = MarketGroup(pk=None)

  def test_simple_group(self):
    """One parent group with 2 subgroups."""
    parentGroup = self.dummyGroup
    parentGroup.save()
    expected = []

    childGroup1 = MarketGroup.objects.all()[0]
    childGroup1.pk = None
    childGroup1.parentGroupID = parentGroup
    childGroup1.save()

    childGroup2 = MarketGroup.objects.all()[0]
    childGroup2.pk = None
    childGroup2.parentGroupID = parentGroup
    childGroup2.save()

    expected.append((0, 0, parentGroup, True))
    expected.append((1, 1, parentGroup.pk))
    expected.append((0, 1, childGroup1, False))
    expected.append((0, 1, childGroup2, False))
    expected.append((-1, 0, 0))

    actual = buildMarketTree(parentGroup)
    self.assertEqual(expected, actual)

  def test_lots_of_subgroups(self):
    """One parent group with 100 subgroups."""
    parentGroup = self.dummyGroup
    parentGroup.save()
    expected = []

    expected.append((0, 0, parentGroup, True))
    expected.append((1, 1, parentGroup.pk))

    for i in xrange(100):
      childGroup = MarketGroup.objects.all()[0]
      childGroup.pk = None
      childGroup.parentGroupID = parentGroup
      childGroup.save()
      expected.append((0, 1, childGroup, False))

    expected.append((-1, 0, 0))

    actual = buildMarketTree(parentGroup)
    self.assertEqual(expected, actual)

  def test_multiple_levels(self):
    """One parent group with 10 nested subgroups."""
    parentGroup = self.dummyGroup
    parentGroup.save()
    expected = []

    expected.append((0, 0, parentGroup, True))
    expected.append((1, 1, parentGroup.pk))

    # Insert 9 nested subgroups.
    for i in xrange(9):
      childGroup = MarketGroup.objects.all()[i]
      childGroup.pk = None
      childGroup.parentGroupID = MarketGroup.objects.all()[i]
      childGroup.save()
      expected.append((0, i + 1, childGroup, True))
      expected.append((1, i + 2, childGroup.pk))

    # Insert the last subgroup on level 10.
    childGroup = MarketGroup.objects.all()[9]
    childGroup.pk = None
    childGroup.parentGroupID = MarketGroup.objects.all()[9]
    childGroup.save()
    expected.append((0, 10, childGroup, False))

    # End all the subgroups, except the last which has no children.
    for i in xrange(9):
      expected.append((-1, 0, 0))
    # End the parent.
    expected.append((-1, 0, 0))

    actual = buildMarketTree(parentGroup)
    self.assertEqual(expected, actual)

