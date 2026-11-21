from p5 import *

screen_width = 800
screen_height = 640
board = []

def create_board(cStart, cEnd):
    square_size = 40
    for i in range(3, 9):
        row = square_size*i+60
        for j in range (cStart, cEnd):
            column = square_size*j+40
            board.append(Grid_Square(column, row, square_size))


class Grid_Square:
 def __init__(self, x, y, s):
     self.x = x
     self.y = y
     self.s = s
     self.tiled = False


 def checkmousepressed(self):
     is_x_inside = self.x < mouse_x < self.x + self.w
     is_y_inside = self.y < mouse_y < self.y + self.h
     if is_x_inside and is_y_inside:
         self.clicked()


 def render(self):
    fill("white")
    stroke("black")
    stroke_weight(5)
    rect(self.x, self.y, self.s, self.s)

create_board(2, 8)
create_board(9, 15)

def setup():
    size(screen_width, screen_height)

def draw():
    background(0, 20, 60)
    for square in board:
        square.render()

run()