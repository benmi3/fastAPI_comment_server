import os

from . import check
from . import comment
from . import user
from . import auth

db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('POSTGRES_HOST')
db_name = os.environ.get('POSTGRES_DB')
db_port = os.environ.get('POSTGRES_PORT')

try:
    # set db_url as global
    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
except TypeError:
    db_url = "sqlite3.db"


async def check_db():
    # Check if all necessary environ variables has been set
    if None in [db_user, db_pass, db_host, db_port]:
        return False
    # Check if you can connect to the database
    if not check.check_db_connection(db_url):
        return False
    # If table does not exist, create it
    # User
    if not user.setup_user_table(db_url):
        return False
    # Comment
    if not comment.setup_comment_table(db_url):
        return False

    return True


def select_all_users() -> list:
    if not check.check_db_connection(db_url):
        return ["",]

    return user.get_all_users()


async def select_all_comments(post: str) -> list:
    if not check.check_db_connection(db_url):
        return ["",]

    return await comment.select_comments(db_url= db_url, post=post)


async def auth_check(user_name: str, user_auth: str) -> int:
    if not check.check_db_connection(db_url):
        return 0

    user_data = await user.select_user(
        db_url=db_url,
        username=user_name)

    if not user_data:
        print("ERROR: User not found")
        return 0

    if not auth.authenticate(
            pdw=user_data[2],
            pdw_password=user_data[3],
            admin=user_data[4],
            auth_token=user_auth):
        print("ERROR: Failed because of authentication error")
        return 0
    # User ID
    return user_data[0]


async def insert_comment(user_name: str, user_auth: str, text: str) -> bool:
    user_id = await auth_check(user_name, user_auth)
    if user_id <= 999:
        # Tables starts the id at 1000
        # so if the answer is 999 or lower
        # something happened in the auth_check
        return False

    if comment.insert_comment(db_url=db_url, cid=user_name, text=text):
        return True

    return False


async def delete_comment(user_name: str, user_auth: str, id: int):
    if not auth_check(user_name, user_auth):
        return False
    