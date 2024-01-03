from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
# Local packages
import models


class CommentCreate(BaseModel):
    text: str


class CommentDelete(BaseModel):
    id: int


class UserDisplay(BaseModel):
    text: str


class UserCreate(BaseModel):
    text: str


class UserUpdate(BaseModel):
    text: str
    id: int


class UserDelete(BaseModel):
    id: int


app = FastAPI()


@app.get("/")
async def root():
    # TODO: redirect to desired link?
    # there should be no reason to call root.
    url = "https://google.com"
    return RedirectResponse(
        url, status_code=307, headers=None, background=None
    )


@app.get("/comment/{post}/")
async def get_comment(post: str):
    # This gets all the comments.
    return {"post_id": post}


@app.put("/comment/{post}/")
async def put_comment(post: str, item: CommentCreate):
    # This creates the comment
    json_compatible_item_data = jsonable_encoder(item)
    print(post)
    print(json_compatible_item_data)


@app.delete("/comment/{post}/")
async def delete_comment(post: str, item: CommentDelete):
    # This deletes the comment
    json_compatible_item_data = jsonable_encoder(item)
    print(post)
    print(json_compatible_item_data)


@app.get("/user/")
async def get_user(item: UserDisplay):
    # This gets the info of the user that made the comment
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)


@app.put("/user/")
async def put_user(item: UserCreate):
    # This creates a new user
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)


@app.post("/user/")
async def post_user(item: UserUpdate):
    # This will update the user
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)


@app.delete("/user/")
async def delete_user(item: UserDelete):
    # This will delete the user
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)


if __name__ == "__main__":
    if not models.check_db():
        print("Could not get connection to database")
        print("Check environmental variables")
        exit()
