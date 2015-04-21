#!/usr/bin/env python3

DEBUG = False
from collections import namedtuple
import re
sm = staticmethod
depth = 0
def staticmethod(func):
  _=[sm(func)]
  def newFunc(*a, **b):
    global depth
    f=_[0]
    print(" |" * depth, func, a, b)
    depth += 1
    res = func(*a,**b)
    depth -= 1
    print(" |" * depth, res)
    return res
  return newFunc

if not DEBUG:
  staticmethod = sm

class TokenStream:
  def __init__(self, line):
    self.pos = 0
    self.toks = list(filter(bool,re.split(r"(\d+\.\d+|\d+|\w+)", line)))
    self.toks.append("<END>")

  def get(self):
    t = self.toks[self.pos]
    self.pos += 1
    return t

  def unget(self):
    self.pos -= 1

  def __str__(self):
    return str(self.pos) + str(self.toks)
  def __repr__(self):
    return str(self)
def optional(cls, toks):
  t = toks.pos
  val = cls.parse(toks)

  if val is not None:
    return val

  toks.pos = t
  return None


class Assignment:
  @staticmethod
  def parse(line):
    var = optional(VariableAssignment, line)
    if var is not None:
      return var

    func = optional(FunctionalAssignment, line)
    if func is not None:
      return func

    return Expression.parse(line)

class VariableAssignment(namedtuple('VariableAssignment', ['name', 'expr'])):
  @staticmethod
  def parse(line):
    name = line.get()
    if not name.isalpha():
      return None
    if line.get() != '=':
      return None
    expr = Assignment.parse(line)
    if expr is None:
      return None
    return VariableAssignment(name, expr)

  def evaluate(self):
    scope[self.name] = self.expr.evaluate()
    return scope[self.name]

class FunctionalAssignment(namedtuple('FunctionalAssignment', ['name', 'args', 'expr'])):
  @staticmethod
  def parse(line):
    name = line.get()

    if not name.isalpha():
      return None
    if line.get() != '(':
      return None

    args = []
    arg = line.get()
    if arg != ')':
      # (name ',') (name ')')
      while True:
        if not arg.isalpha():
          return None
        args.append(arg)

        arg = line.get()
        if arg ==')':
          break;
        if arg ==',':
          arg = line.get()

    expr = Assignment(line)
    if expr is None:
      return None
    return FunctionAssignment(name, args, expr)


class Expression(namedtuple('Expression', ['head', 'tail'])):
  @staticmethod
  def parse(line):
    head = Term.parse(line)
    if head is None:
      return None

    tail = []
    while True:
      op = line.get()
      if op not in "+-":
        line.unget()
        break
      val = Term.parse(line)
      if val is None:
        raise "Expected atom"
      tail.append((op, val))

    if not tail:
      return head
    return Expression(head, tail)

  def evaluate(self):
    val = self.head.evaluate()
    for (mod, term) in self.tail:
      v = term.evaluate()
      if mod == '+':
        val += v
      elif mod == '-':
        val -= v
      else:
        raise("error")
    return val


class Term(namedtuple('Term', ['head', 'tail'])):
  @staticmethod
  def parse(line):
    head = Factor.parse(line)
    if head is None:
      return None

    tail = []
    while True:
      op = line.get()
      if op not in "*/%":
        line.unget()
        break
      val = Factor.parse(line)
      if val is None:
        raise "Expected atom"
      tail.append((op, val))
    if tail:
      return Term(head, tail)
    return head

  def evaluate(self):
    val = self.head.evaluate()
    for (mod, term) in self.tail:
      v = term.evaluate()
      if mod == '*':
        val *= v
      elif mod == '/':
        val /= v
      elif mod == '%':
        val %= v
      else:
        raise("error")
    return val

class Factor(namedtuple('Factor', ['base', 'exp'])):
  @staticmethod
  def parse(line):
    head = Value.parse(line)
    if head is None:
      return None

    tok = line.get()
    if tok != '^':
      line.unget()
      return head

    exp = Factor.parse(line)
    return Factor(head, exp)


  def evaluate(self):
    return self.base.evaluate() ** self.exp.evaluate()

class Value(namedtuple('Value', ['base', 'mod'])):
  @staticmethod
  def parse(line):
    mod = line.get()
    if mod not in "-":
      line.unget()
      mod = None
    base = Atom.parse(line)
    if base is None:
      return None
    if mod is None:
      return base
    return Value(base, mod)

  def evaluate(self):
    val = self.base.evaluate()
    if self.mod == '-':
      val *= -1
    return val

class Atom(namedtuple('Atom', ['value', 'name'])):
  @staticmethod
  def parse(line):
    tok = line.get()
    if tok.isalpha():
      return Atom(None, tok)
    try:
      return Atom(float(tok), None)
    except:
      return None

  def evaluate(self):
    if self.value is not None:
      return self.value
    return scope.get(self.name, 0)

def evaluate(line):
  tree = Assignment.parse(TokenStream(line.replace(" ","")))
  if tree is None:
      return None
  return tree.evaluate()

scope = {}


import api

@api.onPrivmsg()
def math(sender, message, target):
  if not message.startswith("%"):
    return
  equ = message[1:].replace(" ","")
  value = evaluate(equ)
  if value is not None:
      api.privmsg(target, "{GREEN}" + str(evaluate(equ)))


