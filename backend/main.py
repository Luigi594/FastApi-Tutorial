from contextlib import asynccontextmanager

from database import database
from fastapi import FastAPI
from routes.posts import router as posts_router


# connect to the database before requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


# Create the FastAPI app
# accessing the FastAPI class from the fastapi package
# initial context
app = FastAPI(lifespan=lifespan)

# uvicorn main:app --reload -> run the server
# http://127.0.0.1:8000/docs -> swagger documentation


# Starting the Udemy course
app.include_router(posts_router, prefix="/posts")
