import sqlite3
import json
import datetime
from models import Category

def get_all_categories():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            *
        from Categories c
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(
                row['id'], 
                row['label']
            )

            categories.append(category.__dict__)

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

def delete_category(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (id, ))

def update_category(id, updated_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        update Categories
            set
                label = ?
        where id = ?
        """, (updated_category['label'], id ))

        return json.dumps(updated_category)

def get_category_by_id(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        category = Category(data['id'], data['label'])

        return json.dumps(category.__dict__)
