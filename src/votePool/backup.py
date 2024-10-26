import threading
import time
import csv
from datetime import datetime
from connection import get_db_connection
import os 

def generate_copies(connection):
    """
    Periodically takes a copy of the vote_pool table every 30 minutes 
    and saves it as a CSV file in the vote_pool_backup directory.
    """
    # Define the backup directory
    backup_directory = "vote_pool_backup"

    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    while True:
        # Get the current timestamp to create a unique filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = os.path.join(backup_directory, f"vote_pool_backup_{timestamp}.csv")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vote_pool")

        # Fetch all rows from the vote_pool table
        rows = cursor.fetchall()

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        # Write to CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(column_names)
            # Write the data
            writer.writerows(rows)

        print(f"Backup saved as {filename}")

        # Wait for 30 minutes (30 * 60 seconds)
        time.sleep(30 * 60)


def start_backup_task():
    """
    Starts the background thread that runs the generate_copies function.
    """
    connection = get_db_connection()
    backup_thread = threading.Thread(target=generate_copies, args=(connection,))
    backup_thread.daemon = True  # Set daemon so the thread will close when the app exits
    backup_thread.start()

