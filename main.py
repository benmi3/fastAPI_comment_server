from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
# Local packages
import models


class CommentJson(BaseModel):
    text: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/comment/{post}/")
async def get_comment(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/comment/{post}/")
async def post_comment(post: str, item: CommentJson):
    json_compatible_item_data = jsonable_encoder(item)
    print(post)
    print(json_compatible_item_data)


if __name__ == "__main__":
    if not models.check_db():
        print("Could not get connection to database")
        print("Check environmental variables")
        exit()
