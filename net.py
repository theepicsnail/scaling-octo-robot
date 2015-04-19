import socket, sys, threading, os

sock_file = "/tmp/sock"

usock = None

def startLocalServer():
  global usock
def connectLocal():
  global usock
  usock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  usock.connect(sock_file)

def usockGetCh():
  global usock
  if usock is None:
    return ''
  return usock.recv(1).decode('utf-8')

def usockSendLine(line):
  global usock
  if usock is None:
    print("Missed message", line)
    return
  print("[usock]<<",line)
  return usock.send(line.encode('utf-8'))

def reader(getCh, onLine):
  def readloop():
    data = ""
    while True:
      ch = getCh()
      if ch == '':
        print("End of", onLine)
        return
      if ch == '\n':
        onLine(data)
        data = ""
      else:
        data += ch

  return threading.Thread(target = readloop)
