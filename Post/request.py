import sqlite3
import json
import datetime
from models import Post

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
            p.category_id
        from Posts p
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

            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)

def get_single_user(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active
        from Users u
        WHERE u.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        user = User(data['id'], data['first_name'], data['last_name'], data['email'],
                            data['bio'], data['username'], data['password'], data['created_on'], data['active'])
        return json.dumps(user.__dict__)


def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        insert into Users
            ( first_name, last_name, email, bio, username, password, created_on, active )
        values
            (?, ?, ?, ?, ?, ?, ?, ?);
        """, (new_user['first_name'], new_user['last_name'],new_user['email'], new_user['bio'], new_user['username'], new_user['password'], datetime.datetime.now(), new_user['active'] ))


        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_user['id'] = id

        

        return json.dumps(new_user)