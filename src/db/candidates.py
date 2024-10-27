def get_candidates_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    return candidates


def get_candidate_from_db_by_id(candidate_id, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id=%s", (candidate_id,))
    candidate = cursor.fetchone()
    return candidate


def reset_votes_in_db(connection):
    cursor = connection.cursor()
    # atomic operation to reset the vote count for all candidates
    cursor.execute("UPDATE candidates SET vote_count=0")
    connection.commit()
    return


def set_votes_in_db(candidate, connection):
    cursor = connection.cursor()
    # atomic operation to increment the vote count for the candidate
    cursor.execute(
        "UPDATE candidates SET vote_count=vote_count+1 WHERE candidate=%s", (candidate,)
    )
    connection.commit()
    return
