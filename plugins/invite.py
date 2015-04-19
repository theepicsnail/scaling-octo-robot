import api

@api.onInvite()
def invited(sender, chan):
  api.join(chan)

