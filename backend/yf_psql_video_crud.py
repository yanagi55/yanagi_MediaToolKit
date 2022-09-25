from enum import auto, unique
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from sqlalchemy import Boolean, Column, Integer, String,Text, DateTime
from sqlalchemy.orm import relationship
from backend.yf_api import video_upload
# from sqlalchemy.sql.operators import exists
from yf_psql import Base
import yf_psql
from fastapi import Depends
# import uuid

### models ###
class VideoModel(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dist = Column(Text, unique=True, index=True)
    title = Column(Text, unique=False, index=True)
    username = Column(Text, unique=False, index=True)
    duration = Column(Integer, unique=False, index=True)
    playcount = Column(Integer, unique=False, index=True)
    datetime = Column(DateTime, unique=False, index=True)

## CRUD ###

def get_video_list(
    db: Session = Depends(yf_psql.get_db),
):
    dist_list = db.query(
        VideoModel.dist, VideoModel.title,
        VideoModel.username, VideoModel.duration,
        VideoModel.playcount, VideoModel.datetime
    ).all()
    return dist_list

def check_duplicated_user_video(
    db: Session, input_dist: str
) -> bool:
    exists_dist = db.query(VideoModel.dist).filter(VideoModel.dist == input_dist) \
        .scalar() is not None
    if exists_dist: return False
    return True

def register_video(
    db: Session,
    title: str, username:str,
    dir_id: str, duration: int,
    datetime: DateTime
) -> bool:

    video = VideoModel()
    video.dist = dir_id
    # video.dist = input_username + '-' + input_title
    # video.dist = uuid.uuid4().hex
    video.title = title
    video.username = username
    video.duration = duration
    video.datetime = datetime
    video.playcount = 0

    db.add(video)
    db.commit()

    return True

# def check_duplicated_user(
#     db: Session, input_email: str, input_name:str
# ) -> bool:
#     exists_email = db.query(UserModel.email).filter(UserModel.email == input_email) \
#             .scalar() is not None
#     if exists_email: return False
#     exists_username = db.query(UserModel.name).filter(UserModel.name == input_name) \
#             .scalar() is not None
#     if exists_username : return False
#     return True


