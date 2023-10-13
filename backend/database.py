from config import config
from databases import Database
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

metadata = MetaData()

post_table = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
)

comment_table = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("post_id", ForeignKey("posts.id"), nullable=False),
)


# check_same_thread just for sqlite
engine = create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

metadata.create_all(engine)

database = Database(config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK)
