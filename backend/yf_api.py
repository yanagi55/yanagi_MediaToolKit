# -*- coding: utf-8 -*-
from fastapi import APIRouter, UploadFile, File, Request, \
    Form, BackgroundTasks, Depends, Cookie, Body
from typing import List, Dict, Optional
from pydantic import BaseModel
from sqlalchemy.sql.operators import is_
from starlette.responses import FileResponse, Response, StreamingResponse
from sqlalchemy.orm import Session
import yf_auth
import eyed3_mymodule
import shutil
import uuid
import os
import json
import glob
from pathlib import Path
import yf_sqlite
import yf_psql_user_crud
import yf_psql_video_crud
import yf_psql
import PIL.Image
import datetime

router = APIRouter()
RECENT_NUMBER = 20 # 最新取得件数

### Functions ###
def remove_tempfile(path:str) -> None: # 非同期処理で削除する関数
    os.remove(path)

### Authenticate User ユーザー認証 ###
@router.get('/user/authenticate', tags=['user'])
async def get_authenticate(is_auth: bool = Depends(yf_auth.authenticate_user)):
    return is_auth
### Authorize Token トークン認可 ###
@router.get('/user/authorize', tags=['user'])
async def get_authorize(token_user: str = Depends(yf_auth.authorize_user_token)):
    return token_user
### Logout ###
@router.post('/user/logout', tags=['user'])
async def logout(token_user: str = Depends(yf_auth.authorize_user_token)):
    print('logout: ' + token_user['user'])
    return token_user

### Register ユーザー登録 ###
@router.post('/user/register', tags=['user'])
# async def register(username: str, email: str, password: str):
async def register(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(yf_psql.get_db)
):
    check = yf_psql_user_crud.check_duplicated_user(email, username, db)
    if not check: return False
    register = yf_psql_user_crud.register_user(email, username, password, db)
    return register

# 動画のリストを読み込む
@router.get('/api/get_video_list')
async def get_video_list(
    db: Session = Depends(yf_psql.get_db)
):
    dist_list = yf_psql_video_crud.get_video_list(db)
    return dist_list

@router.post('/api/video_upload_raw_mp4')
async def video_upload_raw_mp4(
    video: UploadFile = File(...),
    db: Session = Depends(yf_psql.get_db)
):
    print("normal")
    return

# 動画アップロード Upload Video
@router.post('/api/video_upload')
async def video_upload(
    title: str = Form(...),
    dist: str = Form(...),
    username: str = Form(...),
    video: UploadFile=File(...),
    thumb: UploadFile=File(...),
    db: Session = Depends(yf_psql.get_db)
    # dir_id: str = Form(...),
):
    # RDB処理
    dir_id = dist
    # dir_id = username + '-' + title # ★簡易的に、ユーザーネーム+タイトルをIDとする
    check = yf_psql_video_crud.check_duplicated_user_video(db, dir_id)
    # if not check: return False

    # 既に同じIDがない場合のみ、登録操作をする
    if check: yf_psql_video_crud.register_video(db, title, username, dir_id)

    # ファイル処理
    upload_dir = './storage/video/public/' + dir_id + '/'
    if os.path.exists(upload_dir) == False : os.makedirs(upload_dir)
    saveVideoPath = os.path.join(upload_dir, video.filename)
    with open(saveVideoPath, 'wb') as buffer:
        shutil.copyfileobj(video.file, buffer)

    # サムネ

    thumb_name = 'thumb.webp'
    thumb_path = os.path.join(upload_dir, thumb_name)
    # thumb_name = 'thumb' + os.path.splitext(thumb.filename)[1]
    # with open(thumb_path, 'wb') as buffer:
    #     shutil.copyfileobj(thumb.file, buffer)


    img_file = PIL.Image.open(thumb.file)
    img_file.thumbnail((400, 400)) # この関数は元の画像を直接リサイズする
    # img_file.save(thumb_path, 'webp')

    img_file.save(thumb_path, quality=95)

    # img_file.save(thumb_path, 'png')


    return json.dumps({
        'uploaded_path': dir_id + '/' + video.filename
    })



### ローカルからの動画アップロード(FROM LOCAL)###
@router.post('/api/pypost_test')
async def pypost_test(
    request: Request,
    file: bytes = File(...),
    # ここでのPydanticモデルは不可。HTTPの制約上、Form-dataとjsonの共存が出来ないため。
):
    form = await request.form()
    filename:str = form['file'].filename # UploadFileObject
    dir_id = form['username'] + form['original_name']

    upload_dir = 'storage/video/public/' + dir_id + '/'
    if os.path.exists(upload_dir) == False : os.makedirs(upload_dir)
    saveVideoPath = os.path.join(upload_dir, filename)
    with open(saveVideoPath, 'wb') as buffer:
        buffer.write(file)
        print(saveVideoPath)
    print('posted: ' + filename)
    return True

class VideoRegisterModel(BaseModel):
    username: str
    filename: str
    duration: int
@router.post('/api/pypost_rdb')
async def pypost_rdb (
    item: VideoRegisterModel,
    db: Session = (Depends(yf_psql.get_db))
):
    dir_id = item.username + item.filename
    timestamp = datetime.datetime.now()

    check = yf_psql_video_crud.check_duplicated_user_video(db, dir_id)
    if check:
        yf_psql_video_crud.register_video(
            db, title=item.filename,
            dir_id=dir_id, username=item.username, 
            duration=item.duration, datetime=timestamp
        )
    else:
        print('duplicated : ' + item.filename)
        return 'duplicated'

    print('rdb posted: ' + dir_id)
    return json.dumps({
        'uploaded': dir_id + '/' + item.filename
    })


class Sentence(BaseModel):
    text: str
@router.post('/api/post_tweet')
def post_tweet(
    message: Sentence,
    token_user: str = Depends(yf_auth.authorize_user_token)
    ):
    yf_sqlite.insert_text(message.text, token_user['user'])
    return

@router.get('/api/get_newpost')
def get_newpost(current_id: Optional[int]=1):
    # print(current_id)
    # if current_id == 0 :
    #     current_id = yf_sqlite.get_newest_id() -RECENT_NUMBER
    text_list= yf_sqlite.get_newpost(id_from=current_id)
    newest_id = yf_sqlite.get_newest_id()
    # print(newest_id)
    # print(text_list)
    return json.dumps({
        'textlist': text_list, 'newest_id': newest_id,
    })


# アップロードされた画像を取得
@router.get('/api/get_images')
async def get_images():
    # dir = './storage'
    fileList = glob.glob('./storage/*.[PpJj][NnPp][GgGg]')
    # images = sorted([p for p in dir.glob('**/*') if re.search('/*\.(jpg|jpeg|png|gif|bmp)', str(p))])
    # print(files)
    return json.dumps({
        'fileList': fileList
    })

# 画像アップロード Upload Picture
@router.post('/api/image_upload/')
async def image_upload(
    background_tasks: BackgroundTasks,
    image: UploadFile=File(...)
):
    upload_dir = './storage'
    saveImageName = image.filename
    # saveImageName = uuid.uuid4().hex + image.filename
    saveImagePath = os.path.join(upload_dir, saveImageName)
    with open(saveImagePath, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
    filepath = os.path.join('storage/', saveImageName)

    return FileResponse(saveImagePath, filename=filepath)



### Cover Art Replacer (embed image on mp3) ###
@router.post('/api/embed_image_on_mp3')
async def embed_image_on_audio(
    background_tasks: BackgroundTasks,
    audio: UploadFile=File(...),
    image: UploadFile=File(...),
    token: str = Form(...),
):
    upload_dir = './yf_tmpfs' # tmpfsを使う　Linuxサーバーで用意している想定
    
    ## 画像ファイルの保存
    saveImageName = uuid.uuid4().hex + image.filename
    saveImagePath = os.path.join(upload_dir, saveImageName)
    with open(saveImagePath, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    ## mp3ファイルの保存
    saveAudioName = uuid.uuid4().hex + audio.filename
    saveAudioPath = os.path.join(upload_dir, saveAudioName)
    with open(saveAudioPath, 'wb')as buffer:
        shutil.copyfileobj(audio.file, buffer)

    ## eyed3で置き換え
    eyed3_mymodule.embed_image_on_mp3(saveAudioPath, saveImagePath, image.content_type)

    ## ファイル削除
    # background_tasks.add_task(os.remove(saveAudioPath), saveAudioPath)
    # ↑ これだと即時実行してしまう。↓ だと、return後に関数が動き始める。
    background_tasks.add_task(remove_tempfile, saveAudioPath)
    background_tasks.add_task(remove_tempfile, saveImagePath)

    return FileResponse(saveAudioPath, filename=audio.filename)





# @router.get('/api/get_total')
# def get_total():
#     total = yf_sqlite.get_newest_id()
#     return json.dumps({
#         'total': total
#     })

# アップロードされた画像のURIを取得
# @router.get('/api/get_uri_list')
# def get_uri_list():
#     uri_list = yf_sqlite.get_uri_list()
#     return json.dumps({
#         'datalist': uri_list
#     })

### old ###

'''
# RDBにアクセスして、画像の情報を拾ってくる
@router.get('/api/rdb_image_uri')
def get_img_uris(
):
    img_list = []
    img_list = yf_psql.get_uri_list()
    return json.dumps({
        'img_list': img_list
    })

# RDBから取得したフロントのリストが、重複するかをチェックする
# 後回し
@router.get('/api/dup_check')
def dupcheck():
    img_list = []
    img_list
    return

### S3 署名
@router.get('/api/sign_s3')
def sign_s3(
    file_name: str,
    file_type: str
):
    s3_bucket = os.environ.get('S3_BUCKET')
    s3_dirname = 'image-uploader'
    region_name = 'ap-northeast-1'
    s3 = boto3.client('s3')
    presigned_post = s3.generate_presigned_post(
        Bucket = s3_bucket,
        Key = f'{s3_dirname}/{file_name}',
        Fields = {
            "acl": "public-read",
            "Content-Type": file_type ,
           },
        Conditions = [
            {"acl": "public-read"},
            {"Content-Type": file_type},
       ],
        ExpiresIn = 3600
    )

    uri = 'https://%s.s3.%s.amazonaws.com/%s' % (s3_bucket, region_name, s3_dirname+'/'+file_name)

    # 重複チェックせずRESTブチ込む
    # (RDB側で一応重複は弾くがムダ通信多い)
    yf_psql.insert_stmt( uri, datetime.datetime.now() )

    return json.dumps({
        'data': presigned_post,
        'url': uri
    })


'''