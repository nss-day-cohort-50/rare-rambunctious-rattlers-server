from models import Tag
import sqlite3
import json

def get_all_tags():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT *
        FROM Tags
        ORDER BY label ASC
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)
        
    return json.dumps(tags)

def update_tag(id, new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?;
        """, (new_tag['label'], id, ))
    
    return json.dumps(new_tag)

def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Tags
        WHERE id = ?
        """, (id, ))