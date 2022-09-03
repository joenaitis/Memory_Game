# Joe's simple game of memory, done as a project for the online course "An Introduction to Interactive Programming in Python"

# Select two cards and try to find the pair.
# If you find a pair, the pair will remain visible
# If you don't find a pair, the cards will flip back over
# Try to find all the pairs in the lowest amount of turns

import simpleguitk as simplegui
import random

# define globals
TILE_WIDTH = 50
TILE_HEIGHT = 100
DISTINCT_TILES = 8


# helper function to initialize globals
def new_game():
    global my_tiles, state, turns, list_of_clicked_tiles

    tile_numbers = list(range(DISTINCT_TILES))
    #print(tile_numbers)
    tile_numbers.extend(list(range(DISTINCT_TILES)))
    #print(tile_numbers)
    random.shuffle(tile_numbers)
    my_tiles = []
    for i in range(2 * DISTINCT_TILES):
        if i < DISTINCT_TILES:
            my_tiles.append(Tile(tile_numbers[i], False, [TILE_WIDTH * i, TILE_HEIGHT]))
        else:
            my_tiles.append(Tile(tile_numbers[i], False, [TILE_WIDTH * (i - DISTINCT_TILES), TILE_HEIGHT * 2]))

    print
    my_tiles
    # my_tiles = [Tile(tile_numbers[i], False, [TILE_WIDTH * i, TILE_HEIGHT]) for i in range(2 * DISTINCT_TILES)]

    state = 0
    turns = 0
    list_of_clicked_tiles = []


# definition of a Tile class
class Tile:

    # definition of intializer
    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc

    # definition of getter for number
    def get_number(self):
        return self.number

    # check whether tile is exposed
    def is_exposed(self):
        return self.exposed

    # expose the tile
    def expose_tile(self):
        self.exposed = True

    # hide the tile
    def hide_tile(self):
        self.exposed = False

    # string method for tiles
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)

        # draw method for tiles

    def draw_tile(self, canvas):
        loc = self.location
        if self.exposed:
            text_location = [loc[0] + 0.2 * TILE_WIDTH, loc[1] - 0.3 * TILE_HEIGHT]
            canvas.draw_text(str(self.number), text_location, TILE_WIDTH, "White")
        else:
            tile_corners = (loc, [loc[0] + TILE_WIDTH, loc[1]], [loc[0] + TILE_WIDTH, loc[1] - TILE_HEIGHT],
                            [loc[0], loc[1] - TILE_HEIGHT])
            canvas.draw_polygon(tile_corners, 1, "Red", "Green")

    # selection method for tiles
    def is_selected(self, pos):
        inside_hor = self.location[0] <= pos[0] < self.location[0] + TILE_WIDTH
        inside_vert = self.location[1] - TILE_HEIGHT <= pos[1] <= self.location[1]
        return inside_hor and inside_vert

    # define event handlers


def mouseclick(pos):
    global state, turns, turn1_tile, turn2_tile, list_of_clicked_tiles

    for tile in my_tiles:
        if tile.is_selected(pos):
            clicked_tile = tile

    if clicked_tile.is_exposed():
        return

    list_of_clicked_tiles.append(clicked_tile)
    # print list_of_clicked_tiles
    # print list_of_clicked_tiles[-1]
    clicked_tile.expose_tile()

    if state == 0:
        # clicked_tile.expose_tile()
        state = 1
    elif state == 1:
        # clicked_tile.expose_tile()
        state = 2
    else:
        if list_of_clicked_tiles[-3].get_number() == list_of_clicked_tiles[-2].get_number():
            # clicked_tile.expose_tile()
            state = 1
        else:
            list_of_clicked_tiles[-3].hide_tile()
            list_of_clicked_tiles[-2].hide_tile()
            state = 1

    label.set_text("Turns = " + str(len(list_of_clicked_tiles) // 2))


# draw handler
def draw(canvas):
    for tile in my_tiles:
        tile.draw_tile(canvas)


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", DISTINCT_TILES * TILE_WIDTH, TILE_HEIGHT * 2)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick)

# get things rolling
new_game()
frame.start()
