import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas
import logging


class TicTacToe(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Tic-Tac-Toe Game')

        # Window geometry
        self.minsize(width=100, height=100)
        side_length = min(self.winfo_screenwidth() // 4, self.winfo_screenheight() // 4)
        x = (self.winfo_screenwidth() - side_length) // 2
        y = (self.winfo_screenheight() - side_length) // 2
        self.geometry('{width}x{height}+{x}+{y}'.format(width=side_length, height=side_length, x=x, y=y))
        self.resizable(False, False)

        # Main canvas
        self.canvas = Canvas(self, width=side_length, height=side_length, bg='gray')
        self.canvas.pack()
        
        # Grid and cells binding with callback click-on function
        margin = side_length // 20
        grid_gap = (side_length - 2 * margin) // 3
        self.cells_coords = [[(margin + j * grid_gap, margin + i * grid_gap, margin + (j + 1) * grid_gap, margin + (i + 1) * grid_gap)
                            for j in range(3)] for i in range(3)]

        self.cells_coords = self.cells_coords[0] + self.cells_coords[1] + self.cells_coords[2]
        
        for cell_i in range(9):
            self.canvas.create_rectangle(self.cells_coords[cell_i][0],
                                            self.cells_coords[cell_i][1],
                                            self.cells_coords[cell_i][2],
                                            self.cells_coords[cell_i][3],
                                            tags=str(cell_i),
                                            fill='grey')
            self.canvas.tag_bind(str(cell_i + 1), '<ButtonPress-1>', self.player_turn)

        # Game logic initializing
        self.letters = ['-'] * 9
        self.player_letter = 'X'
        self.opponent_letter = 'O'

        self.mainloop()
    

    def player_turn(self, event):
        logging.debug('canvas click x:{} y:{}'.format(event.x, event.y))

        x = event.x
        y = event.y

        for cell_number in range(9):
            if (self.cells_coords[cell_number][0] < x and x < self.cells_coords[cell_number][2] and
                self.cells_coords[cell_number][1] < y and y < self.cells_coords[cell_number][3]):
                break
        logging.debug('cell {} selected'.format(cell_number))

        if self.letters[cell_number] == '-':
            self.letters[cell_number] = self.player_letter
            self.draw_letter(cell_number, self.player_letter)

            self.opponent_turn()

    
    def draw_letter(self, cell_number, letter):
        x = (self.cells_coords[cell_number][2] + self.cells_coords[cell_number][0]) // 2
        y = (self.cells_coords[cell_number][3] + self.cells_coords[cell_number][1]) // 2
        font_size = (self.cells_coords[cell_number][3] - self.cells_coords[cell_number][1]) // 3
        self.canvas.create_text(x, y, font='Times {}'.format(font_size), text=letter)


    def opponent_turn(self):
        pass



if __name__ == '__main__':
    logging.basicConfig(filename="tic-tac-toe.log", level=logging.DEBUG)

    game = TicTacToe()