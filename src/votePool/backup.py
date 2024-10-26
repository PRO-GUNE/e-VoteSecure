import threading
import time
import csv
from datetime import datetime
from connection import get_db_connection
import os 

def generate_copies():
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

        # Create a new connection for each backup
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM vote_pool")
            # Fetch all rows from the vote_pool table
            rows = cursor.fetchall()

            # Write to CSV file
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['unique_id', 'signed_vote']) 
                writer.writeheader()  # Write the header
                
                for row in rows:
                    writer.writerow(row)  # Write each dictionary as a row

        except Exception as e:
            print(f"Error during backup: {e}")

        finally:
            cursor.close()
            connection.close()

        # Wait for 30 minutes (30 * 60 seconds)
        time.sleep(30 * 60)

def start_backup_task():
    """
    Starts the background thread that runs the generate_copies function.
    """
    backup_thread = threading.Thread(target=generate_copies)
    backup_thread.daemon = True  # Set daemon so the thread will close when the app exits
    backup_thread.start()


