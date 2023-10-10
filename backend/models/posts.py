from pydantic import BaseModel


# data income
class UserPostIn(BaseModel):
    body: str


# data outcome
class UserPost(UserPostIn):
    id: int


# data income
class CommentsIn(BaseModel):
    body: str
    post_id: int


# data outcome
class Comments(CommentsIn):
    id: int


# data outcome with comments
class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comments]


# just for testing, later we will use a database
post_table = {}
comment_table = {}
