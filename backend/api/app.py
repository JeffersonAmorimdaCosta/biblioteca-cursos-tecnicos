from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK)
async def hello():
    return {'message': 'Hello World!'}
