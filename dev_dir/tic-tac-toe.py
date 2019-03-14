import tkinter as tk
from tkinter import messagebox
import logging


def start_game():
    logging.debug('initializing tk window')
    tk_window = tk.Tk()
    tk_window.title('Tic-Tac-Toe Game')

    tk_window.minsize(width=100, height=100)
    side_length = min(tk_window.winfo_screenwidth() // 4, tk_window.winfo_screenheight() // 4)
    x = (tk_window.winfo_screenwidth() - side_length) // 2
    y = (tk_window.winfo_screenheight() - side_length) // 2
    logging.debug('side length: {}'.format(side_length))
    logging.debug('x window position: {}'.format(x))
    logging.debug('y window position: {}'.format(y))
    tk_window.geometry('{width}x{height}+{x}+{y}'.format(width=side_length, height=side_length, x=x, y=y))
    tk_window.resizable(False, False)
    
    letter = choose_letter()

    logging.debug('tk main loop started')
    tk_window.mainloop()

def choose_letter():
    if messagebox.askyesno('X?', 'Would you like to play with X?'):
        return 'X'
    return 'O'

if __name__ == '__main__':
    logging.basicConfig(filename="tic-tac-toe.log", level=logging.DEBUG)

    start_game()
