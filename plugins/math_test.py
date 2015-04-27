from testing.testcase import TestCase
from . import math

class TestMath(TestCase):
  def test_simple(self):
    self.receive.privmsg(
        self.env.user,
        "%1+2",
        self.env.channel)
    self.assertPrivmsg(
        self.env.channel,
        "{GREEN}3.0")
  def test_error(self):
    self.assertRaises(Exception,
        self.receive.privmsg,
        # args
        self.env.user,
        "%1+",
        self.env.channel)

    self.assertPrivmsg(
        self.env.channel,
        "{GREEN}1+{RED}<Incomplete expression>{GREEN}")
