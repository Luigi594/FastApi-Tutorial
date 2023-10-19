import logging

from database import engine, user_table
from fastapi import APIRouter, HTTPException, status
from models.users import UserIn
from security.security import get_user
from sqlalchemy import insert
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    query = insert(user_table).values(email=user.email, password=user.password)

    logger.debug(query)

    with Session(engine) as session:
        try:
            session.execute(query)
            session.commit()

            return {"message": "User created successfully"}
        except Exception as e:
            session.rollback()
            raise e
