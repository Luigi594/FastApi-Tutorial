import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from database import engine
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from loggin_conf import configure_loggin
from routes.posts import router as posts_router
from routes.upload_files import router as upload_files_router
from routes.users import router as users_router

logger = logging.getLogger(__name__)


# connect to the database before requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as connection:
        configure_loggin()
        connection
        yield
        connection.close()


# Create the FastAPI app
# accessing the FastAPI class from the fastapi package
# initial context
app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

# uvicorn main:app --reload -> run the server
# http://127.0.0.1:8000/docs -> swagger documentation


# Starting the Udemy course
app.include_router(posts_router, prefix="/posts")
app.include_router(users_router, prefix="/users")
app.include_router(upload_files_router, prefix="/uploads")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
