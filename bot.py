#!/usr/bin/env python3
import socket, ssl, select, os, threading, configparser, time
from util.color import parse_colors
from api import handlers
import os
import socket, sys, threading
import configparser
class Bot:
  def __init__(self, config):
    self.config = config
    self.autorun = False # Should run autorun in response in ping?
    self.sock = None
    self.running = True

    #threading.Thread(target=self.readLoop).start()
    self.connect()

  def shutdown(self):
    self.running = False
    self.disconnect()

  def disconnect(self):
    try:
      send("QUIT")
    except:pass
    self.sock.close()
    self.sock = None

  def connect(self):
    connection = self.config["Connection"]
    registration = self.config["Registration"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if connection.get("ssl", False):
      context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
      #context.verify_mode = ssl.CERT_REQUIRED
      #context.check_hostname = True
      #context.load_default_certs()
      s = context.wrap_socket(s, server_hostname=connection["host"])

    # Connect (and retry) logic.
    delay = 1
    connected = False
    while not connected:
      try:
        print("Connecting to {} on port {}".format(connection["host"], connection.get("port", "6667")))
        s.connect((connection["host"],
          int(connection.get("port", "6667"))))
        connected = True
        print("Connected!")
      except Exception:
        print("[Connection refused]")
        raise
        print("Waiting {}s".format(delay))
        time.sleep(delay)
        delay *= 2
        if delay > 30:
          delay = 30

    self.sock = s
    print("Handshake...")
    self.send("USER {} {} * :{}\r\n".format(
      registration["username"],
      registration["mode"],
      registration["realname"]
      ))

    self.send("NICK {}\r\n".format(
      registration["nick"]
      ))
    
    self.autorun = True

  def send(self, line):
    try:
      self.sock.send(parse_colors(line+"\r\n").encode('utf-8'))
    except:
      print("Error sending line:" + repr(line))
      pass 

  def readLoop(self):
    buff = ""
    while self.running:
      if self.sock is None:
        time.sleep(1)
        continue
      
      read = self.sock.read(1024)
      print("Read:", read)
      if read == b'':
        self.disconnect()
        self.connect()
        continue
 
      buff += read.decode('utf-8', 'ignore')
      while "\n" in buff:
        line, buff = buff.split("\n", 1)
        self.handleNetLine(line.replace("\r",""))

  def handleNetLine(self, line):
    if line.startswith("PING "):
      self.send(line.replace("PING", "PONG"))

    if (" " in line) and line.split(" ")[1]=="001" and self.autorun:
        self.performAutorun()

    handlers.emitEvent("line", line)
  
  def performAutorun(self):
    print("Autorun")
    self.autorun = False
    autorun = self.config["Autorun"] if "Autorun" in self.config else {}
    for i in range(100): # up to 100 inital lines *shrug*
      s = str(i)
      if s in autorun:
        self.send(autorun[s])
         

def loadPlugins(sendline):
    handlers.register("sendline", sendline)
    for f in os.listdir("plugins"):
        if not f.endswith(".py"): # Not python? skip.
          continue
        if f.endswith("test.py"): # Python, but is a test? skip.
          continue
        name = f.split(".")[0]
        try:
            __import__("plugins." + name)
            print("[ OK ]", name)
        except Exception as e:
            print("[FAIL]", name, e)

# Read config
conf = configparser.ConfigParser()
conf.read("config.cfg")
b = Bot(conf)
loadPlugins(b.send)
b.readLoop()
