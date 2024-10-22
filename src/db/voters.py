def get_user_from_db(username, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    return user


def set_voted_in_db(username, connection):
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET voted=1 WHERE username=%s", (username,))
    connection.commit()
