from selenose.cases import LiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from inv.models import Item, MarketGroup
from inv.const import MARKET_GROUP_SHIPS, CATEGORIES_SHIPS

import time


class TestResizeHandle(LiveServerTestCase):

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
    self.leftSidebar = self.driver.find_element_by_id("left-sidebar")
    self.leftTop = self.driver.find_element_by_id("left-sidebar-top")
    self.leftBottom = self.driver.find_element_by_id("left-sidebar-bottom")
    self.resizeHandle = self.driver.find_element_by_id("resize-handle")

    self.actionChains = ActionChains(self.driver)

  def test_initial_position(self):
    from math import floor
    leftSidebarHeight = int(self.leftSidebar.value_of_css_property("height")[:-2])
    top = self.resizeHandle.value_of_css_property("top")

    self.assertEqual(top, "%dpx" % floor(leftSidebarHeight / 2))

  def test_restore_handle_position(self):
    width = 800
    height = 600

    self.driver.set_window_size(width, height)

    oldTop = self.resizeHandle.value_of_css_property("top")
    oldWindow = self.driver.get_window_size()

    self.driver.set_window_size(oldWindow["width"], oldWindow["height"] - 100)
    time.sleep(0.1)
    self.driver.set_window_size(oldWindow["width"], oldWindow["height"])

    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     oldTop)

    self.driver.set_window_size(oldWindow["width"], oldWindow["height"] + 100)
    time.sleep(0.1)
    self.driver.set_window_size(oldWindow["width"], oldWindow["height"])

    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     oldTop)

  def test_resize_window(self):
    width = 800
    height = 500

    self.driver.set_window_size(width, height)
    time.sleep(0.1)
    oldTop = int(self.resizeHandle.value_of_css_property("top")[:-2])

    self.driver.set_window_size(width, height + 100)
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % (oldTop + 50))

    self.driver.set_window_size(width, height + 150)
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % (oldTop + 75))

    self.driver.set_window_size(width, height - 100)
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % (oldTop - 50))

    self.driver.set_window_size(width, height - 150)
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % (oldTop - 75))

    self.driver.set_window_size(width, height)
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % oldTop)

  def test_resize_stress(self):
    width = 800
    height = 600
    TEST_RANGE = 10
    offset = 10

    self.driver.set_window_size(width, height)
    oldTop = self.resizeHandle.value_of_css_property("top")

    for i in range(TEST_RANGE):
      offset = -offset
      self.driver.set_window_size(width, height + offset)
      time.sleep(0.1)

    self.driver.set_window_size(width, height)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     oldTop)

  def test_left_sidebar_heights_on_init(self):
    handlerHeight = int(self.resizeHandle.value_of_css_property("height")[:-2])
    topHeight = int(self.leftTop.value_of_css_property("height")[:-2])
    bottomHeight = int(self.leftBottom.value_of_css_property("height")[:-2])
    sidebarHeight = int(self.leftSidebar.value_of_css_property("height")[:-2])

    self.assertEqual(sidebarHeight, topHeight + bottomHeight + handlerHeight)

  def test_left_sidebar_heights_on_window_resize(self):
    width = 800
    height = 600

    self.driver.set_window_size(width, height)
    handlerHeight = int(self.resizeHandle.value_of_css_property("height")[:-2])
    topHeight = int(self.leftTop.value_of_css_property("height")[:-2])
    bottomHeight = int(self.leftBottom.value_of_css_property("height")[:-2])
    sidebarHeight = int(self.leftSidebar.value_of_css_property("height")[:-2])

    self.assertEqual(sidebarHeight, topHeight + bottomHeight + handlerHeight)

  def test_persistent_resize_handle_position(self):
    width = 800
    height = 600

    self.driver.set_window_size(width, height)
    oldTop = self.resizeHandle.value_of_css_property("top")

    self.driver.refresh()
    self.resizeHandle = self.driver.find_element_by_id("resize-handle")
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     oldTop)

  def test_top_limit_on_window_resize(self):
    width = 800
    height = 600

    self.driver.set_window_size(width, height)
    topLimit = int(self.driver.execute_script("return resizeHandleTopLimit;"))

    # For some reason, this may hang on Chrome.
    #self.actionChains.drag_and_drop_by_offset(self.resizeHandle, 0, -100).perform()
    time.sleep(0.1)
    # Make the window small enough so the resize handle reaches its limit.
    self.driver.set_window_size(width, 200)
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % topLimit)

  def test_containment(self):
    width = 800
    height = 600

    self.driver.set_window_size(width, height)
    topLimit = int(self.driver.execute_script("return resizeHandleTopLimit"))
    bottomLimit = int(self.driver.execute_script("return leftSidebar.height() - "
        "resizeHandle.outerHeight(true);")) - 1

    self.actionChains.drag_and_drop_by_offset(self.resizeHandle, 0, -500).perform()
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % topLimit)

    self.actionChains.drag_and_drop_by_offset(self.resizeHandle, 0, 500).perform()
    time.sleep(0.1)
    self.assertEqual(self.resizeHandle.value_of_css_property("top"),
                     "%dpx" % bottomLimit)

