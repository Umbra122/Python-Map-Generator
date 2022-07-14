import json
from tracemalloc import start
from dungeon_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from dungeon_app import app
import random

class Dungeon_Gen:
    def __init__(self, data):
        # self.user_id = data['user_id']
        self.map_key = json.loads(data['map_key'])
        self.map_theme = data['map_theme']
        # self.size_x = data['size_x']
        # self.size_y = data['size_y']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']

    #creates and returns a standard base 10 random int
    @staticmethod
    def random_num():
        rand = 1 + int(10 * random.random())
        return rand

    #generates the map key
    def key(xNum, size_x):
        randomNum = int(xNum * random.random())
        print(randomNum)
        #multiplying random float number by a large base 10 number to turn it into a big int
        #number needs to be a big int to cleanly split apart the number and convert it into array
        #conversion to int also necessary to allow user to determine X axis size as the int length is limited by user choice
        
        randomArr = []

        for a in str(randomNum):

            #random is currently returning either 0 or 1
            #this denotes whether simply a room tile exits, or not
            randomArr.append(int(a) % 2)
        while len(randomArr) < size_x:
            randomArr.append(0)
        print(randomArr)

        return randomArr

    def map_validate(data):
        is_valid = True
        x = int(data['size_x'])
        y = int(data['size_y'])
        if x > 50:
            flash("Your X axis is to big")
            is_valid = False
        if y > 50:
            flash("Your Y axis is to big")
            is_valid = False
        return is_valid

    #This class function assigns the names for each individual block
    #Change this function to add, edit or remove blocks from the possible map gen blocks
    #if the method of assigning blocks changes, change it here!
    @staticmethod
    def block_assign(num):
        block_name = ""
        #all blocks are either full or empty
        if num == 0:
            block_name = "empty-space"
        if num == 1:
            block_name = "full-space"

        return block_name

    #function to force generate rooms that are complete with 4 walls and corners
    @staticmethod
    def room_gen(key):
        print("Welcome to the room generator")
        room_size = (Dungeon_Gen.random_num()) #limits room size to random amount of squares but no more than 12
        room_size += 2
        start_pointX = (int(random.random() * len(key[0]))) #X axis is always same length so it doesn't matter which Y axis point we grab
        num_y = (int(random.random() * 100) + 1) % len(key)
        while num_y > (len(key)):
            num_y = (int(random.random() * 100) + 1) % len(key)
        # print("Key: " + str(key))
        # room = []
        print("room_size: " + str(room_size))
        print("start_point: " + str(start_pointX))
        print("start point num_y: " + str(num_y))
        for y in range(room_size):
            num_x = start_pointX
            if num_y >= len(key):
                break
            for x in range(room_size):
                if num_x >= len(key[num_y]):
                    break
                key[num_y][num_x] = 1
                num_x += 1
            num_y += 1
            
        return key

    def maze_theme(key):
        print("Welcome to the Maze theme generator")
        length = len(key)
        length2 = len(key[0])
        print("Index size for Y: " + str(length))
        print("Index size for X: " + str(length2))
        for y in range(0, len(key)):

            row = 0
            
            for z in range(int(len(key[y]))):
                yUp = y + 1
                yDown = y - 1
                if (yUp >= int(len(key))) or (yDown <= 0):
                    break
                if key[yUp][row] == 1 and key[yDown][row] == 1:
                    key[y][row] = 0
                elif key[yUp][row] == 0 and key[yDown][row] == 0:
                    key[y][row] = 1
                
                if z == Dungeon_Gen.random_num():
                    key[yUp][row] = 1
                    key[yDown][row] = 1
                row += 1
                if row >= int(len(key[y])):
                    break
                    
        return key

    def dungeon_gen(yCol, xRow, size_x, roomNum, theme):
        key = []
        for y in range(yCol):
            
            arr = Dungeon_Gen.key(xRow, size_x)
            # use this to add key to the class instance
            # self.map_key.append(arr)
            # arr = Dungeon_Gen.room_gen(arr)
            key.append(arr)
            

        if theme == "maze":
            key = Dungeon_Gen.maze_theme(key)


        for n in range(roomNum):
            key = Dungeon_Gen.room_gen(key)
        # print("key out of room gen: " + str(key))

        # Use this to convert map_key as str or list
        # o = json.dumps(self.map_key)
        # print(type(o))
        # p = json.loads(o)
        # print(type(p))
        return key


    def dungeon_show():
        key = session['map_key']
        size_x = session['size_x']
        size_y = session['size_y']
        # self.map_key.append(key)
        print("size_x: " + str(size_x))
        print("size_y: " + str(size_y))
        # print("key: " + str(key) )
        # key2 = []
        # key3 = []
        map = []
        # row = 0
        # for y in range(size_y):
        #     print("y: " + str(y))
        #     for x in range(size_x):
        #         key2.append(key[row])
        #         if row > len(key):
        #             break
        #         row += 1
        #     if row > len(key):
        #             break
        #     print("key2: " + str(key2))
        #     key3.append(key2)
        # print(key3)



        for list in key:
            spaces = []
            for elem in list:
                spaces.append(Dungeon_Gen.block_assign(int(elem)))
            map.append(spaces)
        return map

    @staticmethod
    def save_dungeon_map(data):
        query = "INSERT INTO map (map_key, map_theme, map_style, size_x, size_y, user_id) VALUES (%(map_key)s, %(map_theme)s, %(map_style)s, %(size_x)s, %(size_y)s, %(user_id)s);"
        # #Make sure to change database connection based on what db you're connecting to
        # result = connectToMySQL('dungeon_map_gen').query_db(query,data)
        return connectToMySQL('dungeon_map_gen').query_db(query,data)

    @classmethod
    def get_map_info(cls, data):
        query = "SELECT * FROM map LEFT JOIN users ON map.user_id = users.id WHERE users.id = %(user_id)s;"
        result = connectToMySQL('dungeon_map_gen').query_db(query, data)
        # maps = cls(result[0])
        maps = []
        # Iterate over the db results and create instances of users with cls.
        for mapList in result:
            map_data = {
                "map_key" : mapList["map_key"],
                "map_theme" : mapList["map_theme"],
                "map_style" : mapList["map_style"],
                "size_x" : mapList["size_x"],
                "size_y" : mapList["size_y"]
            }
            maps.append(map_data)
        
        return maps
        
    
    @staticmethod
    def map_session(data):
        session['map_key'] = data['map_key']
        session['size_x'] = data['size_x']
        session['size_y'] = data['size_y']
        session['map_theme'] = data['map_theme']
        session['map_style'] = data['map_style']
        return 0