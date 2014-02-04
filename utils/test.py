from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SeleniumTestCase(LiveServerTestCase):
  @classmethod
  def setUpClass(cls):
    cls.driver = webdriver.PhantomJS()
    cls.actionChains = webdriver.ActionChains(cls.driver)
    super(SeleniumTestCase, cls).setUpClass()

  @classmethod
  def tearDownClass(cls):
    cls.driver.quit()
    super(SeleniumTestCase, cls).tearDownClass()

  @classmethod
  def waitFor(cls, locator, msg="Timed out", timeout=2):
    WebDriverWait(cls.driver, timeout).until(EC.presence_of_element_located(
        (By.ID, locator)), msg)

