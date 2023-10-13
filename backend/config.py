from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    # dev, test or prod environment
    ENV_STATE: Optional[str] = None
    # the name of our file that contains the variables
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# don't allow Pydantic to read the database connection string
class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None

    # for every test the database is cleared
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")

    # final variable for database -> DEV_DATABASE_URL
    # pydantic is going to look for dev_ and then use the rest
    # of the variable name from GlobalConfig


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


# what we're doing here is to make this function cachable
# so if we change the environment state, it will not call again this
# function, it will just return the cached value
@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}

    # if the env_state value is dev, it will access to the DevConfig Class
    # and then it will create an object of that class
    return configs[env_state]()


# loads the .env file and get the configuration
config = get_config(BaseConfig().ENV_STATE)
