from database import engine, post_table
from sqlalchemy import select
from sqlalchemy.orm import Session


async def find_post(post_id: int):
    query = select(post_table).where(post_table.c.id == post_id)

    with Session(engine) as session:
        result = session.execute(query)
        return result.scalars().first()
