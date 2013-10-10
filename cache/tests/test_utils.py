from django.test import TransactionTestCase
from cache.utils import disableSynchronous
from django.db import connection


class TestDisableSynchronous(TransactionTestCase):
  def test_disable(self):
    c = connection.cursor()

    disableSynchronous.disable()
    currentState = c.execute("PRAGMA synchronous;").fetchone()

    self.assertEqual(currentState, (0,))

  def test_restore(self):
    c = connection.cursor()

    oldState = c.execute("PRAGMA synchronous;").fetchone()
    disableSynchronous.disable()
    disableSynchronous.restore()
    currentState = c.execute("PRAGMA synchronous;").fetchone()

    self.assertEqual(currentState, oldState)

  def test_with(self):
    c = connection.cursor()

    oldState = c.execute("PRAGMA synchronous;").fetchone()

    with disableSynchronous():
      currentState = c.execute("PRAGMA synchronous;").fetchone()
      self.assertEqual(currentState, (0,))

    currentState = c.execute("PRAGMA synchronous;").fetchone()

    self.assertEqual(currentState, oldState)

