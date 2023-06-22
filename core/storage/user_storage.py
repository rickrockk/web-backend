from .base_storage import BaseStorage


class UserStorage(BaseStorage):
    @classmethod
    def get_user_via_id(cls, user_id: int):
        pass

    @classmethod
    def get_user_via_email(cls, email: str):
        pass

    @classmethod
    def get_user_via_username(cls, username: str):
        pass

    @classmethod
    def get_user_via_phone_number(cls, phone: str):
        pass

    @classmethod
    def login_user(cls, user_id: int, password: str) -> bool:
        pass

    @classmethod
    def get_current_user_via_token(cls, token: str):
        # payload = decode_access_token
        pass
