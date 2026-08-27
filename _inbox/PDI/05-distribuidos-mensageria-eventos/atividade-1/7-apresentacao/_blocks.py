# -*- coding: utf-8 -*-
def P(t):  return ("p", t)
def UL(items):  return ("ul", list(items))
def OL(items):  return ("ol", list(items))
def TBL(h, rows):  return ("table", list(h), [list(r) for r in rows])
def CODE(lang, c):  return ("code", lang, c)
def H(t):  return ("h", t)
def N(t):  return ("note", t)
def W(t):  return ("warn", t)
