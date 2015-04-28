import api
import html
import json
import re
import urllib.parse
import urllib.request

url_re = "(https?[^\\s]+)"


def getTitle(url):
    data = urllib.request.urlopen(url).read().decode("utf-8")
    title = " ".join(data.split("<title>")[1].split("</title>")[0].split())
    return html.unescape(title)

def shorten(url):
    safeurl = urllib.parse.quote(url)
    v_gd = "http://v.gd/create.php?format=simple&url="
    resp = urllib.request.urlopen(v_gd + safeurl).read()
    return resp.decode('utf-8')


@api.onPrivmsg()
def handle(who, msg, where):
  parts = re.split(url_re, msg, 1) # Only grab the first url. lame i know.
  if len(parts) == 1:
    return

  url = parts[1]

  short = ""
  if len(url) >= 20: # Long enough for a shorten
    short = shorten(url)
    short = "{{LINK}}{}{{}} | ".format(shorten(url))

  title = getTitle(url)

  out = "<{}{{blue}}Title{{}}: {{yellow}}{}{{}}>".format(short, title)
  api.privmsg(where, out)

