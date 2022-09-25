from re import A
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials, APIKeyHeader, APIKeyCookie
from jose import JWTError, jwt
import json
import datetime
import yf_psql_user_crud
import yf_psql
import urllib.parse

router = APIRouter()
security = HTTPBasic()


### AUTH SETTINGS ###
MY_PKEY = 'aaa'
TOKEN_EXPIRE_MIN = 60

### AUTHENTICATE USER 認証 ###   
async def authenticate_user(
    db: Session = Depends(yf_psql.get_db),
    credentials: HTTPBasicCredentials = Depends(security)
):
    user = yf_psql_user_crud.authenticate_user(db, credentials.username, credentials.password)
    if user:
        payload = {
            'exp':  datetime.datetime.utcnow() \
                 + datetime.timedelta(minutes=TOKEN_EXPIRE_MIN),
            'email': user.email.rstrip(),
            'user': user.name.rstrip()
        }
        token = jwt.encode(payload, MY_PKEY)
        print('(Login Authenticated) username: ' + user.name.rstrip())
        return {"access_token": token, "identified name": user.name.rstrip() }
    else:
        raise HTTPException(status_code=401,detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"})

### AUTHORIZE TOKEN 認可 ###
api_key = APIKeyCookie(name="yf_token", auto_error=False)
# api_key = APIKeyHeader(name="Authorization", auto_error=False)
async def authorize_user_token( authorization: str = Depends(api_key) ):
    credientials_exception = HTTPException(
        status_code=401,
        detail="Could not validate token",
        # headers={"WWW-Authenticate": authorization},
    )
    authorization = urllib.parse.unquote(authorization) # Cookieの場合はURLデコードする

    if authorization: auth = authorization.split(" ")
    if len(auth) != 2: raise credientials_exception
    if auth[0] != "Bearer": raise credientials_exception

    id_token = auth[1]
    try:
        payload = jwt.decode(id_token, MY_PKEY, algorithms="HS256")
    except Exception:
        raise credientials_exception

    print('(Token Authorized) username:' + payload['user'])
    return {"user": payload["user"], "email": payload["email"]}


