#!/usr/bin/env python3
from util.color import parse_colors
from api import handlers
import os
#os.system("clear")
sock_file = "/tmp/sock"
import socket, sys, threading


class socks:
  local = None

def sendline(line):
  if socks.local is None:
    shutdown()
  else:
    line = parse_colors(line) + "\r\n"
    socks.local.send(line.encode("utf-8"))

def readLocal():
    data = ""
    socks.local.settimeout(.1)
    while True:
        try:
            read = socks.local.recv(1024).decode('utf-8')
        except socket.timeout:
            continue
        print("Bot read", read, "from local")
        if read == '':
            print("[remote disconnect]")
            shutdown()
            return

        data += read
        while "\n" in data:
            line, data = data.split("\n", 1)
            try:
                handleLine(line.replace("\r",""))
            except Exception as e:
                print(e)


def mainLoop():
  handlers.register("sendline", sendline)
  for f in os.listdir("plugins"):
    if not f.endswith(".py"): # Not python? skip.
      continue
    if f.endswith("test.py"): # Python, but is a test? skip.
      continue
    name = f.split(".")[0]
    __import__("plugins." + name)

  #handlers.emitEvent("ready")
  while True:
    try:
        line = sys.stdin.readline()
    except KeyboardInterrupt:
        print("Keyboard interrupt. closing socket")
        socks.local.close()
        return
    socks.local.send(line.encode('utf-8'))

def shutdown():
  pass

def handleLine(line):
  handlers.emitEvent("line", line)

socks.local = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
socks.local.connect(sock_file)
b = threading.Thread(target=readLocal)
b.start()
mainLoop()
b.join()
