import time
import keyboard

class TetrisGame:
    def __init__(self):
        self.frame = [[0] * 10 for _ in range(20)] # Loop to create frame
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
        self.last_move_time_left = 0
        self.last_move_time_right = 0
        self.DAS_time = 0.150 # Since last movement
        self.DAS_start_time_left = 0
        self.DAS_start_time_right = 0
        self.ARR_time = 0.05 # Interval between movement
    
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
        self.left_pressed = keyboard.is_pressed("left")
        self.right_pressed = keyboard.is_pressed("right")

    def fall(self):
        self.piece_row += 1
        if self.piece_row > 0:
            self.frame[self.piece_row - 1][self.piece_col] = 0
        self.frame[self.piece_row][self.piece_col] = 1
        return self.piece_row
    
    def move_right(self):
        if self.piece_col >= 9:
            return self.piece_col
        if (self.frame[self.piece_row][self.piece_col + 1] == 1):
            return self.piece_col
        
        self.piece_col += 1
        self.frame[self.piece_row][self.piece_col - 1] = 0
        self.frame[self.piece_row][self.piece_col] = 1
        return self.piece_col

    def move_left(self):
        if self.piece_col <= 0:
            return self.piece_col
        if (self.frame[self.piece_row][self.piece_col - 1] == 1):
            return self.piece_col
        
        self.piece_col -= 1
        self.frame[self.piece_row][self.piece_col + 1] = 0
        self.frame[self.piece_row][self.piece_col] = 1
        return self.piece_col
    
    def horizontal(self, current_time):
        if self.right_pressed and not self.right_previous_pressed:
            self.move_right()
            self.last_move_time_right = current_time
            self.DAS_start_time_right = current_time
        elif self.right_pressed and self.right_previous_pressed:
            if (current_time - self.DAS_start_time_right) >= self.DAS_time:
                if (current_time - self.last_move_time_right) >= self.ARR_time:
                    self.move_right()
                    self.last_move_time_right = current_time
        if self.left_pressed and not self.left_previous_pressed:
            self.move_left()
            self.last_move_time_left = current_time
            self.DAS_start_time_left = current_time
        elif self.left_pressed and self.left_previous_pressed:
            if (current_time - self.DAS_start_time_left) >= self.DAS_time:
                if (current_time - self.last_move_time_left) >= self.ARR_time:
                    self.move_left()
                    self.last_move_time_left = current_time
    
        return self.left_pressed, self.right_pressed
    
    def game_loop(self):
        while self.piece_row < 19 and self.frame[self.piece_row + 1][self.piece_col] != 1:
            current_time = time.time() # to do: gotta make this grav loop into a function
            fall_difference = current_time - self.last_grav_time
            self.render_window()
            self.take_input()

            if fall_difference >= self.falling_interval:
                self.piece_row = self.fall()
                self.last_grav_time = current_time

            self.horizontal(current_time)
            self.right_previous_pressed = self.right_pressed
            self.left_previous_pressed = self.left_pressed
            time.sleep(self.game_interval)  
            print("\033[H", end="") # Note to self: learn this shit
        return self.last_grav_time, self.last_move_time_left, self.last_move_time_right
        
while True:
    game = TetrisGame()
    game.game_loop()
    
