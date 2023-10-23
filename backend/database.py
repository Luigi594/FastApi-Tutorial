from config import config
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
    Column("user_id", ForeignKey("users.id"), nullable=False),
)

comment_table = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("post_id", ForeignKey("posts.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True),
    Column("password", String),
)

likes_table = Table(
    "likes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("post_id", ForeignKey("posts.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)

# check_same_thread just for sqlite
engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)
