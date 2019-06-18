# coding:utf-8

import sqlite3

db = 'data/savedata.db'

# データベース
conn = sqlite3.connect(db)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

try:
    cur.execute('CREATE TABLE ranking(stage INTEGER, score INTEGER)')

except sqlite3.Error as e:
    print('sqlite3.Error :', e.args[0])
"""
cur.execute('INSERT INTO ranking(score) values(100)')
cur.execute('INSERT INTO ranking(score) values(3400)')
cur.execute('INSERT INTO ranking(score) values(200)')
cur.execute('INSERT INTO ranking(score) values(120)')

# データベースへの変更をコミット
conn.commit()

print([data for data in cur.execute('SELECT * FROM ranking')])
"""
# データベースへのコネクションを閉じる
conn.close()

def insert_score(stage_id, score):
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    cur.execute('INSERT INTO ranking(stage, score) values(?, ?)', [stage_id, score])
        
    # データベースへの変更をコミット
    conn.commit()
    # データベースへのコネクションを閉じる
    conn.close()

def print_ranking():
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    print([data for data in cur.execute('SELECT * FROM ranking')])
    # データベースへのコネクションを閉じる
    conn.close()
