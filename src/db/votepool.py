def add_to_vote_pool(signed_vote, connection):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO vote_pool (signed_vote) VALUES (%s)", (signed_vote,))
    connection.commit()
