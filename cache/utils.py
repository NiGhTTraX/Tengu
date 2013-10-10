from django.db import connection


class disableSynchronous():

  def __init__(self):
    self.previous = None

  @classmethod
  def disable(cls):
    """Disables SQLite synchronous mode for faster performance."""
    if connection.vendor == "sqlite":
      cursor = connection.cursor()
      cls.previous = cursor.execute("PRAGMA synchronous;").fetchone()
      cursor.execute("PRAGMA synchronous = OFF;")

    return cls.previous

  @classmethod
  def restore(cls):
    """Restores the SQLite synchronous mode."""
    if connection.vendor == "sqlite" and cls.previous:
      cursor = connection.cursor()
      cursor.execute("PRAGMA synchronous = %s;" % cls.previous)

  def __enter__(self):
    self.disable()
    return self.previous

  def __exit__(self, type, value, traceback):
    self.restore()

