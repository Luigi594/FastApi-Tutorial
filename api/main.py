from fastapi import FastAPI
from models.users import User

# Create the FastAPI app
# accessing the FastAPI class from the fastapi package
# initial context
app = FastAPI()

# uvicorn main:app --reload -> run the server
# http://127.0.0.1:8000/docs -> swagger documentation

user_lists = [
    User(
        id=1,
        username="luigi",
        email="luigi@gmail.com",
        full_name="Luigi",
        disabled=False,
        url="https://www.google.com",
        age=20,
    ),
    User(
        id=2,
        username="luigi",
        email="luigi@gmail.com",
        full_name="Luigi",
        disabled=False,
        url="https://www.google.com",
        age=20,
    ),
    User(
        id=3,
        username="luigi",
        email="luigi@gmail.com",
        full_name="Luigi",
        disabled=False,
        url="https://www.google.com",
        age=20,
    ),
]


# Create a route
@app.get("/users")
# every call to a server is async
async def home():
    return user_lists


def search_user(user_id: int):
    user = filter(lambda user: user.id == user_id, user_lists)

    try:
        return list(user)[0]
    except:
        return {"message": "User not found"}


# query path parameter
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return search_user(user_id)


# query string parameter ?key=value
@app.get("/user-query")
async def get_user(user_id: int):
    return search_user(user_id)


@app.post("/new-user")
async def create_user(user: User):
    existing_user = search_user(user.id)

    # if the user exists and is a User object
    if type(existing_user) == User:
        return {"message": "User already exists"}
    else:
        user_lists.append(user)
        return user


@app.put("/update-user/{user_id}")
async def update_user(user_id: int, user: User):
    existing_user = search_user(user_id)

    user_lists[existing_user.id] = user

    return {"message": "User updated successfully"}


@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: int):
    existing_user = search_user(user_id)

    if type(existing_user) == User:
        user_lists.remove(existing_user)
        return {"message": "User deleted successfully"}
