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
last_move_right_time = 0
DAS_start_time_right = 0
last_move_left_time = 0
DAS_start_time_left = 0
DAS_time = 0.150
ARR_time = 0.050
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

def move_left(frame, piece_row, piece_col):
    if piece_col <= 0:
        return piece_col
    if frame[piece_row][piece_col - 1] == 1:
        return piece_col
    
    piece_col -= 1
    frame[piece_row][piece_col + 1] = 0
    frame[piece_row][piece_col] = 1
    return piece_col

def move_right(frame, piece_row, piece_col): # Bound conditions moved here to separate piece state from horizontal()
    if piece_col >= 9:
        return piece_col
    if (frame[piece_row][piece_col + 1] == 1):
        return piece_col
    
    piece_col += 1
    frame[piece_row][piece_col - 1] = 0
    frame[piece_row][piece_col] = 1
    return piece_col

def lateral_movement(current_time): # just for coords changes
    # if piece_col != 9 and frame[piece_row][piece_col + 1] != 1:
    #     if key == 'right':
    #         return move_right(frame, piece_row, piece_col)
    # if piece_col != 0 and frame[piece_row][piece_col - 1] != 1:
    #     if key == 'left':
    #         return move_left(frame, piece_row, piece_col)
    # return piece_col

    if right_pressed and not right_previous_pressed:
        move_right()
        last_move_time_right = current_time
        DAS_start_time_right = current_time
    elif right_pressed and right_previous_pressed:
        if (current_time - DAS_start_time_right) >= DAS_time:
            if (current_time - last_move_time_right) >= ARR_time:
                move_right()
                last_move_time_right = current_time
    if left_pressed and not left_previous_pressed:
        move_left()
        last_move_time_left = current_time
        DAS_start_time_left = current_time
    elif left_pressed and left_previous_pressed:
        if (current_time - DAS_start_time_left) >= DAS_time:
            if (current_time - last_move_time_left) >= ARR_time:
                move_left()
                last_move_time_left = current_time

    return piece_col, left_pressed, right_pressed

def take_input(left_pressed, right_pressed):
    left_pressed = keyboard.is_pressed("left")
    right_pressed = keyboard.is_pressed("right")


# Do I gotta add all arguments or nah??
def game_loop(key, frame, piece_row, piece_col, game_interval, falling_interval, last_grav_time):
    while piece_row < 19 and frame[piece_row + 1][piece_col] != 1:
        current_time = time.time() # to do: gotta make this grav loop into a function
        difference = current_time - last_grav_time
        render_window(frame)
        key = take_input(key) # no clue what variable this actually is
        if difference >= falling_interval:
            piece_row = vertical_movement(frame, piece_row, piece_col)
            piece_col, left_pressed, right_pressed = lateral_movement(current_time)
            last_grav_time = current_time
        right_previous_pressed = right_pressed
        left_previous_pressed = left_pressed
        time.sleep(game_interval)  
        print("\033[H", end="") # Note to : learn this shit
    return last_grav_time, right_previous_pressed, left_previous_pressed
    
        

while True:
    game_loop(key, frame, piece_row, piece_col, game_interval, falling_interval, last_grav_time)
