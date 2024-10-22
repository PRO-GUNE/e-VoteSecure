def set_votes_in_db(candidate, connection):
    cursor = connection.cursor()
    # atomic operation to increment the vote count for the candidate
    cursor.execute(
        "UPDATE candidates SET vote_count=vote_count+1 WHERE candidate=%s", (candidate,)
    )
    connection.commit()
    return
