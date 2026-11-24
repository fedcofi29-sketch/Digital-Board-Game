from p5 import *
import random

screen_width = 800
screen_height = 640
left_board = []
right_board = []
l_b_edges = []
r_b_edges = []
board = [left_board, right_board]
players = []
# Where the dots should appear relative to the dice size
dot_cords = {
    #  [multiply x by, mulitply y by, radius]
    0: [],
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
options = []
projections = []
# Only one indicator, so it is just overwritten
turn_indicator = ''
# Moves are explained in the rules
# The names are from my original draft, subject to change
text_reqs = ["Survey", 1, "Void", 2, "Expand", 3, "Recharge", "Reset and Flip"]

def create_board(cStart, cEnd, side):
    square_size = 40
    for i in range(3, 9):
        row = square_size*i+60
        for j in range (cStart, cEnd):
            column = square_size*j+40
            # There is probably a way to shortcut the if/else but this should work for now
            if side == "left":
                left_board.append(GridSquare(column, row, square_size))
            elif side == "right":
                right_board.append(GridSquare(column, row, square_size))
    y_low = square_size*3+60
    y_high = square_size*9+60
    x_low = square_size*cStart+40
    x_high = square_size*cEnd+40
    if side == "left":
        l_b_edges.extend([x_low, x_high, y_low, y_high])
    elif side == "right":
        r_b_edges.extend([x_low, x_high, y_low, y_high])


def create_players(player_board, color, side):
    start = random.choice(player_board)
    x, y, s = center_cords_in_grid(start.x, start.y, start.s)
    players.append(DicePlayer(x, y, s, color, start, side))


def center_cords_in_grid(sq_x, sq_y, sq_s):
    s_length = sq_s/10 * 6
    x_cord = sq_x + (sq_s/2 - s_length/2)
    y_cord = sq_y + (sq_s/2 - s_length/2) 
    return x_cord, y_cord, s_length


def create_options_and_indicator(text_reqs):
    # Centers on the screen
    x = screen_width/2 - (120*4+20*4+60)/2
    for i in range(0, len(text_reqs), 2):
        options.append(MoveOptions(x, 80, 120, 60, text_reqs[i], text_reqs[i+1]))
        x += 140
    return TurnIndicator(x, 80, 60)


def update_dice_location(x, y, s, square, num):
    x1, y1, s1 = center_cords_in_grid(x, y, s)
    active = next((dice for dice in players if dice.color == turn_indicator.color), None)
    i = players.index(active)
    players[i].x = x1
    players[i].y = y1
    players[i].s = s1
    players[i].square = square
    players[i].num = num
    projections.clear()
    if active.color == "salmon":
        turn_indicator.color = "green"
    elif active.color == "green":
        turn_indicator.color = "salmon"
    for option in options:
        option.color = "blue"



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


class GridSquare(Hitbox):
    def __init__(self, x, y, s):
        # hitbox uses w and h so the squares will have those stored a the same as s
        super().__init__(x, y, s, s)
        self.s = s
        self.color = "white"
        self.tiled = False

    def checkmousepressed(self):
        super().checkmousepressed()

    # could add something that if no values hit, it displays a temporary message saying you can't move there
    def clicked(self):
        for projection in projections:
            if self.x < projection.x < self.x+self.s and self.y < projection.y < self.y+self.s:
                # This is a global function because I wasn't sure how else to update the dice from within the gridSquare
                update_dice_location(self.x, self.y, self.s, self, projection.num)
            


    def render(self):
        fill(self.color)
        stroke("black")
        stroke_weight(5)
        square(self.x, self.y, self.s)


class MoveOptions(Hitbox):
    def __init__(self, x, y, w, h, action, cost):
        super().__init__(x, y, w, h)
        self.action = action
        self.cost = cost
        self.color = "blue"

    def render(self):
        fill(self.color)
        stroke_weight(4)
        stroke("black")
        text_align("CENTER")
        text_size(15)
        rect(self.x, self.y, self.w, self.h)
        no_stroke()
        fill("white")
        text(self.action, self.x+self.w/2, self.y+self.h/3)
        text(str(self.cost), self.x+self.w/2, self.y+self.h*2/3)

    def checkmousepressed(self):
        super().checkmousepressed()

    def clicked(self):
        # Probably not the most efficient way to filter but it works for now
        # Worth keeping in mind that this could amount to lag if mulitple functions have to iterate through whole lists
        nothing_active = True
        for option in options:
            if option.color == "gray":
                nothing_active = False
        if nothing_active:
            self.color = "gray"
            self.create_projections()
        elif self.color == "gray":
            self.color = "blue"
            projections.clear()

    def create_projections(self):
        # Active player matches turn indicator color
        active = next((dice for dice in players if dice.color == turn_indicator.color), None)
        color = "light" + active.color
        if self.action == "Survey" or self.action == "Void":
            sq_x = active.square.x
            sq_y = active.square.y
            sq_s = active.square.s       
            self.create_orthagonal_projections(sq_x, sq_y, sq_s, color, self.cost, active.side, active.num)
            if self.action == "Survey":
                self.create_diagonal_projections(sq_x, sq_y, sq_s, color, self.cost, active.side, active.num)
            if self.action == "Void":
                self.create_tile_projection(sq_x, sq_y, sq_s, color)
        elif self.action == "Recharge":
            if active.side == "left":
                i = left_board.index(active.square)
                target = right_board[i]
            if active.side == "right":
                i = right_board.index(active.square)
                target = left_board[i]
            sq_x = target.x
            sq_y = target.y
            sq_s = target.s
            self.create_recharge_projection(sq_x, sq_y, sq_s, color, self.cost)
            
            
    # There might be a way to loop through this, but creating each manually is fine
    def create_orthagonal_projections(self, x, y, s, color, cost, side, num):
        # Created in clockwise order starting from top to make it easier to debug
        x1, y1, s1 = center_cords_in_grid(x, y-s, s)
        if self.cords_in_board(x1, y1, side):
            projections.append(Projections(x1, y1, s1, color, cost, num, 'dice'))

        x2, y2, s2 = center_cords_in_grid(x+s, y, s)
        if self.cords_in_board(x2, y2, side):
            projections.append(Projections(x2, y2, s2, color, cost, num, 'dice'))

        x3, y3, s3 = center_cords_in_grid(x, y+s, s)
        if self.cords_in_board(x3, y3, side):
            projections.append(Projections(x3, y3, s3, color, cost, num, 'dice'))

        x4, y4, s4 = center_cords_in_grid(x-s, y, s)
        if self.cords_in_board(x4, y4, side):
            projections.append(Projections(x4, y4, s4, color, cost, num, 'dice'))

    def create_diagonal_projections(self, x, y, s, color, cost, side, num):
            # Created in clockwise order starting from top to make it easier to debug
            x1, y1, s1 = center_cords_in_grid(x+s, y-s, s)
            if self.cords_in_board(x1, y1, side):
                projections.append(Projections(x1, y1, s1, color, cost, num, 'dice'))
    
            x2, y2, s2 = center_cords_in_grid(x+s, y+s, s)
            if self.cords_in_board(x2, y2, side):
                projections.append(Projections(x2, y2, s2, color, cost, num, 'dice'))
    
            x3, y3, s3 = center_cords_in_grid(x-s, y+s, s)
            if self.cords_in_board(x3, y3, side):
                projections.append(Projections(x3, y3, s3, color, cost, num, 'dice'))
    
            x4, y4, s4 = center_cords_in_grid(x-s, y-s, s)
            if self.cords_in_board(x4, y4, side):
                projections.append(Projections(x4, y4, s4, color, cost, num, 'dice'))

    # I feel like it will probably be useful in the future to have this as a function even if it is only one line
    def create_tile_projection(self, x, y, s, color):
        projections.append(Projections(x, y, s, color, '', '', 'tile'))

    def create_recharge_projection(self, x, y, s, color, cost):
        x1, y1, s1 = center_cords_in_grid(x, y, s)
        projections.append(Projections(x1, y1, s1, color, cost, '', 'tile'))
        

    def cords_in_board(self, x, y, side):
        if side == "left":
            edges = l_b_edges
        elif side == "right":
            edges = r_b_edges
        if edges[0] < x < edges[1] and edges[2] < y < edges[3]:
            return True
        else:
            return False

# Used gridSquare for init and render despite them having different functions
class TurnIndicator(GridSquare):
    def __init__(self, x, y, s):
        super().__init__(x, y, s)
        self.color = random.choice(["salmon", "green"])

    def render(self):
        super().render()


class DicePlayer:
    def __init__(self, x, y, s, color, square, side):
        self.x = x
        self.y = y
        self.s = s
        self.color = color
        self.square = square
        self.side = side
        self.num = random.randint(1,6)

    def render(self):
        fill(self.color)
        stroke_weight(2)
        # For tile projection to look cleaner
        if self.num == 0:
            stroke_weight(5)
        square(self.x, self.y, self.s)


# The class itself is pretty simple, most of the work is how they are created
class Projections(DicePlayer):
    def __init__(self, x, y, s, color, cost, num, type):
        super().__init__(x, y, s, color, '', '')
        # Projection shows value after cost or reset
        self.num = num
        if isinstance(cost, (int, float)):
            self.num += cost
        # num = 0 is for tile projections
        elif cost == '':
            self.num = 0
        else:
            self.num = 1
        self.type = type

    def render(self):
        super().render()


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


def mouse_pressed(e):
    for option in options:
        option.checkmousepressed()
    for side in board:
        for square in side:
            square.checkmousepressed()




# Create all objects
create_board(2, 8, "left")
create_board(9, 15, "right")
create_players(left_board, "green", "left")
# Salmon is kind of ugly but I needed two colors that had a "light____" variant for projections
create_players(right_board, "salmon", "right")
# Moves are explained in rules
# Kind of a messy solution but uses return and list appends to get both
turn_indicator = create_options_and_indicator(text_reqs)

def setup():
    size(screen_width, screen_height)
    arial = create_font("arial.ttf")
    text_font(arial)

def draw():
    background(0, 20, 60)
    for side in board:
        for square in side:
            square.render()
    for projection in projections:
        projection.render()
        dots.append(Dots(projection.num, projection))
    for dice in players:
        dice.render()
        dots.append(Dots(dice.num, dice)) 
    for dot in dots:
        dot.render()
    # Idk if this is the cleanest way to store dots
    # In game, they would reset after every move, so maybe there is way to keep it relative to that
    dots.clear()
    for option in options:
        option.render()    
    turn_indicator.render()


run()