from p5 import *
import random

screen_width = 800
screen_height = 640
left_board = []
right_board = []
board = [left_board, right_board]
players = []

def create_board(cStart, cEnd, side):
    square_size = 40
    for i in range(3, 9):
        row = square_size*i+60
        for j in range (cStart, cEnd):
            column = square_size*j+40
            # There is probably a way to shortcut the if/else but this should work for now
            if side == "left":
                left_board.append(Grid_Square(column, row, square_size))
            elif side == "right":
                right_board.append(Grid_Square(column, row, square_size))

def create_players(player_board, color):
    start = random.choice(player_board)
    x_cord = start.x + start.s/10
    y_cord = start.y + start.s/10
    s_length = start.s/10 * 8
    players.append(DicePlayer(x_cord, y_cord, s_length, color))

class Grid_Square:
 def __init__(self, x, y, s):
     self.x = x
     self.y = y
     self.s = s
     self.tiled = False


 def checkmousepressed(self):
     is_x_inside = self.x < mouse_x < self.x + self.s
     is_y_inside = self.y < mouse_y < self.y + self.s
     if is_x_inside and is_y_inside:
         self.clicked()


 def render(self):
    fill("white")
    stroke("black")
    stroke_weight(5)
    square(self.x, self.y, self.s)

class DicePlayer:
    def __init__(self, x, y, s, color):
        self.x = x
        self.y = y
        self.s = s
        self.color = color
        self.num = 1

    def render(self):
        fill(self.color)
        square(self.x, self.y, self.s)


create_board(2, 8, "left")
create_board(9, 15, "right")
create_players(left_board, "green")
create_players(right_board, "orange")

def setup():
    size(screen_width, screen_height)

def draw():
    background(0, 20, 60)
    for side in board:
        for square in side:
            square.render()
    for dice in players:
        dice.render()

run()