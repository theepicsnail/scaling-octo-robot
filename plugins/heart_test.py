from testing.testcase import TestCase
import heart

class TestHeart(TestCase):
  def test_without_heart(self):
    self.receive.privmsg("user", "test", "channel")
    self.assertEqual(self.sent, [])

  def test_with_heart(self):
    self.receive.privmsg("user", "te<3st", "channel")
    expected = u'PRIVMSG user :te{C5}\u2665{}st'
    self.assertEqual(self.sent, [expected])

