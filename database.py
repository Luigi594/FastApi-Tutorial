from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

from config import config

metadata = MetaData()

post_table = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("image_url", String, nullable=True),
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
    Column("confirmed", Boolean, default=False),
)

likes_table = Table(
    "likes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("post_id", ForeignKey("posts.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)

# check_same_thread just for sqlite
engine = create_engine(config.DATABASE_URL, pool_size=3, max_overflow=0)

metadata.create_all(engine)
