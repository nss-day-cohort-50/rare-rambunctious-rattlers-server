import sqlite3
import json
import datetime
from models import Category

def get_all_categories():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT 
            *
        from Categories c
        """)

        # Initialize an empty list to hold all entry representations
        categories = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            category = Category(
                row['id'], 
                row['label']
            )

            categories.append(category.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categories)

def add_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        insert into Categories
            ( label )
        values
            (?);
        """, (new_category['label'], ))

        id = db_cursor.lastrowid

        new_category['id'] = id
    
        return json.dumps(new_category)
