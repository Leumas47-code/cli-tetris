import time
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
piece_col = 5
key = ""
right_pressed = False
right_previous_pressed = False
left_pressed = False
left_previous_pressed = False
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

def vertical_movement(frame, piece_row, piece_col): # sexiest function I ever saw
    piece_row += 1
    frame[piece_row - 1][piece_col] = 0
    frame[piece_row][piece_col] = 1
    return piece_row

def lateral_movement(right_pressed, left_pressed, frame, piece_row, piece_col): # just for coords changes
    if piece_col != 9 and frame[piece_row][piece_col + 1] != 1:
        if right_pressed:
            piece_col += 1
            frame[piece_row][piece_col - 1] = 0
            frame[piece_row][piece_col] = 1
    if piece_col != 0 and frame[piece_row][piece_col - 1] != 1:
        if left_pressed:
            piece_col -= 1
            frame[piece_row][piece_col + 1] = 0
            frame[piece_row][piece_col] = 1
    return piece_col

def take_input(key, left_pressed, right_pressed): # total shit, need to add single key presses
    if keyboard.is_pressed("left"):
        left_pressed = True
    if keyboard.is_pressed("right"):
        right_pressed = True
    if keyboard.is_pressed("esc"):
        pass
    return key, left_pressed, right_pressed

# Do I gotta add all arguments or nah??
def game_loop(key, frame, piece_row, piece_col, 
              game_interval, falling_interval, 
              last_grav_time, left_pressed, 
              right_pressed, left_previous_pressed, 
              right_previous_pressed):
    while piece_row < 19 and frame[piece_row + 1][piece_col] != 1:
        current_time = time.time() # to do: gotta make this grav loop into a function
        difference = current_time - last_grav_time
        render_window(frame)
        key, left_pressed, right_pressed = take_input(key, left_pressed, right_pressed)

        single_right = (right_pressed == True and right_previous_pressed == False)
        held_right = (right_pressed == True and right_previous_pressed == True)
        single_left = (left_pressed == True and left_previous_pressed == False)
        held_left = (left_pressed == True and left_previous_pressed == True)

        if single_right:  
            if difference >= falling_interval:
                piece_row = vertical_movement(frame, piece_row, piece_col)
                piece_col = lateral_movement(right_pressed, left_pressed, key, frame, piece_row, piece_col)
                last_grav_time = current_time
        if single_left:
            if difference >= falling_interval:
                piece_row = vertical_movement(frame, piece_row, piece_col)
                piece_col = lateral_movement(right_pressed, left_pressed, key, frame, piece_row, piece_col)
                last_grav_time = current_time
        if held_right: # Does not trigger at same time as line 97 because conditions are different
            if difference >= falling_interval:
                piece_row = vertical_movement(frame, piece_row, piece_col)
                piece_col = lateral_movement(right_pressed, left_pressed, key, frame, piece_row, piece_col)                last_grav_time = current_time
                last_grav_time = current_time        
        if held_left:
            if difference >= falling_interval:
                piece_row = vertical_movement(frame, piece_row, piece_col)
                piece_col = lateral_movement(right_pressed, left_pressed, key, frame, piece_row, piece_col)
                last_grav_time = current_time
        right_previous_pressed = right_pressed # Updating for single click
        left_previous_pressed = left_pressed
        time.sleep(game_interval)  
        print("\033[H", end="") # Note to self: learn this shit
    return last_grav_time
    
        

while True:
    game_loop(key, frame, piece_row, piece_col, 
              game_interval, falling_interval, 
              last_grav_time, right_pressed, 
              left_pressed, right_previous_pressed, 
              left_previous_pressed)