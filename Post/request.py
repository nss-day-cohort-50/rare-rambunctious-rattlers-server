import sqlite3
import json
import datetime
from models import Post, User, Category

def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT 
            p.id,
            p.title,
            p.publication_date,
            p.content,
            p.user_id,
            p.category_id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.created_on,
            u.active,
            c.label
        from Posts p
        left join Users u
            on p.user_id = u.id
        left join Categories c
            on c.id = p.category_id
        ORDER BY cast(p.publication_date as date(1)) DESC
        """)

        # Initialize an empty list to hold all entry representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            post = Post(
                row['id'], 
                row['title'], 
                row['publication_date'], 
                row['content'], 
                row['user_id'], 
                row['category_id']
            )

            user = User(row['user_id'],
                row['first_name'],
                row['last_name'],
                row['email'],
                row['username'],
                '',
                row['bio'],
                row['active'],
                row['created_on']  
            )

            category = Category(row['category_id'],
                row['label']
            )

            post.user = user.__dict__
            post.category = category.__dict__
            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)

def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            p.id,
            p.title,
            p.publication_date,
            p.content,
            p.user_id,
            p.category_id,  
            u.first_name,
            u.last_name,
            u.email,
            u.username,
            u.password,
            u.bio,
            u.active,
            u.created_on,
            c.label
        from Posts p
        left join Users u
            on p.user_id = u.id
        left join Categories c
            on c.id = p.category_id 
        WHERE p.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        post = Post(
            data['id'], 
            data['title'], 
            data['publication_date'], 
            data['content'],
            data['user_id'], 
            data['category_id']
        )

        user = User(data['user_id'],
            data['first_name'],
            data['last_name'],
            data['email'],
            data['username'],
            '',
            data['bio'],
            data['active'],  
            data['created_on']
            )

        category = Category(data['category_id'],
            data['label']
        )

        post.user = user.__dict__
        post.category = category.__dict__

        return json.dumps(post.__dict__)   