import psycopg


def setup_comment_table(db_url: str) -> bool:
    # Connect to an existing database
    with psycopg.connect(db_url) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("""
                    CREATE TABLE comment_table (
                        id serial PRIMARY KEY,
                        cid integer,
                        text text,
                        post_slug text,
                        created_at timestamp,
                        updated_at timestamp)
                        IF NOT EXISTS
                    """)

            conn.commit()
    return True


async def select_comments(db_url: str, post: str) -> list:
    async with await psycopg.AsyncConnection.connect(db_url) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT cid,
                text,
                created_at,
                updated_at FROM comment_table WHERE post_slug = %s """,
                post)
            await cur.fetchall()
            async for record in cur:
                print(record)
    return [cur]


async def insert_comment(db_url: str, comment: str, post: str, author: str):
    # Connect to an existing database
    async with await psycopg.AsyncConnection.connect(db_url) as conn:
        # Open a cursor to perform database operations
        async with conn.cursor() as cur:
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
