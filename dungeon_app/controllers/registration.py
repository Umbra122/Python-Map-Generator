from dungeon_app import app
from flask import render_template, redirect, request, session
#Make sure to change file directory to match new folder names
from dungeon_app.models.registration import User
from dungeon_app.models.dungeon_gen import Dungeon_Gen

@app.route("/login-register")
def login_register():
    print("Welcome to the index")
    return render_template('login-register.html')

@app.route("/register_user", methods=["POST"])
def registerUser():
    
    is_valid = User.registration_validation(request.form)
    if not is_valid:
        return redirect('/login-register')
    elif is_valid:
        data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "password" : User.password_encrypt(request.form["password"])
    }
        User.register_user(data)
        User.login_user(data)
        return redirect('/dashboard')
    
    return redirect('/')

@app.route("/dashboard")
def welcomeUser():
    if(not session.get('user_id')):
        return redirect('/')
    data = {
        "name": session["name"],
        "email": session["email"],
        "user_id": session["user_id"]
    }
    map_data = Dungeon_Gen.get_map_info(data)
    return render_template('dashboard.html', maps = map_data)

@app.route("/logout")
def logoutUser():
    session.clear()
    return redirect('/')

@app.route("/login", methods=["POST"])
def loginUser():
    
    is_valid = User.login_validation(request.form)
    if not is_valid:
        return redirect('/login-register')
    elif is_valid:
        User.login_user(request.form)
    
    return redirect('/dashboard')