#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Database Layer
#   Functions related to the database layer
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import platform
import sqlite3

# Functions
def getTokenDB(path):
  conn=sqlite3.connect(path)
  conn.execute('''CREATE TABLE IF NOT EXISTS HoneyTokens
                  (ID               INTEGER  PRIMARY KEY AUTOINCREMENT,
                   Token            TEXT     NOT NULL,
                   Action           TEXT     Not NULL,
                   CaseInsensitive  INTEGER  NOT NULL);''')
  conn.commit()
  return conn


def addTokens(path, tokens):
  if type(tokens)!=list:
    tokens=[tokens]
  conn=getTokenDB(path)
  tkns=selectAllFrom(path, "HoneyTokens")
  added=0
  for t in tokens:
    if not any(d['token']==t['token']  for d in tkns):
      conn.execute('''INSERT INTO HoneyTokens(Token, Action, CaseInsensitive) VALUES(:token,:action,:ci)''',
                      {'token':t['token'], 'action': t['action'], 'ci': t['caseinsensitive']})
      added+=1
  conn.commit()
  conn.close()
  return added


def selectAllFrom(path, table, where=None):
  conn=sqlite3.connect(path)
  curs=conn.cursor()
  wh="where "+" and ".join(where) if where else ""
  data=list(curs.execute("SELECT * FROM %s %s"%(table,wh)))
  dataArray=[]
  names = list(map(lambda x: x[0], curs.description))
  for d in data:
    j={}
    for i in range(0,len(names)):
      j[names[i].lower()]=d[i]
    dataArray.append(j)
  conn.close()
  return dataArray

