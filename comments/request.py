import sqlite3
import json
import datetime
from models import Post, User, Category, Comment

def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( subject, content, user_id, post_id, creation_date )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_comment['subject'], new_comment['content'],
              new_comment['user_id'], new_comment['post_id'], datetime.datetime.now() ))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)

def get_comments_by_post(post_id):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.subject,
            c.content,
            c.user_id,
            c.post_id,
            c.created_date
        from Comments c
        WHERE c.post_id = ?
        """, ( post_id, ))

        comments = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['subject'], row['content'], row['user_id'] , row['post_id'], row['creation_date'])
            comments.append(comment.__dict__)

    return json.dumps(comments)


def get_all_comments():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT *
        FROM Comments
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['subject'], row['content'], row['user_id'] , row['post_id'], row['creation_date'])

            comments.append(comment.__dict__)
        
    return json.dumps(comments)