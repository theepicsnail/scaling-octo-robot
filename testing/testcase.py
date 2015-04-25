import unittest
import api

class Receiver:
  def privmsg(self, who, what, where):
    api.emitEvent("line", ":%s!host@domain.com PRIVMSG %s:%s" %(
      who, where, what))




receiver = Receiver()
class TestCase(unittest.TestCase):

  def setUp(self):
    self.sent = []
    self.receive = receiver
    api.handlers.register("sendline", self.sent.append)
