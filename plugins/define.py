import api
import re
import urllib.request
import json

url = "https://glosbe.com/gapi/translate?from=eng&dest=eng&format=json&page=1&phrase="
cache = {}

def define(phrase):
    data = urllib.request.urlopen(url + phrase).read().decode("utf-8")
    return json.loads(data)["tuc"][0]["meanings"]

@api.onCommand("gd")
#@api.onCommand("define")
def handle(who, msg, where):
    res = re.match("^([0-9]+ |)(.*)$", msg)
    if not res:
        return
    num, term = res.groups()
    if num:
        num = int(num.strip())
    else:
        num = 1

    if num < 1:
        num = 1

    val = cache.get(term, None)
    if val is None:
        val = define(term)
        cache[term]=val


    n = len(val)
    num -= 1
    if num >= n:
        api.privmsg(where, "{} has {} definitions. [1-{}]".format(term, n,n))
        return

    definition = val[num]["text"]
    api.privmsg(where, "<{{C3}}Definition{{}} {{B}}{}{{}} (of {}) for {{B}}{}{{}}> {}".format(
        num + 1, n, term, definition))


