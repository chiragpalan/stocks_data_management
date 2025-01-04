import sqlite3
import pandas as pd

# Path to the SQLite database
DB_PATH = 'nifty50_data_v1.db'

# Path to the README file
README_PATH = 'README.md'

def get_last_5_rows_from_tables():
    """Fetch the last 5 rows from each table in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get the list of all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    data = {}

    # Fetch last 5 rows from each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY Id DESC LIMIT 5;")
        rows = cursor.fetchall()

        # Store data in dictionary with table name as key
        data[table_name] = rows

    conn.close()
    return data

def update_readme():
    """Update the README file with last 5 rows from each table."""
    data = get_last_5_rows_from_tables()

    # Read the existing README
    with open(README_PATH, 'r') as f:
        readme_content = f.read()

    # Create a string for the tables' last 5 rows
    tables_content = ""
    for table_name, rows in data.items():
        tables_content += f"### Last 5 rows from table `{table_name}`\n\n"
        df = pd.DataFrame(rows)
        tables_content += df.to_markdown(index=False) + "\n\n"

    # Add the table content to the README
    new_readme_content = readme_content + "\n\n" + tables_content

    # Write the updated content back to the README
    with open(README_PATH, 'w') as f:
        f.write(new_readme_content)

if __name__ == "__main__":
    update_readme()
