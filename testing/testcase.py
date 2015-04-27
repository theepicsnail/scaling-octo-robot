import unittest
import api

class Receiver:
  def privmsg(self, who, what, where):
    api.emitEvent("line", ":%s!host@domain.com PRIVMSG %s:%s" %(
      who, where, what))


receiver = Receiver()
class TestCase(unittest.TestCase):

  def setUp(self):
    global env
    self.env = env
    self.sent = []
    self.receive = receiver
    api.handlers.register("sendline", self.sent.append)

  def assertPrivmsg(self, to, msg):
    self.assertTrue(self.sent)
    self.assertEqual(self.sent.pop(0),
        "PRIVMSG %s :%s" % (to, msg))

  def assertNoSent(self):
    self.assertFalse(self.sent)

_id = 0
class TestEnv:
  def __init__(self):
    self.user = self.newUser()
    self.message = self.newMessage()
    self.channel = self.newChannel()

  def newUser(self):
    return "User" + self.nextId()

  def newMessage(self):
    return "Message " + self.nextId()

  def newChannel(self):
    return "#test" + self.nextId()

  def nextId(self):
    global _id
    _id += 1
    return str(_id)
env = TestEnv()

