# import numpy as np
# from pprint import pprint
import random
# import pandas as pd
# from itertools import cycle


# seed=1000
strfrmt="piece_orientation_flowdirs_color"
example="pipe_up_ud_yellow"

class pcolors:
    HEADER = '\033/[95m'
    OKBLUE = '\x1b/[94m'
    OKGREEN = '\x1b/[92m'
    WARNING = '\x1b/[93m'
    FAIL = '\033/[91m'
    ENDC = '\x1b/[0m'
    BOLD = '\033/[1m'
    UNDERLINE = '\033/[4m'

pieces = {"pipe": {"up": {"array": [['|', ' ', '|'],
                                    ['|', ' ', '|'],
                                    ['|', ' ', '|']],
                          "dirs": "ud"},
                   "rt": {"array": [['-', '-', '-'],
                                    [' ', ' ', ' '],
                                    ['-', '-', '-']],
                          "dirs": "lr"},
                   "dn": {"array": [['|', ' ', '|'],
                                    ['|', ' ', '|'],
                                    ['|', ' ', '|']],
                          "dirs": "ud"},
                   "lf": {"array": [['-', '-', '-'],
                                    [' ', ' ', ' '],
                                    ['-', '-', '-']],
                          "dirs": "lr"}},
          "turn": {"up": {"array": [['|', ' ', '\u2514'],
                                    ['|', ' ', ' '],
                                    ['\u2514', '-', '-']],
                          "dirs": "ur"},
                   "rt": {"array": [['\u250c', '-', '-'],
                                    ['|', ' ', ' '],
                                    ['|', ' ', '\u250c']],
                          "dirs": "rd"},
                   "dn": {"array": [['-', '-', '\u2510'],
                                    [' ', ' ', '|'],
                                    ['\u2510', ' ', '|']],
                          "dirs": "dl"},
                   "lf": {"array": [['\u2518', ' ', '|'],
                                    [' ', ' ', '|'],
                                    ['-', '-', '\u2518']],
                          "dirs": "lu"}},
          "junc": {"up": {"array": [['\u2518', ' ', '\u2514'],
                                    [' ', ' ', ' '],
                                    ['-', '-', '-']],
                          "dirs": "lur"},
                   "rt": {"array": [['|', ' ', '\u2514'],
                                    ['|', ' ', ' '],
                                    ['|', ' ', '\u250c']],
                          "dirs": "urd"},
                   "dn": {"array": [['-', '-', '-'],
                                    [' ', ' ', ' '],
                                    ['\u2510', ' ', '\u250c']],
                          "dirs": "rdl"},
                   "lf": {"array": [['\u2518', ' ', '|'],
                                    [' ', ' ', '|'],
                                    ['\u2510', ' ', '|']],
                          "dirs": "dlu"}}}
import time
class gameboard:

    def __init__(self, board_width=9, board_height=7, seed=random.getrandbits(32)):
        self.board_width = board_width
        self.board_height = board_height
        self.board = self.generate_board(board_width=self.board_width, board_height=self.board_height, seed=seed)
        self.selected = [0, 0]
        self.representation = None
        self._generate_representation()
        self.clock=time.time()

    def _recolor(self, coords, color):
        # piece = self.representation[coords[0]][coords[1]]
        piece_name = self.board[coords[0]][coords[1]].split('_')
        piece = pieces[piece_name[0]][piece_name[1]]["array"]
        color_rep = {"p": pcolors.HEADER, "y": pcolors.WARNING, "g": pcolors.OKGREEN, "b": pcolors.OKBLUE}[color]
        self.representation[coords[0]][coords[1]] = self.color_piece(piece, color_rep)

    def _generate_representation(self):
        if self.representation is None:
            self.representation = [[pieces[item.split('_')[0]][item.split('_')[1]]["array"] for item in row] for row in self.board]
            for i in range(self.board_width):
                for j in range(self.board_height):
                    color = self.board[j][i].split('_')[3]
                    self._recolor([j, i], color)
        else:
            self.representation = [[pieces[item.split('_')[0]][item.split('_')[1]]["array"] for item in row] for row in self.board]
            for i in range(self.board_width):
                for j in range(self.board_height):
                    color = self.board[j][i].split('_')[3]
                    self._recolor([j, i], color)
        self._recolor(self.selected, "b")

    def display(self):
        for row in self.representation:
            width = len(row)
            print("\u001b[38;5;234m+\x1b[0m", end='')
            [print("\u001b[38;5;234m=======+\x1b[0m", end='') for _ in range(width)]
            print()
            for i in range(3):
                top = ['\u001b/[38;5;234m|\x1b/[0m']
                for line in range(width):
                    top.append(row[line][i])
                    top.append('\u001b/[38;5;234m|\x1b/[0m')
                    # if line%3==0:
                    #     top.append(' . ')
                # top = [row[line][i] for line in range(width)]
                out = self.replacer(str(top))
                # out= ' | '.join(a + b for a, b in zip(out[::3], out[1::3]))
                print(out)
        print("\u001b[38;5;234m+\x1b[0m", end='')
        [print("\u001b[38;5;234m=======+\x1b[0m", end='') for _ in range(width)]
        print()
        hashes = int((time.time() - self.clock)%60)
        bar = "[" + "#" * hashes + " " * (30 - hashes) + "]"
        print("\x1b[32mGAME OF PIPE ", end='')
        print(bar, end='\x1b[0m\n')



    def rotate(self):
        piece = self.board[self.selected[0]][self.selected[1]]
        self.board[self.selected[0]][self.selected[1]] = self._rotate_piece(piece)
        self._generate_representation()

    def select(self, direction):
        if direction == 'u' and self.selected[0] > 0:
            self.selected[0] -= 1
        elif direction == 'd' and self.selected[0] < self.board_height-1:
            self.selected[0] += 1
        elif direction == 'l' and self.selected[1] > 0:
            self.selected[1] -= 1
        elif direction == 'r' and self.selected[1] < self.board_width-1:
            self.selected[1] += 1
        self._generate_representation()

    @staticmethod
    def color_piece(piece_array, color):
        return [["{}{}{}".format(color, val, pcolors.ENDC) for val in row] for row in piece_array]

    @staticmethod
    def _rotate_piece(piece_name):
        word = piece_name.split('_')
        word[1] = {"up": "rt", "rt": "dn", "dn": "lf", "lf": "up"}[word[1]]
        word[2] = pieces[word[0]][word[1]]['dirs']
        return '_'.join(word)

    @staticmethod
    def generate_board(board_width, board_height, seed=random.getrandbits(32)):
        random.seed(seed)
        gen_pieces = [["{}_{}".format(list(pieces)[random.randint(0, 2)],
                                      list(pieces[list(pieces)[0]])[random.randint(0, 3)])
                       for i in range(board_width)]
                      for j in range(board_height)]
        piece_names = [[val+'_'+pieces[val.split('_')[0]][val.split('_')[1]]["dirs"]+'_p' for val in row] for row in gen_pieces]
        return piece_names

    @staticmethod
    def replacer(input_string, chars_to_erase=None):
        if chars_to_erase is None:
            chars_to_erase = ["[", "]", ",", "'"]
        prev_char=''
        newstr=''
        for i in range(len(input_string)):
            if input_string[i] not in chars_to_erase:
                newstr+=input_string[i]
            elif prev_char=="/":
                newstr += input_string[i]
            prev_char=input_string[i]
        # newstr=newstr.replace('/','')
        # newstr2=newstr.encode('ascii', 'backslashreplace').decode('unicode_escape')
        return newstr.replace('/','').encode('ascii', 'backslashreplace').decode('unicode_escape')
    @staticmethod
    def print_meta_board(cur_board):
        print("+", end='')
        for _ in range(cur_board.board_width):
            print("================+", end='')
        print()
        for row in cur_board:
            print("| ", end='')
            for item in row:
                print("{:<14}".format(item)+" | ", end='')
            print()
            print("+", end='')
            for _ in range(cur_board.board_width):
                print("----------------+", end='')
            print()

# def piece_from_name(name):
#     parsed = name.split('_')
#     return pieces[parsed[0]][parsed[1]]
#
#
# print(piece_from_name(example))

