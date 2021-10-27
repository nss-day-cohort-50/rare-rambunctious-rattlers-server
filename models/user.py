class User():
    def __init__(self, id, first_name, last_name, email, bio, username, created_on, active, password=""):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.bio = bio
        self.active = 1
        self.created_on = created_on
        
