import sqlite3
import os

# Path to the SQLite database
DB_PATH = "nifty50_data_v1.db"
# Path to the README.md file
README_PATH = "README.md"

def get_last_5_rows_of_each_table():
    """Fetch last 5 rows of each table in the SQLite database."""
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    table_data = {}
    for table in tables:
        table_name = table[0]
        
        # Get the last 5 rows of each table
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY Id DESC LIMIT 5;")
        rows = cursor.fetchall()
        
        # Store the table data
        table_data[table_name] = rows
    
    conn.close()
    return table_data

def format_data_to_markdown(table_data):
    """Format the data into a Markdown table."""
    markdown_content = ""
    
    for table_name, rows in table_data.items():
        markdown_content += f"### {table_name}\n"
        if rows:
            # Extract column names from the first row
            columns = [description[0] for description in cursor.description]
            markdown_content += "| " + " | ".join(columns) + " |\n"
            markdown_content += "| " + " | ".join(["---"] * len(columns)) + " |\n"
            
            # Add each row to the markdown table
            for row in rows:
                markdown_content += "| " + " | ".join(map(str, row)) + " |\n"
        markdown_content += "\n"
    
    return markdown_content

def update_readme(markdown_content):
    """Update the README.md file with the new data."""
    with open(README_PATH, "r") as file:
        readme_content = file.read()
    
    # Find the placeholder where you want to insert the table data
    start_placeholder = "<!-- LAST_5_ROWS -->"
    end_placeholder = "<!-- END_LAST_5_ROWS -->"
    
    # Replace the existing data with the new markdown content
    if start_placeholder in readme_content and end_placeholder in readme_content:
        updated_content = readme_content.replace(
            f"{start_placeholder}\n{end_placeholder}",
            f"{start_placeholder}\n\n{markdown_content}\n{end_placeholder}"
        )
        with open(README_PATH, "w") as file:
            file.write(updated_content)
    else:
        print("Placeholders not found in README.md file.")

if __name__ == "__main__":
    # Fetch last 5 rows from each table in the database
    table_data = get_last_5_rows_of_each_table()
    
    # Format the data to markdown
    markdown_content = format_data_to_markdown(table_data)
    
    # Update the README file with the new data
    update_readme(markdown_content)
