# tempfile, allows to create temporary files before upload it
# into the B2 bucket. Then the file is deleted.

# so the flow is the following:
# client -> server (tempfile) -> B2 bucket -> delete tempfile

# aiofiles, saving what the user sends us in async mode
# the UploadFile from fastapi is a special class that
# allows us to handle files in a very easy way:

# the client split up file into chunks
# the clients sends up chunks 1 at a time
# the last chunk, fastapi will put all the chunks into a single file
# finally will delete the chunks

import os

from fastapi import APIRouter, HTTPException, UploadFile, status
from utils.b2 import b2_upload_file

router = APIRouter()

# define the chunk size
CHUNK_SIZE = 1024 * 1024  # 1MB

# custom temp folder to avoid to write in temp folder from Windows Os
# sooo didn't workout with tempfile, so that's why I'm using this
CUSTOM_TEMP_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")


@router.post("/", status_code=201)
async def upload_file(file: UploadFile):
    # in order to get the next chunk:
    # reads the chunk that has already been uploaded
    # for as long as the chunk is still uploading from the
    # client, the data is still reaching our server

    # then when this is all done it will give us a variable
    # that we can later store in a file

    try:
        file_path = os.path.join(CUSTOM_TEMP_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            while content := await file.read(CHUNK_SIZE):
                buffer.write(content)

        # upload the file to the B2 bucket
        file_url = b2_upload_file(local_file=file_path, file_name=file.filename)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while uploading file",
        )
    finally:
        # delete the file from the temp folder
        os.remove(file_path)

    return {"detail": f"Successfully uploaded {file.filename}", "file_url": file_url}
