import tkinter as tk
from tkinter import Canvas
from tkinter import Button
from tkinter import Label
import logging


class CellInfo:
    def __init__(self, t_x = None, t_y = None, b_x = None, b_y = None):
        self.top_x = t_x
        self.top_y = t_y
        self.bottom_x = b_x
        self.bottom_y = b_y

    def __str__(self):
        return 'top_x: {}\ntop_y: {}\nbottom_x: {}\nbottom_y: {}'.format(self.top_x, self.top_y, self.bottom_x, self.bottom_y)

class TicTacToe(tk.Tk):

    def __init__(self, board_size = 3, target_len = 3):
        """ Sets window properties """
        logging.debug('init game obj')
        tk.Tk.__init__(self)
        self.title('Tic-Tac-Toe Game')

        # Length of winning sequence
        self.target_len = target_len

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
        self.cells = []

        for vert_index in range(self.board_size): # Vertical index
            for hor_index in range(self.board_size): # Horizontal index
                top_x = margin + hor_index * grid_gap
                top_y = margin + vert_index * grid_gap
                bottom_x = margin + (hor_index + 1) * grid_gap
                bottom_y = margin + (vert_index + 1) * grid_gap

                self.cells.append(CellInfo(top_x, top_y, bottom_x, bottom_y))
                
                cell_tag = str(self.cell_index(hor_index, vert_index) + 1)
                self.canvas.create_rectangle(top_x,
                                                top_y,
                                                bottom_x,
                                                bottom_y,
                                                tags=cell_tag,
                                                fill='grey')
                self.canvas.tag_bind(cell_tag, '<ButtonPress-1>', self.player_turn)


        # Game logic initializing
        self.filled_cells_count = 0
        self.letters = [None for i in range(self.board_size ** 2)]
        self.players_letters = ['X', 'O']
        self.current_letter_index = 0
        self.draw_result = 'Draw!'
        self.directions = ((1, 0), (0, 1), (1, 1), (-1, 1)) # Possible win-sequences directions on board in (x, y) axises

    def player_turn(self, event):
        """ Processes players clicks """
        logging.debug('canvas click x:{} y:{}'.format(event.x, event.y))

        x = event.x
        y = event.y

        board_x, board_y = None, None

        # Looking for cell with right coordinates
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.passed_cell(self.cells[self.cell_index(j, i)], x, y):
                    board_y, board_x = i, j
        logging.debug('cell x: {} y: {} selected'.format(board_x, board_y))

        # Is it possible to put a letter into the cell
        if board_x is not None and board_y is not None and self.letters[self.cell_index(board_x, board_y)] is None:
            self.filled_cells_count += 1
            current_letter = self.players_letters[self.current_letter_index]
            self.letters[self.cell_index(board_x, board_y)] = current_letter
            self.draw_letter(board_x, board_y, current_letter)

            # Looking for winner after turn
            winner = self.check_win_state(board_x, board_y)
            if winner is not None:
                self.show_win_window(winner)

            self.change_current_letter()

    def show_win_window(self, winner):
        """ Shows menu window after game (replay, exit) """
        logging.debug('win screen')
        self.canvas.destroy()

        msg = ''
        if winner is self.draw_result:
            msg = self.draw_result
        else:
            msg = '{} won!\n\nDo you want to replay?'.format(winner)

        self.replay_label = Label(self, text=msg)
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

    def draw_letter(self, board_x, board_y, letter):
        index = self.cell_index(board_x, board_y)
        x = (self.cells[index].top_x + self.cells[index].bottom_x) // 2
        y = (self.cells[index].top_y + self.cells[index].bottom_y) // 2
        font_size = (self.cells[index].bottom_y - self.cells[index].top_y) // 3
        self.canvas.create_text(x, y, font='Times {}'.format(font_size), text=letter)

    def change_current_letter(self):
        self.current_letter_index = abs(self.current_letter_index - 1)
        logging.debug('change letter to index {}'.format(self.current_letter_index))

    def check_win_line(self, cells):
        base_x, base_y = cells[0][0], cells[0][1]
        base_index = self.cell_index(base_x, base_y)

        for cell in cells:
            x, y = cell[0], cell[1]
            index = self.cell_index(x, y)

            if not self.valid_coords(x, y):
                logging.debug('line {} is not win-line: wrong coords'.format(cell))
                return None
            
            if self.letters[index] is None or self.letters[base_index] != self.letters[index]:
                logging.debug('line {} is not win-line: diff letters'.format(cell))
                return None

        logging.debug('line {} won'.format(cells))
        return self.letters[base_index]

    def check_win_state(self, root_x, root_y):
        """ Checking potential win-lines """      
        lines = []

        for direction in self.directions:
            lim_x = root_x - direction[0] * (self.target_len - 1)
            lim_y = root_y - direction[1] * (self.target_len - 1)

            for shift in range(self.target_len):
                corner_x = lim_x + direction[0] * shift
                corner_y = lim_y + direction[1] * shift
                
                line = []
                for step in range(self.target_len):
                    x = corner_x + direction[0] * step
                    y = corner_y + direction[1] * step
                    line.append((x, y))

                lines.append(line)

        for line in lines:
            state = self.check_win_line(line)
            if state is not None:
                logging.debug('win-line {}'.format(line))
                return state

        if self.filled_cells_count == self.target_len ** 2:
            return self.draw_result
        
        return None



    def cell_index(self, x, y): # x & y - coords on game board with cells
        return x + y * self.board_size

    def valid_coords(self, x, y):
        proper_x = 0 <= x < self.board_size
        proper_y = 0 <= y < self.board_size
        return proper_x and proper_y

    def passed_cell(self, cell, x, y):
        proper_x = cell.top_x < x < cell.bottom_x
        proper_y = cell.top_y < y < cell.bottom_y
        return proper_x and proper_y
    


if __name__ == '__main__':
    logging.basicConfig(filename="tic-tac-toe.log", level=logging.DEBUG)

    """
    Win line has always length 3.
    Win-combinations can be placed in 4 directions:
    vertical, horizontal and two diagonals.
    """

    game = TicTacToe()
