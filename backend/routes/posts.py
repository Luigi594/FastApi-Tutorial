from fastapi import APIRouter, HTTPException
from models.posts import (
    Comments,
    CommentsIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
    comment_table,
    post_table,
)
from utils.find_post import find_post

router = APIRouter()


@router.get("/", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())


@router.post("/new", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    # model_dump Generate a dictionary representation of the model, optionally
    # specifying which fields to include or exclude
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post

    return new_post


# create new comments
@router.post("/new-comment", response_model=Comments, status_code=201)
async def create_comment(comment: CommentsIn):
    post = find_post(comment.post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment

    return new_comment


# return the comments of a post
@router.get("/post/{post_id}/comments", response_model=list[Comments])
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


# return a post with comments
@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post": post, "comments": await get_comments_on_post(post_id)}
