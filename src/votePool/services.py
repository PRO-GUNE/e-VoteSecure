from connection import get_db_connection, get_target_db_connection
from votepool_db import add_to_vote_pool, get_vote_count
import random
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


connection = get_db_connection()


def get_count():
    return get_vote_count(connection)


def add_vote(id, vote):
    status = add_to_vote_pool(id, vote, connection)
    if status:
        return True
    else:
        return False


def authenticate_JWT(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(data)
        if data["user_id"] == 0:
            return True

    except Exception as e:
        print(e)
        return False


def data_migrate():

    try:
        # Connect to the source and target databases
        source_connection = get_db_connection()
        target_connection = get_target_db_connection()

        # Create cursors for source and target databases
        source_cursor = source_connection.cursor()
        target_cursor = target_connection.cursor()

        # Fetch all `signed_vote` values from the vote_pool table in the source database
        source_cursor.execute("SELECT signed_vote FROM vote_pool")
        signed_votes = source_cursor.fetchall()

        signed_votes = [vote["signed_vote"] for vote in signed_votes]

        # Shuffle the signed votes
        random.shuffle(signed_votes)

        insert_query = (
            "INSERT INTO election_deparment_vote_table (signed_vote) VALUES (%s)"
        )

        for signed_vote in signed_votes:
            target_cursor.execute(insert_query, (signed_vote,))

        target_connection.commit()

        return True

    except Exception as e:
        print(f"Error during data migration: {e}")
        target_connection.rollback()  # Roll back in case of error
        return False

    finally:
        # Close all database connections and cursors
        source_cursor.close()
        source_connection.close()
        target_cursor.close()
        target_connection.close()
