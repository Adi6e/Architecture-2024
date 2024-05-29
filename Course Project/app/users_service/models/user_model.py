from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: int
    user_login: str
    user_name: str
    user_surname: str
    user_password: str


class NewUserModel(BaseModel):
    user_login: str
    user_name: str
    user_surname: str
    user_password: str


class UpdateUserModel(BaseModel):
    user_id: int
    user_login: str | None = None
    user_name: str | None = None
    user_surname: str | None = None
    user_password: str | None = None
