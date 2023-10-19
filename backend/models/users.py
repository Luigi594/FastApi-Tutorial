from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    email: str


class UserIn(User):
    password: str


# we defined these models differently
# from posts model because we don't want to return the password
