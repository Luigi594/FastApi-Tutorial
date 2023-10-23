from database import engine, likes_table, post_table
from sqlalchemy import func, select
from sqlalchemy.orm import Session


async def select_post_and_likes(post_id: int):
    # select_from(post_table).outerjoin(likes_table) ->
    # select * from post_table left join likes_table
    # it's like doing a join in SQL

    query = (
        select(post_table, func.count(likes_table.c.id).label("likes"))
        .select_from(post_table.outerjoin(likes_table))
        .where(post_table.c.id == post_id)
        .group_by(post_table.c.id)
    )

    with Session(engine) as session:
        result = session.execute(query)
        return result.first()
