#!/usr/bin/env python3


import socket, ssl, select, os, threading
os.system("clear")
class socks:
  localServer = None
  local = None
  remote = None

def connect_local(sock_file):
  try:
    os.unlink(sock_file)
  except:pass
  localSock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  localSock.bind(sock_file)
  localSock.listen(1)
  socks.localServer = localSock

def acceptLocal():
  print("[Waiting Local]")
  socks.local = None
  socks.local,_ = socks.localServer.accept()
  print("[Local Connected]")


def serverToLocal():
  data = ""
  while True:
    read = socks.remote.recv(1024)
    if read == b'':
      print("[Remote disconnect]")
      socks.remote = None
      return

    data += read.decode("utf-8")
    while "\n" in data:
      line, data = data.split("\n", 1)
      if line.startswith("PING"):
        line = "PONG {}\r\n".format(line.split(" ")[1])
        socks.remote.send(line.encode('utf-8'))
        print("[Ping]")

    if socks.local == None:
      print("Local missed:", read)
      continue

    try:
      print(">>", read)
      socks.local.send(read)
    except Exception as e:
      print("Local exception:", read)
      print(e)

def localToServer():
  while True:
    try:
        data = socks.local.recv(1024)
    except:
        data = ""
    if data.decode("utf-8") == "":
      print("[Local disconnect]")
      if socks.remote is None:
        return
      acceptLocal()
      print("[Local reconnect]")
      continue

    try:
      print("<<", data)
      socks.remote.send(data)
    except Exception as e:
      print("Remote missed:", data)
      print(e)

def connectIrc(host, port, nick, secure=False):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  if secure:
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()
    s = context.wrap_socket(s, server_hostname=host)

  print("[irc Connecting]")
  s.connect((host, port))
  print("[irc Connecting]")
  socks.remote = s
  socks.remote.send("USER a b c d :e\r\nNICK {}\r\n".format("somenick").encode('utf-8'))



connect_local("/tmp/sock")
acceptLocal()
connectIrc("irc.hashbang.sh", 6697, "someNick", True)
a = threading.Thread(target=serverToLocal)
b = threading.Thread(target=localToServer)
a.start()
b.start()
a.join()
b.join()

