from pydantic import BaseModel, ConfigDict


# data income
class UserPostIn(BaseModel):
    body: str


# data outcome
class UserPost(UserPostIn):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class UserPostWithLikes(UserPost):
    likes: int
    model_config = ConfigDict(from_attributes=True)


# data income
class CommentsIn(BaseModel):
    body: str
    post_id: int


# data outcome
class Comments(CommentsIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


# data outcome with comments
class UserPostWithComments(BaseModel):
    post: UserPostWithLikes
    comments: list[Comments]


class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    id: int
    user_id: int
