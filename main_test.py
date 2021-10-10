import numpy as np
import curses
import os
import time

class tetris_game:

    tetris_map = np.zeros((10,20), dtype=np.int8)
    speedLevel = [1.50, 1.40, 1.30, 1.20, 1.10, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]
    x_ray = False
    character_tetris = [".", "█", "█"]

    def __init__(self, id, name, my_window, level):
        self.id = id
        self.name = name
        self.my_window = my_window
        self.level = level

    
    def x_ray_mode(self):
        if(not self.x_ray):
            self.character_tetris = ["0","1","2"]
            self.x_ray = True
        else:
            self.character_tetris = [".","█","█"]
            self.x_ray = False

    def draw(self):
        for y in range(len(self.tetris_map[0])):
            for x in range(len(self.tetris_map)):
                self.my_window.addstr(y, x, self.character_tetris[self.tetris_map[x][y]])
        self.my_window.addstr(21,0,"")
        my_window.refresh()
        curses.napms(0)
    
    def clearPiece(self, piece_data):
        for x in range(6):
            for y in range(6):
                try:
                    if(self.tetris_map[piece_data["posX"]+x][piece_data["posY"]+y] == 1):
                        self.tetris_map[piece_data["posX"]+x][piece_data["posY"]+y] = 0
                except:
                    continue

    def setPiece(self, piece, piece_data):
        for location in piece:
            if(piece_data["posY"]+location[1] >= 0):
                self.tetris_map[piece_data["posX"]+location[0]][piece_data["posY"]+location[1]] = 1

    def colisionPieceDown(self, piece, piece_data):
        for location in piece:
            if(location[1] + piece_data["posY"] >= 19):
                return True
            elif(piece_data["posY"] > -3):
                if(self.tetris_map[piece_data["posX"]+location[0]][piece_data["posY"]+location[1]+1] > 1):
                    return True
        return False
    
    def collisionPiece(self, key, piece, piece_data):
        collision = False
        for location in piece:
            if(key == ord('d')):
                if(piece_data["posX"]+location[0]+1 > 9 or self.tetris_map[piece_data["posX"]+location[0]+1][piece_data["posY"]+location[1]] > 1):
                    collision = True
            elif(key == ord('a')):
                if(piece_data["posX"]+location[0]-1 < 0 or self.tetris_map[piece_data["posX"]+location[0]-1][piece_data["posY"]+location[1]] > 1):
                    collision = True
            elif(key == ord('s')):
                if(piece_data["posY"]+location[1]+1 > 19 or self.tetris_map[piece_data["posX"]+location[0]][piece_data["posY"]+location[1]+1] > 1):
                    collision = True
        return collision
    
    def collisionRotation(self, piece, piece_data):
        top = 0
        left_right = 0
        for location in piece:
            if(piece_data["posX"]+location[0] > 9):
                left_right -= 1
            elif(piece_data["posX"]+location[0] < 0):
                left_right += 1
            elif(piece_data["posY"]+location[1] > 19):
                top -= 1

            elif(piece_data["posY"]+location[1] >= 0):
                if (self.tetris_map[piece_data["posX"]+location[0]][piece_data["posY"]+location[1]] > 1):
                    top -= 1
        
        return [left_right , top]

    def staticPiece(self, piece, piece_data):
        for location in piece:
            self.tetris_map[piece_data["posX"]+location[0]][piece_data["posY"]+location[1]] = 2

    def clearLine(self, lines):
        if(lines):
            for line in lines:    
                for y in range(line, 4, -1):
                    for x in range(len(self.tetris_map)):
                        self.tetris_map[x][y] = self.tetris_map[x][y-1]
            

    def ClearLineIdentifity(self):
        lines = []
        full = False
        
        for y in range(0,len(self.tetris_map[0])):
            full = True
            for x in range(len(self.tetris_map)):
                if(self.tetris_map[x][y] == 0):
                    full = False
            if(full == True):
                lines.append(int(y))
        return lines

class Pieces:
    piece_data = {"type": -1, "rotation": 0, "posX":0, "posY":0}
    piece_actual_rotation = []
    piece_actual = []
    pieces = [
    # Square
    [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
    ],

    # I
    [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 2, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 2, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    ]
    ,
    # L
    [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 2, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 2, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    ],
    # L mirrored
    [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 2, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 2, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ]
    ],
    # N
    [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 2, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],

        [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    ],
    # N mirrored
    [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    ],
    # T
    [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 2, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 2, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    ]
    ]

    def getPiece(self, piece_type):
        self.piece_data["type"] = piece_type
        self.piece_data["rotation"] = 0
        self.piece_data["posX"] = 2
        self.piece_data["posY"] = -3

        self.piece_actual_rotation = []

        rotation = []
        for rotation_range in range(4):
            for y in range(5):
                for x in range(5):
                    if(self.pieces[self.piece_data["type"]][rotation_range][x][y] > 0):
                        rotation.append([x, y])

            self.piece_actual_rotation.append(rotation)
            rotation = []

        self.piece_actual = self.piece_actual_rotation[self.piece_data["rotation"]]

    def rotationPiece(self):
        if(self.piece_data != -1):
            self.piece_data["rotation"] += 1
            self.piece_data["rotation"] %= 4

    def updatePiece(self):
        self.piece_actual = []
        for location in self.piece_actual_rotation[self.piece_data["rotation"]]:
            self.piece_actual.append(location)

    def movePiece(self, movX, movY):
        self.piece_data["posX"] += movX
        self.piece_data["posY"] += movY

screen = curses.initscr()
curses.cbreak()
curses.noecho()
screen.keypad(True)

my_window = curses.newwin(200,200,0,0)
my_window.nodelay(True)

pieces = Pieces()
tetris = tetris_game(0, "player", my_window, 15)

pieces.getPiece(np.random.randint(0,7))
#pieces.getPiece(1)

key = ''
percorrido = 0
timems_old = time.time()*1000.0

while(key != ord('q')):
    time.sleep(1.0/15)
    pieces.updatePiece()
    
    key = my_window.getch()
    if(key == ord('k')):
        tetris.x_ray_mode()
    if(key == ord('w')):
        pieces.rotationPiece()
        

        """if(tetris.colisionPieceRight(pieces.piece_actual,pieces.piece_data)):
            pieces.piece_data["posX"] -= 1
        if(tetris.colisionPieceLeft(pieces.piece_actual,pieces.piece_data)):
            pieces.piece_data["posX"] += 1"""
    if(key == ord('d')):
        if(not tetris.collisionPiece(key, pieces.piece_actual,pieces.piece_data)):
            pieces.movePiece(+1,0)
    if(key == ord('a')):
        if(not tetris.collisionPiece(key, pieces.piece_actual,pieces.piece_data)):
            pieces.movePiece(-1,0)
    if(key == ord('s')):
        if(not tetris.collisionPiece(key, pieces.piece_actual, pieces.piece_data)):
            pieces.movePiece(0,+1)

    timems_now = time.time()*1000.0
    timeper = timems_now - timems_old
    timems_old = timems_now

    tetris.clearPiece(pieces.piece_data)

    collision_move = tetris.collisionRotation(pieces.piece_actual, pieces.piece_data)
    if(collision_move != [0, 0]):
        pieces.piece_data["posX"] += collision_move[0]
        pieces.piece_data["posY"] += collision_move[1]

    if(percorrido < tetris.speedLevel[tetris.level]*1000):
        percorrido += timeper
    else:
        percorrido = 0
        if(not tetris.colisionPieceDown(pieces.piece_actual, pieces.piece_data)):
            pieces.movePiece(0,1)
        else:
            tetris.staticPiece(pieces.piece_actual, pieces.piece_data)
            pieces.getPiece(np.random.randint(0,7))

        """if(pieces.piece_data["posY"] < 21 and tetris.colisionPieceDown(pieces.piece_actual, pieces.piece_data) == False):
            pieces.movePiece(0,1)"""
        """else:
            tetris.staticPiece(pieces.piece_actual, pieces.piece_data)
            tetris.clearLine(tetris.ClearLineIdentifity())
            pieces.piece_actual = 0"""

    """if(pieces.piece_actual == 0):
        pieces.getPiece(np.random.randint(0,7))"""
    
    tetris.clearLine(tetris.ClearLineIdentifity())
    tetris.setPiece(pieces.piece_actual, pieces.piece_data)
    tetris.draw()


curses.endwin()