import api
import re
import urllib.request

url_re = "(https?[^\\s]+)"

def getTitle(url):
    html = urllib.request.urlopen(url).read().decode("utf-8")
    html = " ".join(html.split("<title>")[1].split("</title>")[0].split())
    return html
@api.onPrivmsg()
def handle(who, msg, where):
    parts = re.split(url_re, msg)
    for url in parts[1::2]:
        api.privmsg(where,
                "<{blue}Title{}: {yellow}" + getTitle(url) +"{} >")
