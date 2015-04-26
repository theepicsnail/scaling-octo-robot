import api, re, urllib.request, json
import urllib.parse
url_re = "(https?[^\\s]+)"
vgd = "http://v.gd/create.php?format=simple&url="

def shorten(url):
    if len(url) < 20:
      return url
    safeurl = urllib.parse.quote(url)
    resp = urllib.request.urlopen(vgd + safeurl).read()
    return resp.decode('utf-8')

@api.onPrivmsg()
def handle(who, msg, where):
  print("Shortener called on:", msg)
  parts = re.split(url_re, msg)
  if len(parts) == 1:
    return

  parts[1::2] = map(shorten, parts[1::2])
  after = "".join(parts)
  if after == msg:
    return
  print("Shortener shortened")
  parts[1::2] = map("{{LINK}}{}{{}}".format, parts[1::2])
  api.privmsg(where, "".join(parts))

