import api
import time

@api.onCTCP("VERSION")
def version(who, cmd, args):
  api.ctcp(who,"VERSION", "SomeIrcBot 1.2.3")

@api.onCTCP("TIME")
def version(who, cmd, args):
  api.ctcp(who, "TIME", time.ctime())
