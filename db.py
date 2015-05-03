"""
Various database providers, as well as some wrapers and backing logic over them.

"""
import util.caller
import shelve
import sqlite3

# Gets overwritten during testing
def shelve_opener(filename):
  return shelve.open("data/" + filename)

def Shelve(default = {}):
  filename = util.caller.getCaller()+".shlv"
  db = shelve_opener(filename)

  for k,v in default.items():
    if k not in db:
      db[k]=v
  return db

# Gets overwritten during testing
def sqlite3_opener(db):
  return sqlite3.connect(db)

def Sqlite3(defaultCommands=[]):
  filename = util.caller.getCaller()+".sql3"
  db = sqlite3_opener(filename)

  for instr in defaultCommands:
    db.execute(instr)
  return db





