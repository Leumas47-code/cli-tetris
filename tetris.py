import time
import keyboard

class TetrisGame:
    def __init__(self):
        self.frame = [[0] * 10 for _ in range(20)] # Loop to create fram
        self.game_interval = 0.001
        self.falling_interval = 0.1
        self.piece_row = 0
        self.piece_col = 5 # Center column
        self.key = "" # Default before input
        self.right_pressed = False
        self.right_previous_pressed = False
        self.left_pressed = False
        self.left_previous_pressed = False
    
    def render_window(self):
        for row in self.frame:
            line = ""
            for cell in row:
                if cell == 0:
                    line += " • " # changed each tile to 3 characters wide for more square shape
                elif cell == 1:
                    line += "[ ]"
            print(line)
    
    def vertical_movement(self):
        self.piece_row += 1
        self.frame[self.piece_row - 1][self.piece_col] = 0
        self.frame[self.piece_row][self.piece_col] = 1
        return self.piece_row

    def lateral_movement(self): # Horizontal movement
        if self.piece_col != 9 and self.frame[self.piece_row + 1][self.piece_col] != 1:
            if self.right_pressed:
                self.piece_col += 1
                self.frame[self.piece_row][self.piece_col - 1] = 0
                self.frame[self.piece_row][self.piece_col] = 1
        if self.piece_col != 0 and self.frame[self.piece_row + 1][self.piece_col] != 1:
            if self.left_pressed:
                self.piece_col -= 1
                self.frame[self.piece_row][self.piece_col + 1] = 0
                self.frame[self.piece_row][self.piece_col] = 1
        return self.piece_col
    
    def game_loop(self):
        while self.piece_row < 19 and self.frame[self.piece_row + 1][self.piece_col] != 1:
            current_time = time.time() # to do: gotta make this grav loop into a function
            difference = current_time - self.last_grav_time
            self.render_window(self.frame)
            self.key, self.left_pressed, self.right_pressed = self.take_input(self.key, self.left_pressed, self.right_pressed)

            

            single_right = (self.right_pressed == True and self.right_previous_pressed == False)
            held_right = (self.right_pressed == True and self.right_previous_pressed == True)
            single_left = (self.left_pressed == True and self.left_previous_pressed == False)
            held_left = (self.left_pressed == True and self.left_previous_pressed == True)

            if single_right:  
                if difference >= self.falling_interval:
                    self.piece_row = self.vertical_movement(self.frame, self.piece_row, self.piece_col)
                    self.piece_col = self.lateral_movement(self.right_pressed, self.left_pressed, self.frame, self.piece_row, self.piece_col)
                    self.last_grav_time = current_time
            if single_left:  
                if difference >= self.falling_interval:
                    self.piece_row = self.vertical_movement(self.frame, self.piece_row, self.piece_col)
                    self.piece_col = self.lateral_movement(self.right_pressed, self.left_pressed, self.frame, self.piece_row, self.piece_col)
                    self.last_grav_time = current_time
            if held_right:  
                if difference >= self.falling_interval:
                    self.piece_row = self.vertical_movement(self.frame, self.piece_row, self.piece_col)
                    self.piece_col = self.lateral_movement(self.right_pressed, self.left_pressed, self.frame, self.piece_row, self.piece_col)
                    self.last_grav_time = current_time
            if held_left:  
                if difference >= self.falling_interval:
                    self.piece_row = self.vertical_movement(self.frame, self.piece_row, self.piece_col)
                    self.piece_col = self.lateral_movement(self.right_pressed, self.left_pressed, self.frame, self.piece_row, self.piece_col)
                    self.last_grav_time = current_time
            self.right_previous_pressed = self.right_pressed # Updating for single click
            self.left_previous_pressed = self.left_pressed
            time.sleep(self.game_interval)  
            print("\033[H", end="") # Note to self: learn this shit
        return self.last_grav_time
        
            

while True:
    game = TetrisGame()
    print(game)
    
