from utils.test import SeleniumTestCase

from inv.models import Item, MarketGroup
from inv.const import MARKET_GROUP_SHIPS, CATEGORIES_SHIPS


class TestMarketHeader(SeleniumTestCase):

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

  def test_switch_tabs(self):
    # Check that the current tab is the ships tab.
    self.assertTrue("current-tab" in self.tab_ships.get_attribute("class"))
    self.assertFalse("current-tab" in self.tab_items.get_attribute("class"))

    # Items box should be empty.
    self.assertFalse(self.items_box.text.strip())

    # Switch to the items tab.
    self.tab_items.click()

    # Check that the current tab has been switched.
    self.assertFalse("current-tab" in self.tab_ships.get_attribute("class"))
    self.assertTrue("current-tab" in self.tab_items.get_attribute("class"))

    # Items box should still be empty.
    self.assertFalse(self.items_box.text.strip())

    # Now switch back.
    self.tab_ships.click()
    self.assertTrue("current-tab" in self.tab_ships.get_attribute("class"))
    self.assertFalse("current-tab" in self.tab_items.get_attribute("class"))

    # Load some content by clicking an item.
    self.mg1.click()
    self.mg2.click()
    self.sh1.click()
    self.waitFor("fits", "Load fits timed out")
    #WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
    #    (By.ID, "fits")), "Load fits timed out")
    content = self.items_box.text.strip()
    self.assertTrue(content)

    # Switch tabs.
    self.tab_items.click()

    # Items box should now be empty.
    self.assertFalse(self.items_box.text.strip())

    # Switch back.
    self.tab_ships.click()

    # Items box should be restored.
    self.assertEqual(self.items_box.text.strip(), content)

  def test_search(self):
    self.search_box.send_keys("item")
    self.waitFor("fits", "Search timed out")
    #WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
    #    (By.ID, "fits")), "Search timed out")
    self.assertTrue("item1" in self.items_box.text)

