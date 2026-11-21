from p5 import *
import random

screen_width = 800
screen_height = 640
left_board = []
right_board = []
board = [left_board, right_board]
players = []
# Where the dots should appear relative to the dice size
dot_cords = {
    #  [multiply x by, mulitply y by, radius]
    1: [1/2, 1/2, 1/3],
    2: [1/3, 1/3, 1/4,
        2/3, 2/3, 1/4],
    3: [1/4, 1/4, 1/5,
        2/4, 2/4, 1/5,
        3/4, 3/4, 1/5],
    4: [1/3, 1/3, 1/5,
        1/3, 2/3, 1/5,
        2/3, 1/3, 1/5,
        2/3, 2/3, 1/5],
    5: [1/4, 1/4, 1/5,
        1/4, 3/4, 1/5,
        2/4, 2/4, 1/5,
        3/4, 1/4, 1/5,
        3/4, 3/4, 1/5],
    6: [1/4, 1/4, 1/5,
        1/4, 3/4, 1/5,
        2/4, 1/4, 1/5,
        2/4, 3/4, 1/5,
        3/4, 1/4, 1/5,
        3/4, 3/4, 1/5],
}
dots = []

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
    s_length = start.s/10 * 6
    x_cord = start.x + (start.s/2 - s_length/2)
    y_cord = start.y + (start.s/2 - s_length/2) 
    players.append(DicePlayer(x_cord, y_cord, s_length, color))


# Used for options and grid, but there are no hitboxes on their own
class Hitbox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def checkmousepressed(self):
        is_x_inside = self.x < mouse_x < self.x + self.w
        is_y_inside = self.y < mouse_y < self.y + self.h
        if is_x_inside and is_y_inside:
            self.clicked()


class Grid_Square(Hitbox):
    def __init__(self, x, y, s):
        # hitbox uses w and h so the squares will have those stored a the same as s
        super().__init__(x, y, s, s)
        self.s = s
        self.tiled = False

    def checkmousepressed(self):
        super().checkmousepressed()

    # will be used for movement later
    def clicked(self):
        pass

    def render(self):
        fill("white")
        stroke("black")
        stroke_weight(5)
        square(self.x, self.y, self.s)


class MoveOptions(Hitbox):
    def __init__(self, x, y, w, h, action, cost):
        super().__init__(x, y, w, h)
        self.action = action
        self.cost = cost


class DicePlayer:
    def __init__(self, x, y, s, color):
        self.x = x
        self.y = y
        self.s = s
        self.color = color
        self.num = random.randint(1,6)

    def render(self):
        fill(self.color)
        stroke_weight(2)
        square(self.x, self.y, self.s)


class Dots:
    def __init__(self, num, dice):
        self.num = num
        self.dice = dice

    def render(self):
        no_stroke()
        fill("white")
        for i in range(0, len(dot_cords[self.num]), 3):
            x_cord = self.dice.x+(self.dice.s*dot_cords[self.num][i])
            y_cord = self.dice.y+(self.dice.s*dot_cords[self.num][i+1])
            radius = self.dice.s*dot_cords[self.num][i+2]
            circle(x_cord, y_cord, radius)






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
        dots.append(Dots(dice.num, dice))
    for dot in dots:
        dot.render()
    # Idk if this is the cleanest way to store dots
    # In game, they would reset after every move, so maybe there is way to keep it relative to that
    dots.clear()


run()