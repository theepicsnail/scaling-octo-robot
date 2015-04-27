from testing.testcase import TestCase
from unittest.mock import MagicMock
from . import shortener


class TestShortener(TestCase):
  def setUp(self):
    super().setUp()
    shortener.shorten = MagicMock()

  def test_nourls(self):
    self.receive.privmsg(self.env.user,
        self.env.message, self.env.channel)
    self.assertFalse(shortener.shorten.called)

  def test_with_short_url(self):
    self.receive.privmsg(self.env.user,
        "http://google.com", self.env.channel)
    self.assertFalse(shortener.shorten.called)

  def test_with_long_url(self):
    shortener.shorten.return_value = "http://v.gd/example"
    self.receive.privmsg(self.env.user,
        "http://google.com/calendar",
        self.env.channel)

    self.assertPrivmsg(
        self.env.channel,
        u'{LINK}http://v.gd/example{}')
