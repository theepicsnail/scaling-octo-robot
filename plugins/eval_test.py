from testing.testcase import TestCase
from . import eval

# Make the commands blocking.
eval.bg = lambda cmd,*args:cmd(*args)

class TestEval(TestCase):
  def test_echo(self):
    self.alice.say("!eval echo test")
    self.alice.assertMsg(eval.stdoutFmt.format("'test'"))

  def test_bad_lang(self):
    self.alice.say("!eval ../bad.sh muahaha")
    self.alice.assertMsg(eval.usage)

  def test_no_bash_evaluation(self):
    self.alice.say("!eval echo *")
    self.alice.assertMsg(eval.stdoutFmt.format("'*'"))
    # Should be '*' not a directory list.
