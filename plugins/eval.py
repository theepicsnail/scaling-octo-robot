import api
import datetime
import subprocess
import threading
import inspect
import os

@api.onCommand("eval")
def log_execution(sender, args, replyTo):
  print("EVAL",
      datetime.datetime.now().strftime("%H:%M:%S %A. %B(%m) %d %Y"),
      sender, replyTo, repr(args))

@api.onCommand("eval")
def eval_command(sender, args, replyTo):
  if " " not in args:
    return api.msg(replyTo, usage)

  script, arg = args.split(" ", 1)
  if not script.isalpha():
    return api.msg(replyTo, usage)

  bg(execute, sender, script, arg, replyTo)


# This is replaced during testing to make the call blocking instead of async.
def bg(cmd, *args):
  threading.Thread(target = cmd, args=args).start()

def shorten(line):
  if len(line) > 80:
    line = truncated.format(line[:70])
  return line

def execute(sender, script, arg, chan):
  filepath = inspect.getfile(inspect.currentframe())
  script = os.path.join(os.path.dirname(filepath), "eval", script + ".sh")
  cmd = ["bash", script, arg]  # "'%s'"%arg]
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  threading.Timer(5, p.terminate) # Kill after 5 seconds
  out, err=  p.communicate()

  print("EVAL RESULT", repr(cmd))
  print("OUT:" + repr(out))
  print("ERR:" + repr(err))

  if out:
    out = repr(out)[2:-1]
    api.msg(chan, stdoutFmt.format(shorten(out)))
  if err:
    err = repr(err)[2:-1]
    api.msg(chan, stderrFmt.format(shorten(err)))

usage = "!eval [lang] [code]"
truncated = "{{YELLOW}}Truncated{{}}:{}"
stdoutFmt = "[{{GREEN}}OUT{{}}]:{}"
stderrFmt = "[{{RED}}ERR{{}}]:{}"


