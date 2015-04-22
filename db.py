"""
Various database providers, as well as some wrapers and backing logic over them.

"""
import utils
import shelve

class Shelve:
  def __init__(self, name=None):
    self.filename = utils.caller()
    if name:
      self.filename += "_" + name
    self.filename += ".shlv"
    print(self.filename)
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

  def seed(self, mapping):
    """Sets default values for this instance"""
    for k,v in mapping.items():
      k = self.fixKey(k)
      if k not in self.shelve:
        self[k]=v
    return self


