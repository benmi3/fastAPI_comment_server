import os
import psycopg

db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('POSTGRES_HOST')
db_name = os.environ.get('POSTGRES_DB')
db_port = os.environ.get('POSTGRES_PORT')
db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


def check_db_connection() -> bool:
    try:
        connection = psycopg.connect(db_url)
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        return True
    except psycopg.DatabaseError as error:
        return False


def setup_comment_table():
    # Connect to an existing database
    with psycopg.connect(db_url) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("""
                    CREATE TABLE comment_table (
                        id serial PRIMARY KEY,
                        cid integer,
                        comment text,
                        post_slug text)
                        IF NOT EXISTS
                    """)

            conn.commit()


def insert_comment(comment: str, post: str, author: str):
    # Connect to an existing database
    with psycopg.connect(db_url) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE test (
                    id serial PRIMARY KEY,
                    num integer,
                    data text)
                """)

            # Pass data to fill a query placeholders and let Psycopg perform
            # the correct conversion (no SQL injections!)
            cur.execute(
                "INSERT INTO test (num, data) VALUES (%s, %s)",
                (100, "abc'def"))

            # Query the database and obtain data as Python objects.
            cur.execute("SELECT * FROM test").fetchall()
            # will return (1, 100, "abc'def")

            # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
            # of several records, or even iterate on the cursor
            for record in cur:
                print(record)

            # Make the changes to the database persistent
            conn.commit()


async def select_comments(post: str):
    async with await psycopg.AsyncConnection.connect(db_url) as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "INSERT INTO test (num, data) VALUES (%s, %s)",
                (100, "abc'def"))
            await acur.execute("SELECT * FROM test")
            await acur.fetchall()
            # will return (1, 100, "abc'def")
            async for record in acur:
                print(record)
