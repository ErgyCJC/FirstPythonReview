import tkinter as tk
import logging


def start_game():
    logging.debug('initializing tk window')
    tk_window = tk.Tk()
    tk_window.title('Tic-Tac-Toe Game')
    tk_window.minsize(width=100, height=100)
    side_length = min(tk_window.winfo_screenwidth() // 4, tk_window.winfo_screenheight() // 4)
    logging.debug('side length: ' + str(side_length))
    tk_window.geometry(str(side_length) + 'x' + str(side_length) + '+0+0')
    tk_window.resizable()

    

    logging.debug('tk main loop started')
    tk_window.mainloop()



if __name__ == '__main__':
    logging.basicConfig(filename="tic-tac-toe.log", level=logging.DEBUG)

    start_game()
