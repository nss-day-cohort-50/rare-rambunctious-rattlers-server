import sqlite3
import json
import datetime
from models import Post, User, Category, Comment

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
            c.label,
            co.id as comment_id,
            co.subject,
            co.content as comment,
            co.user_id,
            co.creation_date
        from Posts p
        left join Users u
            on p.user_id = u.id
        left join Categories c
            on c.id = p.category_id
        left join Comments co
            on p.id = co.post_id
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

            comment = Comment(
                row['comment_id'],
                row['subject'],
                row['comment'],
                row['user_id'],
                row['id'],
                row['creation_date']
            )

            category = Category(row['category_id'],
                row['label']
            )

            post.comment = comment.__dict__
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

def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( title, publication_date, content, user_id, category_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_post['title'], new_post['publication_date'],
              new_post['content'], new_post['user_id'],
              new_post['category_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id


    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor() #variable that gets returned allows you to do fetch and execute

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))



def update_post(id, new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        # setting the fields, telling where to update using the id that was passed in
        db_cursor.execute("""
        UPDATE Posts
            SET 
                title = ?,
                publication_date = ?,
                content = ?,
                user_id = ?,
                category_id = ?
        WHERE id = ?
        """, (new_post['title'], new_post['publication_date'],
              new_post['content'], new_post['user_id'],
              new_post['category_id'], id, ))
            

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount
        # call rowcount to see if anything changed when we call sql query

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

