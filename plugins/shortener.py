import api, re, urllib.request, json
import urllib.parse
url_re = "(https?[^\\s]+)"
vgd = "http://v.gd/create.php?format=simple&url="


def shorten(url):
    safeurl = urllib.parse.quote(url)
    resp = urllib.request.urlopen(vgd + safeurl).read()
    return resp.decode('utf-8')

@api.onPrivmsg()
def handle(who, msg, where):
  parts = re.split(url_re, msg)
  if len(parts) == 1:
    return

  shortened = False
  for i in range(1,len(parts), 2):
    url = parts[i]
    if len(url) < 20:
      continue
    parts[i] = "{{LINK}}{}{{}}".format(shorten(url))
    shortened = True

  if not shortened:
    return

  api.privmsg(where, "".join(parts))

