# coding:utf-8

import sqlite3

db = 'data/savedata.db'

conn = sqlite3.connect(db)
conn.cursor()

try:
    conn.execute('CREATE TABLE')