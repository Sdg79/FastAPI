# Con las nuevas especificacinoes de JWT y pwdlib[argon2]

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

router = APIRouter(
    prefix="/jwtauth2",
    tags=["jwtauth2"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = PasswordHash.recommended()

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$OTVkMzNiYTM2ZmE1NjdkYjUwYjE3OTI1NGIwYzdlYjM$h/OgXKESyS61H7IvKLHRaET4abEWX+B3JvMm9qipgrM"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$NzY2NjBmNzEyOTVkMzU4M2YyNzFlZGJjYjc5N2QxMTU$fQtjDxFCieCDNht1fk+D0P9Zue5VML8X1emfRjTykjA"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except InvalidTokenError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub": user.username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user