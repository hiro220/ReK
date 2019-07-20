# coding:utf-8

import sqlite3

db = 'data/savedata.db'

"""
# データベース
conn = sqlite3.connect(db)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# rankingテーブルが存在しないとき、作成する
cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='ranking'")
if cur.fetchone()[0] == 0:
    cur.execute('CREATE TABLE ranking(id INTEGER PRIMARY KEY, stage INTEGER, score INTEGER)')

# dataテーブルが存在しないとき、作成する
cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='data'")
if cur.fetchone()[0] == 0:
    cur.execute("CREATE TABLE data(key TEXT, value TEXT)")

# データベースへのコネクションを閉じる
conn.close()
"""

def create_table(table_name, keys):
    """
    - table_name : string
    - keys : string list ['key_name type', ...]
    - name type :
        - INTEGER(int)
        - TEXT(str)
        - REAL(float)
    """
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # rankingテーブルが存在しないとき、作成する
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", [table_name])
    execute_text = 'CREATE TABLE ' + table_name + '(' + ', '.join(keys) + ')'
    if cur.fetchone()[0] == 0:
        cur.execute(execute_text)

    # データベースへのコネクションを閉じる
    conn.close()


create_table('ranking', ['id INTEGER PRYMARY KEY', 'stage INTEGER', 'score INTEGER'])
create_table('data', ['key TEXT', 'value TEXT'])
create_table('gun', ['id INTEGER', 'name TEXT', 'bullet_max INTEGER', 'reload_size INTEGER', 'own INTEGER'])


def insert_score(stage_id, score):
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # そのステージのスコアが1000を超えているならdeleteする
    ranking = [data for data in cur.execute('SELECT id, score FROM ranking WHERE stage=?', str(stage_id))]
    if len(ranking) > 1000:
        ranking = sorted(ranking, lambda x:x[1])
        data_id = ranking[0][0]
        cur.execute("DELETE FROM ranking WHERE id=?", [data_id])

    cur.execute('INSERT INTO ranking(stage, score) values(?, ?)', [stage_id, score])


    # データベースへの変更をコミット
    conn.commit()
    # データベースへのコネクションを閉じる
    conn.close()

def load_ranking(stage_id):
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    ranking = [data for data in cur.execute('SELECT id, score FROM ranking WHERE stage=?', str(stage_id))]
    # データベースへのコネクションを閉じる
    conn.close()
    return ranking

def _save_gun(cur, values):
    for gun_id, dic in values.items():
        # keyがテーブル内に存在するなら更新、存在しないなら追加する。
        cur.execute("SELECT COUNT(*) FROM gun WHERE id=?", [gun_id])
        if cur.fetchone()[0] == 0:
            data_list = [gun_id] + list(dic.values())
            cur.execute("INSERT INTO gun(id, name, bullet_max, reload_size, own) values(?, ?, ?, ?, ?)", data_list)
        else:
            cur.execute("UPDATE gun SET own=? WHERE id=?", [dic['own'], gun_id])
        
def save(data_dic):
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    for key, value in data_dic.items():
        if type(value) == dict:
            if key == 'gun':
                _save_gun(cur, value)
                value = 'dict'
        # keyがテーブル内に存在するなら更新、存在しないなら追加する。
        cur.execute("SELECT COUNT(*) FROM data WHERE key=?", [key])
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO data(key, value) values(?, ?)", [key, value])
        else:
            cur.execute("UPDATE data SET value=? WHERE key=?", [value, key])
    # データベースへの変更をコミット
    conn.commit()
    # データベースへのコネクションを閉じる
    conn.close()

def _load_gun():
    dic = {}
    for _id, key, data in cur.execute("SELECT * FROM gun"):
        data = {}
        for key, value in zip(data[0::2], data[1::2]):
            data[key] = value
        dic[key] = value
    return dic


def load():
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # dataテーブル内から全てのデータを辞書にして取り出す。
    data_dic = {}
    for key, value in cur.execute("SELECT * FROM data"):
        if key == 'gun':
            data_dic[key] = _load_gun()
        data_dic[key] = value

    # データベースへのコネクションを閉じる
    conn.close()
    return data_dic

if __name__=='__main__':
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    cur.execute("DROP TABLE ranking")
    cur.execute("DROP TABLE data")
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='ranking'")
    print("ranking table deleted :", cur.fetchone()[0] == 0)
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='data'")
    print("data table deleted :", cur.fetchone()[0] == 0)
    conn.commit()
    conn.close()