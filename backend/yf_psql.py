import os
import psycopg2
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer,String,Date,Text,Boolean
# from sqlalchemy import Boolean
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
from sqlalchemy.dialects.postgresql import Insert
from passlib.context import CryptContext

### DB uri initialize ###
uri = os.environ['DATABASE_URL']
if uri and uri.startswith("postgres://"): # SQLAlchemy向けの対応
    uri = uri.replace("postgres://", "postgresql://", 1)

## init from py ###
import yf_psql_init
yf_psql_init.init_user_table(uri)
yf_psql_init.init_video_table(uri)

### sql alchemy initialize ###
engine = sqlalchemy.create_engine(uri, pool_pre_ping=True)
Base = declarative_base(bind=engine)
# Base = declarative_base()

### session initialize ###
SessionLocal = sessionmaker(bind=engine)
# db = SessionLocal()
# db.close()

### functions ###
def get_db():
    session = SessionLocal()
    try:
        # print('yfdebug:session try')
        yield session
    except:
        # print('yfdebug:session expect')
        session.rollback()
        raise
    finally:
        # print('yfdebug:session finally')
        session.close()

# SessionClass = sessionmaker(engine)
# session = SessionClass()


'''

### redisに関するコード
# import redis
# conn = redis.from_url(url=os.environ.get('REDIS_URL'), decode_responses=True)
# result = conn.set('タイトル', 'RedisMainText')
# print(conn.keys())




## DB uri initialize ##
uri = os.environ['DATABASE_URL']
if uri and uri.startswith("postgres://"): # SQLAlchemy向けの対応
    uri = uri.replace("postgres://", "postgresql://", 1)

## sql alchemy initialize ##
engine = sqlalchemy.create_engine(uri)
Base = declarative_base(bind=engine)

# session initialize #
SessionClass = sessionmaker(engine)
session = SessionClass()

class ImageUploadURI(Base):
    __tablename__ = 'img_uri'
    __table_args__ = {'autoload': True}
    uri = Column(Text, primary_key=True, unique=True) # プライマリキーを指定しないとエラーになるので注意
    date = Column(Date)
    def get_uri(self):
        return '{uri}'

def insert_stmt(uri:str, date): # 重複している場合は何もしないINSERT関数
    insert_stmt = Insert(ImageUploadURI).values([
        { 'uri' : uri, 'date': date }
        # {'uri' : 'testC.jpg', 'date' : '2021-09-02' }
    ])
    on_duplicate_key_stmt = insert_stmt.on_conflict_do_nothing()
    session.execute(on_duplicate_key_stmt)
    print(on_duplicate_key_stmt)

# exec
# insert_stmt()

def get_uri_list():
    uri_texts = session.query(ImageUploadURI).all()
    img_list = []
    for row in uri_texts:
        img_list.append(row.uri)
        # print('%s' % (row.uri))
    # print(img_list)
    return img_list

# commit and close #

# session.commit()
# session.close()






# test_ob = ImageUploadURI(uri='testB.jpg', date=datetime.now())
# session.add(test_ob)

# datas = session.query(ImageUploadURI).all()
# for row in datas:
#     print('%s' % (row.uri))
# ↑結果は以下のようになる。重複は読み込まれない。
# test.jpg
# testB.jpg
# testA.jpg





### psycopg2
def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

def test_confirm():
    # with psycopg2.connect(DB_URL, sslmode='require') as conn:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select version()")
            print(cur.fetchone())
            cur.execute("select * from image_uri")
            print(cur.fetchone())

def test_get_text():
    # ここにDBから取得した情報を書く
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from image_uri")
            text = cur.fetchone()
    return text


# text = test_get_text()
# print(text)



# def test_confirm():
#     conn = psycopg2.connect(DB_URL, sslmode='require')
#     cur = conn.cursor()

#     cur.execute("select version()")
#     print(cur.fetchone())
#     cur.execute("select * from image_uri")
#     print(cur.fetchone())

#     cur.close()
#     conn.close()

'''