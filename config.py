from pydantic import BaseSettings, IPvAnyAddress, PostgresDsn, EmailStr, HttpUrl


class Settings(BaseSettings):
    host: IPvAnyAddress = '0.0.0.0'
    port: int = 8000
    secret: str  # openssl rand -hex 32
    postgres_url: PostgresDsn
    token_lifetime: int = 15
    system_username: str = 'admin'
    system_pwd: str = 'admin'
    system_email: EmailStr = 'ernest@elitvinenko.tech'
    vk_oauth_link: HttpUrl = 'https://oauth.vk.com/authorize'
    vk_app_id: int
    vk_secret_key: str
    vk_service_key: str
    vk_api_version: str
    domain: str

    class Config:
        env_file = '.env'


Config = Settings()


