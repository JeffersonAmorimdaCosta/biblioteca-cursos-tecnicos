from http import HTTPStatus

from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post('/files/uploads', status_code=HTTPStatus.CREATED)
async def upload_files(files: UploadFile):
    return True
