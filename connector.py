#!/usr/bin/env python3


import socket, ssl, select, os, threading
os.system("clear")

class SocketBase:
    def __init__(self):
        self.sock = None

    def connect(self):
        pass

    def send(self, text):
        try:
            text = text.encode('utf-8')
            print(self.name,"<<",text.strip())
            self.sock.send(text)
            return
        except Exception as e:
          pass
        print(self.name, "(Missed)")

    def read(self):
        if self.sock is None:
            print("[%s Connecting]" % self.name)
            self.connect()
            print("[%s Connected]" % self.name)

        try:
            ret = self.sock.recv(1024).decode('utf-8')

            if ret == "":
                self.sock = None
                return self.read()

            print(self.name,">>",ret.strip())
            return ret
        except Exception as e:
            print(e)
            self.sock = None
            raise # This should go away
        return self.read()

class IrcSocket(SocketBase):
    name = "Irc"
    def connect(self):
        host, port = "irc.hashbang.sh", 6697
        nick = "someNick"
        secure = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if secure:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_default_certs()
            s = context.wrap_socket(s, server_hostname=host)

        s.connect((host, port))
        self.sock = s
        self.send("USER a b c d :e\r\nNICK " + nick + "\r\n")

class LocalSocket(SocketBase):
    name = "Local"
    sock_file = "/tmp/sock"

    def connect(self):
        self.name = "Local"
        self.sock = None
        try:
            os.unlink(LocalSocket.sock_file)
        except:pass
        localSock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        localSock.bind(LocalSocket.sock_file)
        localSock.listen(1)
        self.sock,_ = localSock.accept()

local = LocalSocket()
irc = IrcSocket()

def serverToLocal():
    buff = ""
    while True:
        read = irc.read()
        buff += read
        while "\n" in buff:
            line, buff = buff.split("\n",1)
            if line.startswith("PING "):
                irc.send(line.replace("PING", "PONG")+"\n")

        local.send(read)
def localToServer():
    while True:
        irc.send(local.read())


a = threading.Thread(target=serverToLocal)
b = threading.Thread(target=localToServer)
a.start()
b.start()
a.join()
b.join()

