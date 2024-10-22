import pymysql


def get_db_connection():
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-39341dcb-cmggun456-1c5e.g.aivencloud.com",
        password="AVNS_b9CCV1O_xsp-dKGn1OT",
        read_timeout=timeout,
        port=12530,
        user="avnadmin",
        write_timeout=timeout,
    )

    return connection


# Setup database
def setup_db():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users, candidates;")
        cursor.execute(
            """CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique identifier for each user
                    username VARCHAR(50) NOT NULL UNIQUE,   -- Username field (must be unique)
                    password VARCHAR(255) NOT NULL,         -- Password field to store the hashed password
                    voted BOOLEAN DEFAULT FALSE              -- Boolean field to track if the user has voted (default is FALSE)
                );"""
        )

        cursor.execute(
            """CREATE TABLE candidates (
                    id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique identifier for each candidate
                    candidate VARCHAR(100) NOT NULL,         -- Name of the candidate
                    vote_count INT DEFAULT 0                 -- Vote count, starting at 0
                );"""
        )
    finally:
        connection.close()


# Insert values to database
def insert_values():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO users (username, password) VALUES 
                ('user1', '$2b$12$QmF.X7lgTfQdYvSPoI5IuOg0TPPA8SGtQkP.M7zFo92F3hWgI8klG'), -- Password: password123
                ('user2', '$2b$12$mkfYP2Ok16Fv0Gb5iHXYP.WhIuBFoNxzXKK7V99hvTNOHJGsGJprW'), -- Password: mypassword
                ('user3', '$2b$12$0.DzCeZa.VoFbvReD9E5seR4PvvwmktBeqzyTKPDxsDKXO2Y4/JtS'), -- Password: secretpass
                ('user4', '$2b$12$yRVCJMgWchD/BVBu5mUw9OyEqm08td.9FQUT/VhcxZ.NVtr2NEaUy'), -- Password: adminpass
                ('user5', '$2b$12$aVYrJnl7jU2Y3Hdw10lNi.8J9QmP/g3C/Zge.sFq1kIE/ceP1Hl5y'); -- Password: qwerty123"""
        )
        cursor.execute("SELECT * FROM users WHERE username='user1'")
        print(cursor.fetchall())

        cursor.execute(
            """INSERT INTO candidates (candidate, vote_count) VALUES 
                ('Alice Johnson', 0),
                ('Bob Smith', 0),
                ('Carol Lee', 0),
                ('David Brown', 0),
                ('Eve Davis', 0);"""
        )
        cursor.execute("SELECT * FROM candidates")
        print(cursor.fetchall())
    finally:
        connection.close()


if __name__ == "__main__":
    setup_db()
    insert_values()
