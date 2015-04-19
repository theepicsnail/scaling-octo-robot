#!/usr/bin/env python3
from colors import parse_colors
import api
import os
os.system("clear")
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
    if read == '':
      print("[remote disconnect]")
      shutdown()
      return

    data += read
    while "\n" in data:
      line, data = data.split("\n", 1)
      handleLine(line.replace("\r",""))

def mainLoop():
  api.raw = sendline
  for f in os.listdir("plugins"):
    if not f[0].isalpha():
      continue
    name = f.split(".")[0]
    __import__("plugins." + name)

  api.emitEvent("ready")
  while True:
    line = sys.stdin.readline()
    socks.local.send(line.encode('utf-8'))

def shutdown():
  pass

def handleLine(line):
  api.emitEvent("line", line)

socks.local = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
socks.local.connect(sock_file)
b = threading.Thread(target=readLocal)
b.start()
mainLoop()
b.join()
