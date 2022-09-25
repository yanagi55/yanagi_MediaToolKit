from enum import auto
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from sqlalchemy import Boolean, Column, Integer, String,Text
from sqlalchemy.orm import relationship
from yf_psql import Base
from fastapi import Depends
import yf_psql

### models ###
class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(Text, unique=True, index=True)
    name = Column(Text, unique=True, index=True)
    hashed_password = Column(Text)
    is_active = Column(Boolean, default=True)


### CRUD ###
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password.rstrip())


def authenticate_user(
    db: Session, email: str, password: str,
    #  expire: int, reuse: bool
):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_password_hash(password) -> str:
    return pwd_context.hash(password)


### Register ###
def check_duplicated_user(
    input_email: str, input_name:str,
    db: Session = Depends(yf_psql.get_db)
) -> bool:
    exists_email = db.query(UserModel.email).filter(UserModel.email == input_email) \
            .scalar() is not None
    if exists_email: return False
    exists_username = db.query(UserModel.name).filter(UserModel.name == input_name) \
            .scalar() is not None
    if exists_username : return False
    return True

def register_user(
    input_email: str, input_name:str, password: str,
    db: Session = Depends(yf_psql.get_db)
) -> bool:

    user = UserModel()
    user.email = input_email
    user.name = input_name
    user.hashed_password = get_password_hash(password)

    db.add(user)
    db.commit()
    return True