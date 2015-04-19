import re
__handlers = {
  "line": set()
}
def emitEvent(event, *args):
  for handler in __handlers.get(event, []):
    handler(*args)


# Irc commands
def raw(line):
  """Replaced by bot.py unpon having an actual handler"""
  print("Unhandled", line)

def rawf(line, *args):
  raw(line.format(*args))

def msg(target, message):
  rawf("PRIVMSG {} :{}", target, message)
privmsg = msg

def join(chan):
  rawf("JOIN {}", chan)



# Decorators
# Lower level - works on all lines of irc
def onRawLine():
  def decorator(func):
    __handlers["line"].add(func)
    return func
  return decorator

def onRegex(expr, flags=0, search=False):
  # search - search or match, defaults to match.
  matcher = re.compile(expr, flags)
  matchcmd = matcher.search if search else matcher.match
  def decorator(func):
    @onRawLine()
    def handler(line):
      match = matchcmd(line)
      if not match:
        return
      func(match)
    return handler
  return decorator

# protocol level - works of each interesting message type
def onPrivmsg():
  def decorator(func):
    @onRegex("^:(.*?)!.*?PRIVMSG (.*?) :(.*)$")
    def handler(match):
      sender, target, message = match.groups()
      print("privmsg regex matched")
      if target[0]!='#':
        target = sender

      func(sender, message, target)
    return handler
  return decorator

def onInvite():
  def decorator(func):
    #':snail!snail@#!-D1E8CCF0.hsd1.ca.comcast.net INVITE somenick :#test\r\n
    @onRegex("^:(.*?)!.*INVITE (.*?) :(.*)$")
    def handler(match):
      sender, target, channel = match.groups()
      func(sender, channel)
    return handler
  return decorator
# high level - works on only specifically interesting events
def onCommand(command=None, split=False):
  """
  command - string to match to run this command
  split - whther to return the args as a string(False)
          or the parsed list (True).

  @cmd("date", split=True)
  def date(sender, args, target):
  """

  hook = [command, split]
  def decorator(func):
    @onPrivmsg()
    def commandHandler(who, what, where):
      if not what.startswith("!" + command):
        return

      if split:
        args = what.split(" ")[1:]
      else:
        args = ""
        if " " in what:
          args = what.split(" ",1)[1]

      func(who, args, where)
    return commandHandler
  return decorator

