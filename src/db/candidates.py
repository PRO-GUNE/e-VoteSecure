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
