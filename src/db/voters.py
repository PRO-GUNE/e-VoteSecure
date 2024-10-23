def get_user_from_db(username, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    return user


def get_user_from_id_from_db(userid, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (userid,))
    user = cursor.fetchone()
    return user


def set_user_in_db(username, password, connection):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)", (username, password)
    )
    connection.commit()


def set_voted_in_db(username, connection):
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET voted=1 WHERE username=%s", (username,))
    connection.commit()
