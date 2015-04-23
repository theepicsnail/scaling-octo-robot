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
    while True:
        read = socks.local.recv(1024).decode('utf-8')
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
    if not f[0].isalpha():
      continue
    name = f.split(".")[0]
    __import__("plugins." + name)

  #handlers.emitEvent("ready")
  while True:
    line = sys.stdin.readline()
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
