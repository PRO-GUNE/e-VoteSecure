from connection import get_db_connection,get_target_db_connection

connection = get_db_connection()
connection2= get_target_db_connection()

def add_vote_pool(connection):
    cursor = connection.cursor()
    
    # Corrected the SQL query by placing it in a multi-line string format
    cursor.execute("""
    CREATE TABLE vote_pool (
        unique_id VARCHAR(52) PRIMARY KEY,
        signed_vote TEXT
    );
    """)
    
    connection.commit()  # Commit the table creation to the database

    return "Table 'vote_pool' created successfully"

def drop_vote_pool(connection):
    cursor = connection.cursor()

    # Execute the SQL command to drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS vote_pool;")
    
    connection.commit()  # Commit the table drop action to the database

    return "Table 'vote_pool' dropped successfully"

def add_vote_pool_el(connection):
    cursor = connection.cursor()
    
    # Corrected the SQL query by placing it in a multi-line string format
    cursor.execute("""
    CREATE TABLE election_deparment_vote_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                signed_vote TEXT NOT NULL,
                counted BOOLEAN DEFAULT FALSE             -- Boolean field to track if the vote was counted (default is FALSE)
            );"""
    )
    
    connection.commit()  # Commit the table creation to the database

def drop_vote_pool_el(connection):
    cursor = connection.cursor()

    # Execute the SQL command to drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS election_deparment_vote_table;")
    
    connection.commit()  # Commit the table drop action to the database

print(drop_vote_pool(connection))
print(add_vote_pool(connection))
drop_vote_pool_el(connection2)
add_vote_pool_el(connection2)
