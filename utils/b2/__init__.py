import logging
from functools import lru_cache

import b2sdk.v2 as b2
from config import config

logger = logging.getLogger(__name__)


# to connect with the B2 API
@lru_cache()
def b2_get_api():
    logger.debug("Connecting to B2 API")

    info = b2.InMemoryAccountInfo()
    b2_api = b2.B2Api(info)

    b2_api.authorize_account("production", config.B2_KEY_ID, config.B2_APPLICATION_KEY)

    return b2_api


# to get the bucket name
@lru_cache()
def b2_get_bucket(api: b2.B2Api):
    bucket_name = api.get_bucket_by_name(config.B2_BUCKET_NAME)
    print(f"Getting bucket {bucket_name}")
    return bucket_name


# this one is for actually upload the file and then
# return the URL so we can use it in the frontend
def b2_upload_file(local_file: str, file_name: str) -> str:
    api = b2_get_api()

    logger.debug("Uploading file to B2")

    uploaded_file = b2_get_bucket(api).upload_local_file(
        local_file=local_file,
        file_name=file_name,
    )

    download_url = api.get_download_url_for_fileid(uploaded_file.id_)

    return download_url
