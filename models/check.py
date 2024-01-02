import psycopg


def check_db_connection(db_url: str) -> bool:
    try:
        connection = psycopg.connect(db_url)
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        return True
    except psycopg.DatabaseError as error:
        return False
