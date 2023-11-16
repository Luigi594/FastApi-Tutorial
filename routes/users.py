import logging

from database import engine, user_table
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from models.users import UserIn
from security.security import (
    authenticate_user,
    create_access_token,
    create_confirmation_token,
    get_password_hash,
    get_user,
)
from sqlalchemy import insert, update
from sqlalchemy.orm import Session
from utils.get_subject_for_token_type import get_subject_for_token_type
from utils.send_email import send_user_registration_email

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn, background_task: BackgroundTasks, request: Request):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    query = insert(user_table).values(
        email=user.email, password=get_password_hash(user.password)
    )

    logger.debug(query)

    with Session(engine) as session:
        try:
            session.execute(query)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            raise e

    # send the email as a background task, so this
    # endpoint can return a response without waiting
    background_task.add_task(
        send_user_registration_email,
        user.email,
        confirmation_url=request.url_for(
            "confirm_email", token=create_confirmation_token(user.email)
        ),
    )

    return {"message": "User created successfully"}


# endpoint for confirming the email registration
@router.get("/confirm/{token}")
async def confirm_email(token: str):
    email = get_subject_for_token_type(token, "confirmation")

    query = update(user_table).where(user_table.c.email == email).values(confirmed=True)

    with Session(engine) as session:
        try:
            session.execute(query)
            session.commit()
            session.close()
            return {"message": "Email confirmed successfully"}
        except Exception as e:
            session.rollback()
            raise e


@router.post("/login")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
