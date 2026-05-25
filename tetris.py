import time
import random as rd
import keyboard

frame = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Start at top row, random column
game_interval = 0.001
last_grav_time = time.time()
falling_interval = 0.1
piece_row = 0 
piece_col = rd.randint(0, len(frame[0]) - 1)
key = ""
right_pressed = False
left_pressed = False
time.sleep(game_interval) # not sure what for, but scared to remove

def render_window(frame):
    for row in frame:
        line = ""
        for cell in row:
            if cell == 0:
                line += " • " # changed each tile to 3 characters wide for more square shape
            elif cell == 1:
                line += "[ ]"
        print(line)

def vertical_movement(frame, piece_row, piece_col, game_interval): # sexiest function I ever saw
    piece_row += 1
    frame[piece_row - 1][piece_col] = 0
    frame[piece_row][piece_col] = 1
    return piece_row

def lateral_movement(key, frame, piece_row, piece_col): # just for coords changes
    if piece_col != 9 and frame[piece_row][piece_col + 1] != 1:
        if key == 'right':
            piece_col += 1
            frame[piece_row][piece_col - 1] = 0
            frame[piece_row][piece_col] = 1
    if piece_col != 0 and frame[piece_row][piece_col - 1] != 1:
        if key == 'left':
            piece_col -= 1
            frame[piece_row][piece_col + 1] = 0
            frame[piece_row][piece_col] = 1
    return piece_col

def take_input(key, right_pressed, left_pressed): # total shit, need to add single key presses

    if keyboard.is_pressed("left"):
        left_pressed = True 
        key = "left"
    if keyboard.is_pressed("right"):
        right_pressed = True
        key = "right"
    if keyboard.is_pressed("esc"):
        key = "esc"
    return key, right_pressed, left_pressed

# Do I gotta add all arguments or nah??
def game_loop(key, frame, piece_row, piece_col, game_interval, falling_interval, last_grav_time, right_pressed, left_pressed):
    while piece_row < 19 and frame[piece_row + 1][piece_col] != 1:
        current_time = time.time() # to do: gotta make this grav loop into a function
        difference = current_time - last_grav_time
        render_window(frame)
        key = take_input(key) # no clue what variable this actually is
        if difference >= falling_interval:
             piece_row = vertical_movement(frame, piece_row, piece_col, falling_interval)
             piece_col = lateral_movement(key, frame, piece_row, piece_col)
             last_grav_time = current_time
        
        time.sleep(game_interval)  
        print("\033[H", end="") # Note to self: learn this shit
    return last_grav_time
    
        

while True:
    game_loop(key, frame, piece_row, rd.randint(0, len(frame[0]) - 1), game_interval, falling_interval, last_grav_time)

# to do: remove random module cuz tetris blocks start at middle: len(frame[0])/2