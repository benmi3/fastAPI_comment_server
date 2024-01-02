import psycopg


def setup_user_table(db_url: str):
    # Connect to an existing database
    with psycopg.connect(db_url) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("""
                    CREATE TABLE user_table (
                        id serial PRIMARY KEY,
                        cid integer,
                        user_name text,
                        user_pass text,
                        user_salt text,
                        user_pepper text,
                        created_at timestamp,
                        updated_at timestamp)
                        IF NOT EXISTS
                    """)

            conn.commit()


def insert_user(db_url: str, comment: str, post: str, author: str):
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


async def select_user(db_url: str, username: str):
    async with await psycopg.AsyncConnection.connect(db_url) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT * FROM user_table",
                (100, "abc'def"))
            user_data = await cur.fetchone()
    if user_data is None:
        return False
    else:
        return user_data


def get_all_users():
    return None