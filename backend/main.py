# -*- coding: utf-8 -*-
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, JSONResponse, StreamingResponse
# from fastapi.security import OAuth2PasswordBearer
# from fastapi.params import Depends
from pydantic import BaseModel
import random
import uvicorn
import yf_sqlite
import yf_api

app = FastAPI()
app.include_router(yf_api.router)

# 動的コンテンツの取得
@app.get('/storage/{item_id}')
def read_item( item_id ):
    filepath = './storage/'+item_id
    return FileResponse(filepath)

@app.get('/storage/user_icon/{item}')
def get_icon(item):
    filepath = './storage/user_icon/'+item
    return FileResponse(filepath)

@app.get('/storage/video/output/{item}')
def get_video(item):
    filepath = './storage/video/output/'+item
    return FileResponse(filepath)

@app.get('/storage/video/public/{title}/{item}')
def get_video(title, item):
    filepath = './storage/video/public/' + title +'/'+ item
    return FileResponse(filepath)

### サービスワーカーに対応した静的マウント(以降で動的に書いても反応しないので注意) ###
app.mount('/', StaticFiles(directory='./dist', html=True), name='static_html')
app.mount('/', StaticFiles(directory='./dist', html=False), name='static_file')


if __name__ == '__main__':
    print('uvicorn test')
    uvicorn.run('main:app')
    # host,portはlaunch.jsonでuvicornのパラメータで指定
    # uvicorn.run('main:app', host='0.0.0.0', port=5000)
    # 2021/09現在、WindowsDefenderでプライベートネットワークのみ許可している。

## FLASK old ##
# flaskの記述がほとんど参考にならなくなったため削除。
# サイズ制限の記述のみ、FastAPIそのもの全体で指定する感じではないので残す。
# app = Flask(__name__, static_folder='../dist/static',
#             template_folder='../dist')
# app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000 # max: 50 MB