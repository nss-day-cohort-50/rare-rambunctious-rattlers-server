import sqlite3
import json
import datetime
from models import User

def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
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
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            user = User(
                row['id'], 
                row['first_name'], 
                row['last_name'], 
                row['email'], 
                row['bio'], 
                row['username'], 
                row['password'], 
                row['created_on'], 
                row['active']
            )

            entries.append(user.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

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
        res = {}
        db_cursor.execute('''
        SELECT
           *
        FROM Users u
        WHERE u.email = ?
        ''', ( new_user['email'], ))

        dataset = db_cursor.fetchall()
        if not dataset:
            db_cursor.execute("""
            insert into Users
                ( first_name, last_name, email, username, password, created_on )
            values
                (?, ?, ?, ?, ?, ?);
            """, (new_user['first_name'], new_user['last_name'],new_user['email'], new_user['username'], new_user['password'], datetime.datetime.now() ))
            
            id = db_cursor.lastrowid
            res['token'] = id
            res['valid'] = True
        else:
            res['message'] = 'User email already exists'
        
        return json.dumps(res)
