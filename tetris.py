import time
import keyboard

class TetrisGame:
    def __init__(self):
        self.frame = [[0] * 10 for _ in range(20)] # Loop to create fram
        self.game_interval = 0.001
        self.falling_interval = 0.1
        self.move_interval = 0.1
        self.piece_row = 0
        self.piece_col = 5 # Center column
        self.right_pressed = False
        self.right_previous_pressed = False
        self.left_pressed = False
        self.left_previous_pressed = False
        self.last_grav_time = time.time()
        self.last_move_time = time.time()
    
    def render_window(self):
        for row in self.frame:
            line = ""
            for cell in row:
                if cell == 0:
                    line += " • " # changed each tile to 3 characters wide for more square shape
                elif cell == 1:
                    line += "[ ]"
            print(line)
    
    def take_input(self):
        if keyboard.is_pressed("left"):
            self.left_pressed = True
        if keyboard.is_pressed("right"):
            self.right_pressed = True
        return self.right_pressed, self.left_pressed

    def vertical_movement(self):
        self.piece_row += 1
        self.frame[self.piece_row - 1][self.piece_col] = 0
        self.frame[self.piece_row][self.piece_col] = 1
        return self.piece_row

    def lateral_movement(self): # Horizontal movement
        
        single_right = (self.right_pressed and not self.right_previous_pressed)
        held_right = (self.right_pressed and self.right_previous_pressed)
        single_left = (self.left_pressed and not self.left_previous_pressed)
        held_left = (self.left_pressed and self.left_previous_pressed)

        if self.piece_col != 9 and self.frame[self.piece_row + 1][self.piece_col] != 1:
            if single_right:
                self.piece_col += 1
                self.frame[self.piece_row][self.piece_col - 1] = 0
                self.frame[self.piece_row][self.piece_col] = 1
            elif held_right:
                self.piece_col += 1
                self.frame[self.piece_row][self.piece_col - 1] = 0
                self.frame[self.piece_row][self.piece_col] = 1
        if self.piece_col != 0 and self.frame[self.piece_row + 1][self.piece_col] != 1:
            if single_left:
                self.piece_col -= 1
                self.frame[self.piece_row][self.piece_col + 1] = 0
                self.frame[self.piece_row][self.piece_col] = 1
            if held_left:
                self.piece_col -= 1
                self.frame[self.piece_row][self.piece_col + 1] = 0
                self.frame[self.piece_row][self.piece_col] = 1

        self.right_previous_pressed = self.right_pressed
        self.left_previous_pressed = self.left_pressed
        return self.piece_col
    
    def game_loop(self):
        while self.piece_row < 19 and self.frame[self.piece_row + 1][self.piece_col] != 1:
            current_time = time.time() # to do: gotta make this grav loop into a function
            fall_difference = current_time - self.last_grav_time
            move_difference = current_time - self.last_move_time
            self.render_window(self.frame)
            self.left_pressed, self.right_pressed = self.take_input(self.left_pressed, self.right_pressed)

            if fall_difference >= self.falling_interval:
                self.piece_row = self.vertical_movement()
                self.last_grav_time = time.time()

            if move_difference >= self.move_interval:
                self.piece_col = self.lateral_movement()
                self.last_move_time = time.time()

            time.sleep(self.game_interval)  
            print("\033[H", end="") # Note to self: learn this shit
        return self.last_grav_time, self.last_move_time

        
while True:
    game = TetrisGame()
    game.game_loop()
    
