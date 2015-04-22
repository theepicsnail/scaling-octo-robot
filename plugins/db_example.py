import api
import db
print("imported api, got:")
print(dir(api))
# Create a shelve.
# also seed it with initial data
d = db.Shelve().seed({
  "loads": 0
})

d["loads"] += 1

loads = d["loads"]

@api.onCommand("loads")
def printLoads(sender, args, chan):
  api.privmsg(chan, "I've been restarted %s times!" % loads)

