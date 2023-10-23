import datetime
import logging
from typing import Annotated

from config import config
from database import engine, user_table
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])
secret_key = config.JWT_KEY
algorithm = "HS256"

# the URL where the user can obain a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(email: str):
    logger.debug("Creating a token for the user", extra={"email": email})

    expiration_date = datetime.datetime.now(datetime.UTC.utc) + datetime.timedelta(
        minutes=30
    )

    jwt_data = {"sub": email, "exp": expiration_date}
    encoded_jwt = jwt.encode(jwt_data, key=secret_key, algorithm=algorithm)
    return encoded_jwt


# hash and compare passwords
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str):
    logger.debug("Fetching user from the database", extra={"email": email})

    query = select(user_table).where(user_table.c.email == email)

    with Session(engine) as session:
        result = session.execute(query).first()

        if result:
            return result


async def authenticate_user(email: str, password: str):
    logger.debug("Authenticating user", extra={"email": email})

    user = await get_user(email)

    if not user and not verify_password(password, user.password):
        raise credential_exception

    return user


# Dependency Injection, to not give the token as argument
# we not longer need to call the oauth2_scheme
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, key=secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")

        if email is None:
            raise credential_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credential_exception

    user = await get_user(email=email)

    if user is None:
        raise credential_exception

    return user
