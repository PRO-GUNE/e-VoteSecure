def add_to_vote_pool(signed_vote, connection):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO election_deparment_vote_table (signed_vote) VALUES (%s)", (signed_vote,))
    connection.commit()


def get_vote_pool(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM election_deparment_vote_table")
    vote_pool = cursor.fetchall()
    return vote_pool


def set_vote_counted_in_db(id, connection):
    cursor = connection.cursor()
    cursor.execute("UPDATE election_deparment_vote_table SET counted=1 WHERE id=%s", (id,))
    connection.commit()
    return


def set_vote_uncounted_in_db(connection):
    cursor = connection.cursor()
    cursor.execute("UPDATE election_deparment_vote_table SET counted=0")
    connection.commit()
    return