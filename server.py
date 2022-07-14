from dungeon_app import app 
#Insure app file path is changed to match folder name
from dungeon_app.controllers import registration, dungeon_gen

if __name__ == "__main__":
    app.run(debug=True)