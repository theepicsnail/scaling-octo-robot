import api
import datetime
import subprocess
import threading
import inspect
import os

@api.onCommand("eval")
def log_execution(sender, args, replyTo):
  print("EVAL")
  print(sender, replyTo)
  print(repr(args))
  print(datetime.datetime.now().strftime("%H:%M:%S %A. %B(%m) %d %Y"))

@api.onCommand("eval")
def printDate(sender, args, replyTo):
  if " " not in args:
    return api.msg(replyTo, "!eval [lang] [code]")

  script, arg = args.split(" ", 1)
  if not script.isalpha():
    return api.msg(replyTo("invalid language. ([a-zA-Z]+)"))

  threading.Thread(target = execute, args=(sender, script, arg, replyTo)).start()

def shorten(line):
  if len(line) > 80:
    line = "{YELLOW}Truncated{}:" + line[:70]
  return line

def execute(sender, script, arg, chan):
  filepath = inspect.getfile(inspect.currentframe())
  script = os.path.join(os.path.dirname(filepath), "eval", script + ".sh")
  cmd = ["bash", script, "'%s'"%arg]
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  threading.Timer(5, p.terminate) # Kill after 5 seconds
  out, err=  p.communicate()

  print("EVAL RESULTS")
  print("CMD:" + repr(cmd))
  print("OUT:" + repr(out))
  print("ERR:" + repr(err))

  if out:
    out = repr(out)[2:-1]
    api.msg(chan, "[{GREEN}OUT{}]:" + shorten(out))
  if err:
    err = repr(err)[2:-1]
    api.msg(chan, "[{RED}ERR{}]:" + shorten(err))

