from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    disabled: bool
    url: str
    age: int
