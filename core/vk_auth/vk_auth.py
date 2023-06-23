import urllib.parse
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from config import Config
from models.schemas.user_schemas import UserRegisterVkSchema
from ..storage.user_storage import UserStorage
from ..auth.jwt import create_access_token

router = APIRouter(prefix='/api/oauth/vk')


@router.get('/')
async def generate_link():
    link = Config.vk_oauth_link
    params = {
        "client_id": Config.vk_app_id,
        "redirect_uri": Config.domain + "api/oauth/vk/callback",
        "scope": 2 ** 22 + 2 ** 28,
        "response_type": "code"
    }
    url = link + '?' + urllib.parse.urlencode(params)
    return RedirectResponse(url)


@router.get('/callback')
async def vk_callback(code: str):
    data = requests.get(
        f'https://oauth.vk.com/access_token?client_id={Config.vk_app_id}&client_secret={Config.vk_secret_key}&redirect_uri={Config.domain + "api/oauth/vk/callback"}&code={code}').json()
    access_token = data['access_token']
    vk_id = data['user_id']
    email = data['email']

    # CALL VK API
    data = requests.post('https://api.vk.com/method/users.get', data={
        "access_token": access_token,
        "v": Config.vk_api_version,
        "user_ids": vk_id
    }).json()['response'][0]

    full_name = data["first_name"] + " " + data['last_name']

    user = UserRegisterVkSchema(name=full_name, email=email, vk_id=vk_id)
    user = await UserStorage.get_or_create_user_via_vk(user)

    access_token = create_access_token(data={"sub": user.vk_id, "authType": "vk"})
    return {"access_token": access_token, "token_type": "bearer"}
