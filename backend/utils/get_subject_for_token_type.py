from typing import Literal

from config import config
from jose import ExpiredSignatureError, JWTError, jwt
from utils.credentials_exception import create_credentials_exception

secret_key = config.JWT_KEY
algorithm = "HS256"


def get_subject_for_token_type(
    token: str, type: Literal["access", "confirmation"]
) -> str:
    try:
        payload = jwt.decode(token, key=secret_key, algorithms=[algorithm])

    except ExpiredSignatureError:
        raise create_credentials_exception("Token has expired")
    except JWTError:
        raise create_credentials_exception("Invalid token")

    email: str = payload.get("sub")

    if email is None:
        raise create_credentials_exception("Token is missing 'sub' field")

    # check the token type is access
    # to not use the confirmation token to access protected endpoints
    token_type = payload.get("type")

    if token_type is None or token_type != type:
        raise create_credentials_exception("Token has incorrect type")

    return email
