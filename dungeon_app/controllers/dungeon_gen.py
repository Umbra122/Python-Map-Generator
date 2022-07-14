from dungeon_app import app
import json
from dungeon_app.models.dungeon_gen import Dungeon_Gen
from flask import redirect, render_template, request, session, flash

@app.route("/")
def index():
    print("Welcome to the index")
    return render_template('index.html')

@app.route("/generate-map", methods=["POST"])
def generate():
    print("Welcome to the map tile testing area")
    roomNum = int(request.form['rooms'])
    xCol = int('1' + ('0' * int(request.form['xCol'])))

    validate_size = {
        "size_x" : int(request.form['xCol']),
        "size_y" : int(request.form['yCol'])
    }
    if not (Dungeon_Gen.map_validate(validate_size)):
        return redirect('/')
    
    data = {
        "map_key" : Dungeon_Gen.dungeon_gen(int(request.form['yCol']), xCol, int(request.form['xCol']) , roomNum, request.form['map_theme']),
        "map_theme" : request.form['map_theme'],
        "map_style" : request.form['map_style'],
        "size_x" : int(request.form['xCol']),
        "size_y" : int(request.form['yCol'])
    }
    
    
    Dungeon_Gen.map_session(data)
    # session['map_key'] = Dungeon_Gen.dungeon_gen(int(y), xCol, roomNum)
    return redirect("/map-show")

@app.route("/map-show")
def map_test():
    print("Welcome to the map tile testing area")

    spaces = Dungeon_Gen.dungeon_show()
    return render_template('map-show.html', map = spaces)

#Saves the map with current settings
#Uses session to grab info and input it into DB
@app.route("/save-map")
def save_map():
    if not (session.get('user_id')):
        flash("you must be logged in to save a map")
        return redirect('/map-show')
    data = {
        "map_key" : json.dumps(session['map_key']), #Converts map_key into string
        #must convert back into list when grabbing out of DB
        "map_theme" : session['map_theme'],
        "map_style" : session['map_style'],
        "size_x" : session['size_x'],
        "size_y" : session['size_y'],
        "user_id" : session['user_id']
    }
    # Use this to convert map_key as str or list
        # o = json.dumps(session['map_key'])
        # print(type(o))
        # p = json.loads(o)
        # print(type(p))
    Dungeon_Gen.save_dungeon_map(data)
    return redirect('/dashboard')


@app.route("/view-map", methods=["POST"])
def regen_map():
    data = {
        "map_key" : json.loads(request.form['map_key']),
        "map_theme" : request.form['map_theme'],
        "map_style" : request.form['map_style'],
        "size_x" : request.form['size_x'],
        "size_y" : request.form['size_y']
    }
    Dungeon_Gen.map_session(data)
    return redirect("/map-show")