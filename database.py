# coding:utf-8

import sqlite3

db = 'data/savedata.db'

# データベース
conn = sqlite3.connect(db)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='ranking'")
if cur.fetchone()[0] == 0:
    cur.execute('CREATE TABLE ranking(stage INTEGER, score INTEGER)')

cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='data'")
if cur.fetchone()[0] == 0:
    cur.execute("CREATE TABLE data(key TEXT, value TEXT)")

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

def save(data_dic):
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    for key, value in data_dic.items():
        print(key, value)
        cur.execute("SELECT COUNT(*) FROM data WHERE key=?", key)
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO data(key, value) values(?, ?)", [key, value])
        else:
            cur.execute("UPDATE data SET value=? WHERE key=?", [value, key])
    # データベースへの変更をコミット
    conn.commit()
    # データベースへのコネクションを閉じる
    conn.close()

def load():
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    data_dic = {}

    for key, value in cur.execute("SELECT * FROM data"):
        data_dic[key] = value

    # データベースへのコネクションを閉じる
    conn.close()
    return data_dic

save({"1":"changed", "2":"change", "3":"replace"})
print(load())