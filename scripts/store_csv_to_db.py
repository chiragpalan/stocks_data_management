import os
import sqlite3
import pandas as pd

# Database path
DB_PATH = "nifty50_data_v1.db"

# Directory containing CSV files
CSV_DIR = "temp_csv"

# Table creation SQL template with DATETIME type for `Datetime` column (no primary key constraint)
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS {table_name} (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Datetime DATETIME,
    Open REAL,
    High REAL,
    Low REAL,
    Close REAL,
    Adj_Close REAL,
    Volume INTEGER
);
"""

def store_csv_to_db():
    """Store CSV data in SQLite database."""
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Process each CSV file in the folder
    for file_name in os.listdir(CSV_DIR):
        if file_name.endswith(".csv"):
            # Get the table name by removing '.csv' extension
            table_name = file_name.replace(".csv", "")
            file_path = os.path.join(CSV_DIR, file_name)
            
            print(f"Processing file: {file_name}...")
            
            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                
                # Ensure the `Datetime` column is formatted as a string for SQLite
                if 'Datetime' in df.columns:
                    df['Datetime'] = pd.to_datetime(df['Datetime']).astype(str)
                
                # Rename columns to match database schema
                df.rename(
                    columns={ "Adj Close": "Adj_Close" },
                    inplace=True
                )
                
                # Create the table if it doesn't exist
                cursor.execute(TABLE_SCHEMA.format(table_name=table_name))
                
                # Append data to the table
                df.to_sql(table_name, conn, if_exists="append", index=False)
                print(f"Data from {file_name} stored in table: {table_name}.")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    # Close the database connection
    conn.close()
    print("All files processed.")

if __name__ == "__main__":
    store_csv_to_db()
