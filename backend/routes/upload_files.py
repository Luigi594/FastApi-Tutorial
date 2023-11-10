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

import tempfile

from fastapi import APIRouter, HTTPException, UploadFile, status
from utils.b2 import b2_upload_file

router = APIRouter()

# define the chunk size
CHUNK_SIZE = 1024 * 1024  # 1MB


@router.post("/", status_code=201)
async def upload_file(file: UploadFile):
    # in order to get the next chunk:
    # reads the chunk that has already been uploaded
    # for as long as the chunk is still uploading from the
    # client, the data is still reaching our server

    # then when this is all done it will give us a variable
    # that we can later store in a file

    try:
        with tempfile.NamedTemporaryFile(mode="wb") as temp_file:
            filename = temp_file.name  # the temporary file name

            # while the file is uploading, we will read the chunks
            while content := await file.read(CHUNK_SIZE):
                temp_file.write(content)

            file_url = b2_upload_file(local_file=filename, file_name=file.filename)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading file",
        ) from e

    return {"detail": f"Successfully uploaded {file.filename}", "file_url": file_url}
