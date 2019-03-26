import tkinter as tk
from tkinter import Canvas
from tkinter import Button
from tkinter import Label
import logging


class TicTacToe(tk.Tk):

    def __init__(self):
        """ Sets window properties """
        logging.debug('init game obj')
        tk.Tk.__init__(self)
        self.title('Tic-Tac-Toe Game')

        # Window geometry
        self.minsize(width=100, height=100)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.side_length = min(screen_width // 4, screen_height // 4)

        x = (screen_width - self.side_length) // 2
        y = (screen_height - self.side_length) // 2

        window_size = '{}x{}'.format(self.side_length, self.side_length)
        init_coords = '{}+{}'.format(x, y)
        geometry_properties = '{}+{}'.format(window_size, init_coords)
        self.geometry(geometry_properties)
        self.resizable(False, False)

        self.show_game_field()

        self.mainloop()

    def show_game_field(self):
        """ Shows main game field and initialize game logic """
        logging.debug('make game field')

        # Main canvas
        self.canvas = Canvas(self, width=self.side_length, height=self.side_length, bg='gray')
        self.canvas.pack()

        # Grid and cells binding with click-on function
        margin = self.side_length // 20
        grid_gap = (self.side_length - 2 * margin) // 3

        logging.debug('grid_gap: {}'.format(grid_gap))

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
        self.filled_cells_count = 0
        self.letters = ['-'] * 9
        self.players_letters = ['X', 'O']
        self.current_letter_index = 0

    def player_turn(self, event):
        """ Processes players clicks """
        logging.debug('canvas click x:{} y:{}'.format(event.x, event.y))

        x = event.x
        y = event.y

        # Looking for cell with right coordinates
        for cell_number in range(9):
            if (self.cells_coords[cell_number][0] < x and
                x < self.cells_coords[cell_number][2] and
                self.cells_coords[cell_number][1] < y and
                y < self.cells_coords[cell_number][3]):
                break
        logging.debug('cell {} selected'.format(cell_number))

        # Is it possible to put a letter into the cell
        if self.letters[cell_number] == '-':
            self.filled_cells_count += 1
            current_letter = self.players_letters[self.current_letter_index]
            self.letters[cell_number] = current_letter
            self.draw_letter(cell_number, current_letter)

            # Looking for winner after turn
            winner = self.check_win_state()
            if winner is not None:
                self.show_win_window(winner)

            self.change_current_letter()

    def show_win_window(self, winner):
        """ Shows menu window after game (replay, exit) """
        logging.debug('win screen')
        self.canvas.destroy()

        self.replay_label = Label(self, text='{} won!\n\nDo you want to replay?'.format(winner))
        self.replay_label.pack()

        self.replay_button = Button(self, text='Replay', command=self.click_replay)
        self.replay_button.pack()

        self.exit_button = Button(self, text='Exit', command=self.click_exit)
        self.exit_button.pack()

    def click_exit(self):
        logging.debug('exit')
        exit()

    def click_replay(self):
        """ Replay call-back function """
        logging.debug('replay action')

        self.replay_label.pack_forget()
        self.replay_button.pack_forget()
        self.exit_button.pack_forget()
        self.show_game_field()

    def draw_letter(self, cell_number, letter):
        x = (self.cells_coords[cell_number][2] + self.cells_coords[cell_number][0]) // 2
        y = (self.cells_coords[cell_number][3] + self.cells_coords[cell_number][1]) // 2
        font_size = (self.cells_coords[cell_number][3] - self.cells_coords[cell_number][1]) // 3
        self.canvas.create_text(x, y, font='Times {}'.format(font_size), text=letter)

    def change_current_letter(self):
        self.current_letter_index = abs(self.current_letter_index - 1)
        logging.debug('change letter to index {}'.format(self.current_letter_index))

    def check_win_line(self, cells_indexies):
        for cell_number in cells_indexies:
            if self.letters[cell_number] == '-' or self.letters[cells_indexies[0]] != self.letters[cell_number]:
                logging.debug('line {} is not won'.format(cells_indexies))
                return None

        logging.debug('line {} won'.format(cells_indexies))
        return self.letters[cells_indexies[0]]

    def check_win_state(self):
        """ Checking potential win-lines """
        if self.filled_cells_count == 9:
            return 'None'

        lines = ['0 1 2', '3 4 5', '6 7 8', '0 3 6', '1 4 7', '2 5 8', '0 4 8', '2 4 6']
        lines = [list(map(int, x.split())) for x in lines]

        for line in lines:
            win_state = self.check_win_line(line)
            if win_state is not None:
                logging.debug('winner {}'.format(line))
                return win_state

        return None


if __name__ == '__main__':
    logging.basicConfig(filename="tic-tac-toe.log", level=logging.DEBUG)

    game = TicTacToe()
