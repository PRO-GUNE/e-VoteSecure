import pymysql
from streamlit import cache_resource


@cache_resource
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
        autocommit=True,
    )

    return connection


# Setup database
def setup_db():
    try:
        connection = get_db_connection()
        print(connection)
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
        cursor.execute(
            """CREATE TABLE VotePool (
                id INT AUTO_INCREMENT PRIMARY KEY,
                signedvote TEXT NOT NULL
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
                ('user1', '$2y$10$AWjxBjwFBtV9jYGu4u5KoeYXQCkbXOQgEWMHEwjK2fMBfCnRokcGq') -- Password: password123, 
                ('user2', '$2y$10$nKyTtUOStl0Pfc4lNh9jhucwdgl8tcx6ZL23k0x7I4AVK5e/m/G3u'), -- Password: mypassword
                ('user3', '$2y$10$DBqVuyJ3b9eufW8Fkuic2eaIJ6FJcboRgcwWHSL2MwJWUnP7O9U36'); -- Password: secretpass
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

def add_to_vote_pool(signed_vote):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Store the signed vote as a string since it can be a large integer
        query = "INSERT INTO vote_pool (signed_vote) VALUES (%s)"
        cursor.execute(query, (str(signed_vote),))  
        
        connection.commit()

    finally:
        connection.close()

# Drop all tables
def drop_all_tables():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to drop all tables in the database
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Disable foreign key checks temporarily
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        # Drop each table one by one
        for table in tables:
            table_name = list(table.values())[0]  # Extract the table name from the result
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Enable foreign key checks back
        connection.commit()
    finally:
        connection.close()



if __name__ == "__main__":
    setup_db()
    insert_values()
