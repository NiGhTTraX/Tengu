from utils.test import SeleniumTestCase

from inv.models import Item, MarketGroup
from inv.const import MARKET_GROUP_SHIPS, CATEGORIES_SHIPS


class TestMarketTree(SeleniumTestCase):

  def setUp(self):
    # Create some items and groups.
    MarketGroup.objects.create(pk=1, marketGroupName="group1",
        parentGroupID_id=4)
    MarketGroup.objects.create(pk=2, marketGroupName="group2",
        parentGroupID_id=1)
    Item.objects.create(pk=1, typeName="item1", marketGroupID_id=2,
        categoryID_id=6, published=True)
    Item.objects.create(pk=2, typeName="item2", marketGroupID_id=2,
        categoryID_id=6, published=True)

    # Clear cookies.
    self.driver.delete_all_cookies()

    # Go to the home page.
    self.driver.get(self.live_server_url)

    # Store some commonly used elements.
    self.mg1 = self.driver.find_element_by_id("mg1")
    self.mg2 = self.driver.find_element_by_id("mg2")
    self.sh1 = self.driver.find_element_by_id("sh1")
    self.search_box = self.driver.find_element_by_id("search-items")
    self.items_box = self.driver.find_element_by_id("items-box")
    self.tab_ships = self.driver.find_element_by_id("tab-ships")
    self.tab_items = self.driver.find_element_by_id("tab-items")

  def test_expand_and_collapse_groups(self):
    # Check that everything except the root group is hidden.
    self.assertFalse(self.mg2.is_displayed())
    self.assertFalse(self.sh1.is_displayed())

    # Expand a market group.
    self.mg1.click()

    # The child group should now be visible.
    self.assertTrue(self.mg2.is_displayed())
    self.assertFalse(self.sh1.is_displayed())

    # Expand the child group.
    self.mg2.click()

    # Items should now be visible.
    self.assertTrue(self.sh1.is_displayed())

    # Collapse the root group.
    self.mg1.click()

    # Everything else should now be hidden.
    self.assertFalse(self.mg2.is_displayed())
    self.assertFalse(self.sh1.is_displayed())

    # Expand the parent group again.
    self.mg1.click()

    # Child group should remain collapsed.
    self.assertTrue(self.mg2.is_displayed())
    self.assertFalse(self.sh1.is_displayed())

  def test_persistent_tree(self):
    # Expand the root group.
    self.mg1.click()

    # Refresh the page.
    self.driver.refresh()
    self.mg1 = self.driver.find_element_by_id("mg1")
    self.mg2 = self.driver.find_element_by_id("mg2")
    self.sh1 = self.driver.find_element_by_id("sh1")

    # Tree should be persistent.
    self.assertTrue(self.mg2.is_displayed())
    self.assertFalse(self.sh1.is_displayed())

    # Expand the child group.
    self.mg2.click()

    # Refresh the page
    self.driver.refresh()
    self.mg1 = self.driver.find_element_by_id("mg1")
    self.mg2 = self.driver.find_element_by_id("mg2")
    self.sh1 = self.driver.find_element_by_id("sh1")

    # Tree should be persistent.
    self.assertTrue(self.mg2.is_displayed())
    self.assertTrue(self.sh1.is_displayed())

  def test_selected(self):
    # Expand the groups and select the item.
    self.mg1.click()
    self.mg2.click()
    self.sh1.click()

    # Check if it was selected.
    self.assertTrue("selected" in self.sh1.get_attribute("class"))

    # Collapse everything.
    self.mg1.click()

    # Check that the item is still selected.
    self.assertTrue("selected" in self.sh1.get_attribute("class"))

