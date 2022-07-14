from dungeon_app.config.mysqlconnection import connectToMySQL
#Make sure to change file directory to match new folder names
from flask import flash, session
from dungeon_app import app
from flask_bcrypt import Bcrypt
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument

class User:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.password_confirm = data['password_confirm']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #Basic user validation is, name email and password.
        #Make sure to change these variables as necessary to match ERD


    @classmethod
    def registration_validation(cls, data):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"
        #Make sure to change database connection based on what db you're connecting to
        result = connectToMySQL('dungeon_map_gen').query_db(query,data)
        if len(result) > 0:
            flash("email already exists")
            is_valid = False

        if len(data['name']) < 1:
            flash("Must have a valid name")
            is_valid = False

        if (len(data['email']) < 1) and (not EMAIL_REGEX.match(data['email'])):
            flash("Must have a valid email")
            is_valid = False

        if len(data['password']) < 1:
            flash("Must have a password")
            is_valid = False
        if (len(data['password_confirm']) < 1) and (data['password'] != data['password_confirm']):
            flash("Must confirm your password")
            is_valid = False
        
        return is_valid

    @classmethod
    def login_validation(cls, data):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"
        #Make sure to change database connection based on what db you're connecting to
        result = connectToMySQL('dungeon_map_gen').query_db(query,data)
        for row_from_db in result:
            user_data = {
            "name": row_from_db["name"],
            "email": row_from_db["email"],
            "password" : row_from_db["password"]
            }
        if (len(result) < 1) or (not bcrypt.check_password_hash(user_data['password'], data['password'])):
            flash("Email or Password is incorrect")
            print("Checked password, and returned false")
            return False

        # if (len(data['email']) < 1) and (not EMAIL_REGEX.match(data['email'])):
        #     flash("Must have a valid email")
        #     is_valid = False
        # if len(data['password']) < 1:
        #     flash("Must have a password")
        #     is_valid = False
        
        print("Everything looks good")

        return is_valid

    @staticmethod
    def password_encrypt(data):
        print("This is the user password before hashing: " + data)
        password_hash = bcrypt.generate_password_hash(data)
        print(password_hash)
        return password_hash

    @classmethod
    def register_user(cls, data):
        # data = cls.password_encrypt(data)

        query = "INSERT INTO users ( name, email, password ) VALUES ( %(name)s, %(email)s, %(password)s);"
        # data is a dictionary that will be passed into the save method from server.py
        #change database name based on name of new db you're connecting to
        return connectToMySQL('dungeon_map_gen').query_db( query, data )

    @classmethod
    def login_user(cls, data):
        #This function purely logs in the user and stores important user info within session so that it may be used as necessary
        #this function is called when a user logs in, AND when a user is registered, so that they auto login even during registration
        query = "SELECT * FROM users WHERE email = %(email)s;"
        #change database name based on name of new db you're connecting to
        result = connectToMySQL('dungeon_map_gen').query_db(query,data)
        for row_from_db in result:
            user_data = {
            "user_id" : row_from_db["id"],
            "name": row_from_db["name"],
            "email": row_from_db["email"],
            }
        #logs in the user and stores their ID name and email within the session
        #so that you can call upon it when necessary
        #add new info here, that you wish to store in session
        session['user_id'] = user_data['user_id']
        session['name'] = user_data['name']
        session['email'] = user_data['email']





