import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")


def get_db_connection(db_name="stabledb"):
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


# Setup database
def setup_db():
    try:
        connection = get_db_connection()
        print(connection)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users, candidates, vote_pool;")
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
            """CREATE TABLE vote_pool (
                id BIGINT UNSIGNED PRIMARY KEY,
                signed_vote TEXT NOT NULL,
                counted BOOLEAN DEFAULT FALSE             -- Boolean field to track if the vote was counted (default is FALSE)
            );"""
        )

        cursor.execute(
            """
            CREATE PROCEDURE AddVoteToPool(
                IN vote_text TEXT
            )
            BEGIN
                DECLARE last_vote_id BIGINT UNSIGNED;
                DECLARE new_vote_id BIGINT UNSIGNED;

                -- Error handling to roll back transaction in case of any error
                DECLARE EXIT HANDLER FOR SQLEXCEPTION
                BEGIN
                    ROLLBACK;
                    SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'Failed to insert vote';
                END;

                START TRANSACTION;

                -- Get the last entered vote ID; if no rows exist, set to NULL
                SELECT id INTO last_vote_id FROM vote_pool
                ORDER BY id DESC
                LIMIT 1;

                -- Generate new_vote_id
                IF last_vote_id IS NULL THEN
                    -- If no previous vote exists, generate a random BIGINT UNSIGNED for the first vote
                    SET new_vote_id = FLOOR(RAND() * POW(2, 63));
                ELSE
                    -- Otherwise, hash the last_vote_id and convert to BIGINT
                    SET new_vote_id = CONV(SUBSTRING(SHA2(last_vote_id, 256), 1, 16), 16, 10);
                END IF;

                -- Insert new vote record into vote_pool table
                INSERT INTO vote_pool (id, signed_vote)
                VALUES (new_vote_id, vote_text);

                -- Commit the transaction if successful
                COMMIT;
            END;
            """
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


# Drop all tables
def drop_all_tables():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to drop all tables in the database
        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 0;"
        )  # Disable foreign key checks temporarily
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        # Drop each table one by one
        for table in tables:
            table_name = list(table.values())[
                0
            ]  # Extract the table name from the result
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Enable foreign key checks back
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    setup_db()
    insert_values()
