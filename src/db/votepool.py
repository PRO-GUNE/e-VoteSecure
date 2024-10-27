def add_to_vote_pool(signed_vote, connection):
    cursor = connection.cursor()
    # Call the stored procedure to add a new vote to the vote_pool table
    cursor.callproc("AddVoteToPool", (signed_vote,))
    connection.commit()


def get_vote_pool(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vote_pool")
    vote_pool = cursor.fetchall()
    return vote_pool


def set_vote_counted_in_db(id, connection):
    cursor = connection.cursor()
    cursor.execute("UPDATE vote_pool SET counted=1 WHERE id=%s", (id,))
    connection.commit()
    return


def set_vote_uncounted_in_db(connection):
    cursor = connection.cursor()
    cursor.execute("UPDATE vote_pool SET counted=0")
    connection.commit()
    return


def get_vote_count(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM vote_pool")
    count = cursor.fetchone()
    return count
