def add_to_vote_pool(signed_vote, connection):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO vote_pool (signed_vote) VALUES (%s)", (signed_vote,))
    connection.commit()
    return connection.status()


def get_vote_pool(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vote_pool")
    vote_pool = cursor.fetchall()
    return vote_pool


def get_vote_count(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM vote_pool")
    count = cursor.fetchone()[0]  
    return count


