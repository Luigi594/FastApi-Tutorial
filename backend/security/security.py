import logging

from database import engine, user_table
from sqlalchemy import select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


async def get_user(email: str):
    logger.debug("Fetching user from the database", extra={"email": email})

    query = select(user_table).where(user_table.c.email == email)

    with Session(engine) as session:
        result = session.execute(query).scalars().first()

        if result:
            return result
