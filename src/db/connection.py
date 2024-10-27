import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")


def get_db_connection(db_name="defaultdb"):
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=db_name,
        host=HOST,
        password=PASSWORD,
        read_timeout=timeout,
        port=int(PORT),
        user=USER,
        write_timeout=timeout,
        autocommit=True,
    )

    return connection


# Setup main database
def setup_primary_db():
    try:
        connection = get_db_connection()
        print(connection)
        cursor = connection.cursor()
        cursor.execute(
            "DROP TABLE IF EXISTS users, candidates, election_deparment_vote_table;"
        )
        cursor.execute(
            """CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique identifier for each user
                    username VARCHAR(50) NOT NULL UNIQUE,   -- Username field (must be unique)
                    email VARCHAR(50) NOT NULL,             -- Email field
                    password VARCHAR(255) NOT NULL,         -- Password field to store the hashed password
                    voted BOOLEAN DEFAULT FALSE             -- Boolean field to track if the user has voted (default is FALSE)
                );"""
        )

        cursor.execute(
            """CREATE TABLE candidates (
                    id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique identifier for each candidate
                    candidate VARCHAR(100) NOT NULL,         -- Name of the candidate
                    vote_count INT DEFAULT 0                 -- Vote count, starting at 0
                );"""
        )
        cursor.execute(
            """CREATE TABLE election_deparment_vote_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                signed_vote TEXT NOT NULL,
                counted BOOLEAN DEFAULT FALSE             -- Boolean field to track if the vote was counted (default is FALSE)
            );"""
        )
    finally:
        connection.close()


# Setup secondary database
def setup_secondary_db():
    try:
        connection = get_db_connection("secondarydb")
        print(connection)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS vote_pool;")
        cursor.execute(
            """CREATE TABLE vote_pool (
                unique_id VARCHAR(52) PRIMARY KEY,
                signed_vote TEXT
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
            """INSERT INTO users (username, email, password) VALUES 
                ('user1', 'cmggun456@gmail.com', '$2y$10$AWjxBjwFBtV9jYGu4u5KoeYXQCkbXOQgEWMHEwjK2fMBfCnRokcGq'), -- Password: password123
                ('user2', 'cmggun456@gmail.com', '$2y$10$nKyTtUOStl0Pfc4lNh9jhucwdgl8tcx6ZL23k0x7I4AVK5e/m/G3u'), -- Password: mypassword
                ('user3', 'cmggun456@gmail.com', '$2y$10$DBqVuyJ3b9eufW8Fkuic2eaIJ6FJcboRgcwWHSL2MwJWUnP7O9U36'); -- Password: secretpass
            """
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
    setup_primary_db()
    setup_secondary_db()
    insert_values()
