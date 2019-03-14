import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas
import logging


class TicTacToe:
    
    def __init__(self):
        self.tk_window = tk.Tk()
        self.init_gui()


    def init_gui(self):
        logging.debug('initializing tk window')
        self.tk_window.title('Tic-Tac-Toe Game')

        self.tk_window.minsize(width=100, height=100)
        side_length = min(self.tk_window.winfo_screenwidth() // 4, self.tk_window.winfo_screenheight() // 4)
        x = (self.tk_window.winfo_screenwidth() - side_length) // 2
        y = (self.tk_window.winfo_screenheight() - side_length) // 2
        logging.debug('side length: {}'.format(side_length))
        logging.debug('x window position: {}'.format(x))
        logging.debug('y window position: {}'.format(y))
        self.tk_window.geometry('{width}x{height}+{x}+{y}'.format(width=side_length, height=side_length, x=x, y=y))
        self.tk_window.resizable(False, False)

        self.tk_canvas = Canvas(self.tk_window, width=side_length, height=side_length)
        self.tk_canvas.pack()
        
        # Grid
        margin = side_length // 20
        self.tk_canvas.create_rectangle(margin, margin, side_length - margin, side_length - margin)
        grid_gap = (side_length - 2 * margin) / 3
        self.tk_canvas.create_rectangle(margin + grid_gap, margin, margin + grid_gap * 2, side_length - margin)
        self.tk_canvas.create_rectangle(margin, margin + grid_gap, side_length - margin, margin + grid_gap * 2)


    def choose_letter(self):
        if messagebox.askyesno('X?', 'Would you like to play with X?'):
            return 'X', 'O'
        return 'O', 'X'


    def play(self):
        # letter, opponent_letter = self.choose_letter()
        self.tk_window.mainloop()


if __name__ == '__main__':
    logging.basicConfig(filename="tic-tac-toe.log", level=logging.DEBUG)

    game = TicTacToe()
    game.play()