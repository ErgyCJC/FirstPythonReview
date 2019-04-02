import tkinter as tk
from tkinter import Canvas
from tkinter import Button
from tkinter import Label
import logging


class TicTacToe(tk.Tk):

    def __init__(self, board_size = 3):
        """ Sets window properties """
        logging.debug('init game obj')
        tk.Tk.__init__(self)
        self.title('Tic-Tac-Toe Game')

        # Window geometry
        self.minsize(width=100, height=100)
        self.board_size = board_size

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.side_length = min(screen_width // 2, screen_height // 2)

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
        grid_gap = (self.side_length - 2 * margin) // self.board_size

        logging.debug('grid_gap: {}'.format(grid_gap))

        self.cells_coords = [[(margin + j * grid_gap, margin + i * grid_gap, margin + (j + 1) * grid_gap, margin + (i + 1) * grid_gap)
        for j in range(self.board_size)] for i in range(self.board_size)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.canvas.create_rectangle(self.cells_coords[i][j][0],
                                            self.cells_coords[i][j][1],
                                            self.cells_coords[i][j][2],
                                            self.cells_coords[i][j][3],
                                            tags=str(i * self.board_size + j + 1),
                                            fill='grey')
                self.canvas.tag_bind(str(i * self.board_size + j + 1), '<ButtonPress-1>', self.player_turn)

        # Game logic initializing
        self.filled_cells_count = 0
        self.letters = [['-' for j in range(self.board_size)] for i in range(self.board_size)]
        self.players_letters = ['X', 'O']
        self.current_letter_index = 0

    def player_turn(self, event):
        """ Processes players clicks """
        logging.debug('canvas click x:{} y:{}'.format(event.x, event.y))

        x = event.x
        y = event.y

        result_i, result_j = None, None

        # Looking for cell with right coordinates
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (self.cells_coords[i][j][0] < x and
                    x < self.cells_coords[i][j][2] and
                    self.cells_coords[i][j][1] < y and
                    y < self.cells_coords[i][j][3]):
                    result_i, result_j = i, j
        logging.debug('cell {}x{} selected'.format(result_i, result_j))

        # Is it possible to put a letter into the cell
        if result_i is not None and result_j is not None and self.letters[result_i][result_j] == '-':
            self.filled_cells_count += 1
            current_letter = self.players_letters[self.current_letter_index]
            self.letters[result_i][result_j] = current_letter
            self.draw_letter(result_i, result_j, current_letter)

            # Looking for winner after turn
            winner = self.check_win_state(result_i, result_j)
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

    def draw_letter(self, cell_i, cell_j, letter):
        x = (self.cells_coords[cell_i][cell_j][2] + self.cells_coords[cell_i][cell_j][0]) // 2
        y = (self.cells_coords[cell_i][cell_j][3] + self.cells_coords[cell_i][cell_j][1]) // 2
        font_size = (self.cells_coords[cell_i][cell_j][3] - self.cells_coords[cell_i][cell_j][1]) // 3
        self.canvas.create_text(x, y, font='Times {}'.format(font_size), text=letter)

    def change_current_letter(self):
        self.current_letter_index = abs(self.current_letter_index - 1)
        logging.debug('change letter to index {}'.format(self.current_letter_index))

    def check_win_line(self, cells):
        base_y, base_x = cells[0][0], cells[0][1]
        
        for cell in cells:
            y, x = cell[0], cell[1]
            if x < 0 or y < 0 or x >= self.board_size or y >= self.board_size:
                logging.debug('line {} is not win-line: wrong coords'.format(cells))
                return None

            if self.letters[y][x] == '-' or self.letters[base_y][base_x] != self.letters[y][x]:
                logging.debug('line {} is not win-line: diff letters'.format(cells))
                return None

        logging.debug('line {} won'.format(cells))
        return self.letters[base_y][base_x]

    def check_win_state(self, cell_i, cell_j):
        """ Checking potential win-lines """

        line_len = 3 # Length of possible win-line
        
        # Vertical and horizontal lines and diagonals checking
        init_delta = 1 - line_len
        for delta in range(init_delta, init_delta + line_len):
            lines = []
            directions = 4
            for x in range(directions):
                lines.append([])

            for index in range(line_len):
                lines[0].append((cell_i + delta + index, cell_j))
                lines[1].append((cell_i, cell_j + delta + index))
                lines[2].append((cell_i + delta + index, cell_j + delta + index))
                lines[3].append((cell_i + delta + index, cell_j - delta - index))
            
            for index in range(directions):
                win_state = self.check_win_line(lines[index])
                if win_state is not None:
                    logging.debug('winner {}'.format(lines[index]))
                    return win_state

        if self.filled_cells_count == (self.board_size ** 2):
            return 'Noone'

        return None


if __name__ == '__main__':
    logging.basicConfig(filename="tic-tac-toe.log", level=logging.DEBUG)

    """
    Win line has always length 3.
    Win-combinations can be placed in 4 directions:
    vertical, horizontal and two diagonals.
    """

    game = TicTacToe()
