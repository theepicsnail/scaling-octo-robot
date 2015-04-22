from api.handlers import emitEvent
def raw(line):
  emitEvent("sendline", line)

def rawf(line, *args):
  raw(line.format(*args))

def msg(target, message):
  rawf("PRIVMSG {} :{}", target, message)
privmsg = msg

def join(chan):
  rawf("JOIN {}", chan)



