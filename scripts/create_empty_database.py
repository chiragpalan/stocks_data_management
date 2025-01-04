import sqlite3
import os

# Path to the database file
DB_PATH = "nifty50_data_v1.db"

def create_empty_database(db_path):
    """Clear the existing SQLite database (if it exists) and create a new empty database."""
    # Check if the database file already exists
    if os.path.exists(db_path):
        os.remove(db_path)  # Remove the existing database file
        print(f"Existing database at {db_path} has been removed.")
    
    # Create a new empty database
    conn = sqlite3.connect(db_path)
    conn.close()
    print(f"Empty database created at: {db_path}")

if __name__ == "__main__":
    create_empty_database(DB_PATH)
