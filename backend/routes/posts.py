import logging
from typing import Annotated

from database import comment_table, engine, likes_table, post_table
from fastapi import APIRouter, Depends, HTTPException
from models.posts import (
    Comments,
    CommentsIn,
    PostLikeIn,
    UserPostIn,
    UserPostWithComments,
)
from models.users import User
from security.security import get_current_user
from sqlalchemy import desc, insert, select
from sqlalchemy.orm import Session
from utils.find_post import find_post
from utils.post_with_likes import base_query, select_post_and_likes
from utils.sorting_posts import PostSorting

router = APIRouter()
logger = logging.getLogger(__name__)


# response_model=list[UserPost] -> return a list of UserPost
@router.get("/", response_model=dict)
async def get_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    sorting: PostSorting = PostSorting.new,
):
    logger.info("Getting all posts")

    if sorting == PostSorting.new:
        query = base_query.order_by(post_table.c.id.desc())

    elif sorting == PostSorting.old:
        query = base_query.order_by(post_table.c.id.asc())

    else:
        query = base_query.order_by(desc("likes"))

    logger.debug(query)

    with Session(engine) as session:
        result = session.execute(query)
        json_result = [dict(zip(result.keys(), row)) for row in result]
        session.close()

        return {"posts": json_result}


@router.post("/new", status_code=201)
async def create_post(
    post: UserPostIn,
    # grab the user authenticated by the token
    current_user: Annotated[User, Depends(get_current_user)],
):
    logger.info("Creating a new post")

    # model_dump Generate a dictionary representation of the model, optionally
    # specifying which fields to include or exclude
    data = {**post.model_dump(), "user_id": current_user.id}
    query_insert = insert(post_table).values(**data)

    with Session(engine) as session:
        try:
            result = session.execute(query_insert)

            logger.debug(result)

            session.commit()
            session.close()
            return {**data, "id": result.inserted_primary_key[0]}
        except Exception as e:
            session.rollback()
            raise e


# create new comments
@router.post("/new-comment", status_code=201)
async def create_comment(
    comment: CommentsIn, current_user: Annotated[User, Depends(get_current_user)]
):
    post = await find_post(comment.post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**comment.model_dump(), "user_id": current_user.id}
    query_insert = insert(comment_table).values(**data)

    with Session(engine) as session:
        try:
            result = session.execute(query_insert)
            session.commit()
            session.close()
            return {**data, "id": result.inserted_primary_key[0]}
        except Exception as e:
            session.rollback()
            raise e


# return the comments of a post
@router.get("/post/{post_id}/comments", response_model=list[Comments])
async def get_comments_on_post(post_id: int):
    query = select(comment_table).where(comment_table.c.post_id == post_id)

    with Session(engine) as session:
        result = session.execute(query)

        json_result = [dict(zip(result.keys(), row)) for row in result]

        session.close()

        return json_result


# return a post with comments
@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await select_post_and_likes(post_id)

    comments = await get_comments_on_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post": post, "comments": comments}


# like funcionality for a post
@router.post("/like", status_code=201)
async def like_post(
    liking_post: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Liking a post")

    post = await find_post(liking_post.post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post was not found")

    data = {**liking_post.model_dump(), "user_id": current_user.id}

    query_insert = insert(likes_table).values(**data)

    with Session(engine) as session:
        try:
            result = session.execute(query_insert)
            session.commit()

            session.close()

            return {**data, "id": result.inserted_primary_key[0]}
        except Exception as e:
            session.rollback()
            raise e
