import os

from . import check
from . import comment
from . import user

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
    # Check if all necessary envir variables has been set
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

async def insert(user_name: str, user_auth: str) -> bool:
    if not check.check_db_connection(db_url):
        return False

    user_data = await user.select_user(user_name=user_name)