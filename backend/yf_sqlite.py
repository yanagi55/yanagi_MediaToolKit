import sqlite3
import datetime
import os
JST = datetime.timezone(offset=datetime.timedelta(hours=+9))

# ファイルパス
dbname = './yf_tmpfs/main.db'
dbpath = './yf_tmpfs'
# herokuほかtmpfsがデフォルトで存在しない環境への対応
if os.path.exists(dbpath) == False: os.mkdir('./yf_tmpfs')

def __init__():
    conn = sqlite3.connect(dbname) 
    cur = conn.cursor()
    # cmd.execute('create table img_url (id int, title text, body text, created datetime)') 
    cur.execute('CREATE TABLE IF NOT EXISTS \
    "tweets" ( \
	"id"    INTEGER, \
	"text"  TEXT, \
	"datetime"  TEXT, \
    "username"  TEXT, \
	PRIMARY KEY("id" AUTOINCREMENT) \
    );')
    
    # cmd.execute("INSERT into tweets (text, datetime) VALUES('First Text', '1990-11-01');")
    cur.close()
    conn.commit()
    conn.close()

__init__()


def get_newpost(id_from:int):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    
    cur.execute(f'SELECT text,datetime,username from tweets WHERE id > {id_from};')
    text_list = cur.fetchall() # [('text', 'datetime'), ....] 
    return text_list

def get_newest_id():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('SELECT seq FROM sqlite_sequence WHERE name="tweets";')
    max_id_value = cur.fetchone() # (value,)という形で返ってくる
    # print(max_id_value[0])
    if max_id_value == None: max_id_value = [0] # サーバーでDB初期化すると値が入らないので例外処理
    return max_id_value[0]

def get_formatted_nowtime():
    now = datetime.datetime.now(tz=JST)
    date = (f"{now:%Y-%m-%d %H:%M:%S}")
    return date

def insert_text(message:str, username:str):
    conn = sqlite3.connect(dbname)
    time = get_formatted_nowtime()
    cur = conn.cursor()
    cur.execute(f"INSERT into tweets (text, datetime, username) VALUES('{message}', '{time}', '{username}') ")
        # on conflict(id) do nothing ;')
    conn.commit()
    return

def get_uri_list():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('select filepath from img_uri')
    uri_list = cur.fetchall()
    return uri_list
    # 注記
    # select filepath と指定しているが、複数列指定も可能なため、
    # filepathの中身はlistである。bare Stringsではない。

# get_uri_list()


# def get_uri_list():
#     uri_texts = session.query(ImageUploadURI).all()
#     img_list = []
#     for row in uri_texts:
#         img_list.append(row.uri)
#         # print('%s' % (row.uri))
#     # print(img_list)
#     return img_list



# def __init__():
#     dbname = './tmpfs/main.db'
#     conn = sqlite3.connect(dbname)

# c = __init__()