from pydantic import BaseSettings, IPvAnyAddress, PostgresDsn, EmailStr


class Settings(BaseSettings):
    host: IPvAnyAddress = '0.0.0.0'
    port: int = 8000
    secret: str  # openssl rand -hex 32
    postgres_url: PostgresDsn
    token_lifetime: int = 15
    system_username: str = 'admin'
    system_pwd: str = 'admin'
    system_email: EmailStr = 'ernest@elitvinenko.tech'

    class Config:
        env_file = '.env'


Config = Settings()


