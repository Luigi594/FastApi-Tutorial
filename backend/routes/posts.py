import logging

from database import comment_table, engine, post_table
from fastapi import APIRouter, HTTPException
from models.posts import CommentsIn, UserPostIn
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from utils.find_post import find_post

router = APIRouter()
logger = logging.getLogger(__name__)


# response_model=list[UserPost] -> return a list of UserPost
@router.get("/")
async def get_posts():
    logger.info("Getting all posts")

    query = select(post_table)

    logger.debug(query)

    with Session(engine) as session:
        result = session.execute(query)
        json_result = [dict(zip(result.keys(), row)) for row in result]
        session.close()

        return {"posts": json_result}


@router.post("/new", status_code=201)
async def create_post(post: UserPostIn):
    logger.info("Creating a new post")

    # model_dump Generate a dictionary representation of the model, optionally
    # specifying which fields to include or exclude
    data = post.model_dump()
    query_insert = insert(post_table).values(**data)

    with Session(engine) as session:
        try:
            result = session.execute(query_insert)

            logger.debug(result)

            session.commit()

            return {**data, "id": result.inserted_primary_key[0]}
        except Exception as e:
            session.rollback()
            raise e


# create new comments
@router.post("/new-comment", status_code=201)
async def create_comment(comment: CommentsIn):
    post = await find_post(comment.post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    query_insert = insert(comment_table).values(**data)

    with Session(engine) as session:
        try:
            result = session.execute(query_insert)
            session.commit()

            return {**data, "id": result.inserted_primary_key[0]}
        except Exception as e:
            session.rollback()
            raise e


# return the comments of a post
@router.get("/post/{post_id}/comments")
async def get_comments_on_post(post_id: int):
    query = select(comment_table).where(comment_table.c.post_id == post_id)

    with Session(engine) as session:
        result = session.execute(query)

        json_result = [dict(zip(result.keys(), row)) for row in result]

        session.close()

        return json_result


# return a post with comments
@router.get("/post/{post_id}")
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)

    comments = await get_comments_on_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post": post, "comments": comments}
