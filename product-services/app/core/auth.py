from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from requests import get, post 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="product/login")

def get_current_user(token: str):
    url = "http://user-management:8000/user/admin"
    headers = {"Authorization": f"Bearer {token}"}
    response = get(url, headers=headers)
    # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    # user_id: str = str(payload.get("id"))
    if response.status_code == 200:
        return response.json()

    raise HTTPException(status_code=response.status_code)


def login_for_access_token(form_data):
    url = "http://user-management:8000/user/admintoken"
    data = {"username": form_data.username, "password": form_data.password}
    response = post(url, data=data)

    if response.status_code == 200:
        return response.json()

    raise HTTPException(status_code=response.status_code)


AccessTokenDep = Annotated[dict, Depends(oauth2_scheme)]


def get_user_dep(token: AccessTokenDep):
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user = get_current_user(token)
        return user
    except Exception as e:
        print (str(e))


AdminDep = Annotated[Any, Depends(get_user_dep)]


def get_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return login_for_access_token(form_data)
