def add_to_vote_pool(unique_id, signed_vote, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO vote_pool (unique_id, signed_vote) VALUES (%s, %s)",
            (unique_id, signed_vote),
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        return False


def get_vote_pool(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vote_pool")
    vote_pool = cursor.fetchall()
    return vote_pool


def get_vote_count(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM vote_pool")

    result = cursor.fetchone()  # Fetch one row

    count = result["COUNT(*)"]
    return count
