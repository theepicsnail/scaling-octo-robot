"""
Various database providers, as well as some wrapers and backing logic over them.

"""
import util.caller
import shelve

class Shelve:
  def __init__(self, name=None):
    self.filename = util.caller.getCaller()
    if name:
      self.filename += "_" + name
    self.filename += ".shlv"
    print(self.filename)
    self.open()

  def open(self):
    self.shelve = shelve.open("data/" + self.filename)

  def fixKey(self, key):
    if not isinstance(key, str):
      key2 = "%s" % key
      print("[Warning] key '%s' is not a basestring. Using '%s' as a key." % (key, key2))
      return key2
    return key

  def __getitem__(self, key):
    return self.shelve[self.fixKey(key)]

  def __setitem__(self, key, val):
       self.shelve[self.fixKey(key)] = val

  def __contains__(self, key):
    return key in self.shelve

  def __delitem__(self, key):
    del self.shelve[key]

  def seed(self, mapping):
    """Sets default values for this instance"""
    for k,v in mapping.items():
      k = self.fixKey(k)
      if k not in self.shelve:
        self[k]=v
    return self


