from fastapi import FastAPI
from routes.posts import router as posts_router

# Create the FastAPI app
# accessing the FastAPI class from the fastapi package
# initial context
app = FastAPI()

# uvicorn main:app --reload -> run the server
# http://127.0.0.1:8000/docs -> swagger documentation


# Starting the Udemy course
app.include_router(posts_router, prefix="/posts")
