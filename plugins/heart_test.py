from testing.testcase import TestCase
from . import heart

class TestHeart(TestCase):
  def test_without_heart(self):
    self.receive.privmsg(
        self.env.user,
        self.env.message,
        self.env.channel)
    self.assertNoSent()

  def test_with_heart(self):
    self.receive.privmsg(
        self.env.user,
        "te<3st",
        self.env.channel)

    self.assertPrivmsg(
        self.env.channel,
        'te{C5}\u2665{}st')
