import random
import time
import json
import os
strfrmt="piece_orientation_flowdirs_color"
example="pipe_up_ud_y"

with open(os.path.dirname(os.path.realpath(__file__))+'./pieces.json', 'r') as f:
    pieces = json.load(f)


class pcolors:
    HEADER = '\033/[95m'
    OKBLUE = '\x1b/[94m'
    OKGREEN = '\x1b/[92m'
    WARNING = '\x1b/[93m'
    FAIL = '\033/[91m'
    ENDC = '\x1b/[0m'
    BOLD = '\033/[1m'
    UNDERLINE = '\033/[4m'


class GameBoard:

    def __init__(self, board_width=9, board_height=7, seed=None):
        if seed is None:
            self.seed = random.getrandbits(32)
        else:
            self.seed = seed
        random.seed(self.seed)

        self.board_width = board_width
        self.board_height = board_height
        self.board = self.generate_board(board_width=self.board_width, board_height=self.board_height, seed=self.seed)
        self.entry = [0, 0]
        self.exit = [self.board_height, self.board_width]
        self.selected = [0, 0]
        self.flows = [self.entry]
        self.representation = None
        self._generate_representation()
        self.clock=time.time()

    def start_flow(self):
        self._fill_piece(self.entry)
        self._generate_representation()
    def increment_flow(self):
        current_flows = self.flows
        if len(self.flows) == 0:
            print("YOU LOSE")
            input()
            exit()
        found = self._look(current_flows)
        if found:
            self.flows = []
            [self.flows.append(piece) for piece in found if piece not in self.flows]
            [self._fill_piece(to_fill) for to_fill in self.flows]
        else:
            print("YOU LOSE")
            input()
            exit()
        self._generate_representation()

    def _look(self, flow_list):
        results = []
        for coords in flow_list:
            piece_name = self.board[coords[0]][coords[1]].split('_')
            flow_dirs = piece_name[2]

            for dir in flow_dirs:
                found = self._look_in_dir(coords, dir)
                if found:
                    results.append(found)

        if results:
            return results
        else:
            return None

    def _look_in_dir(self, coords, dir):
        if dir == 'u':
            if coords[0]-1 < 0:
                return None
            word = self.board[coords[0]-1][coords[1]].split('_')
            if 'd' in word[2] and 'g' != word[-1]:
                return [coords[0]-1, coords[1]]
            else:
                return None
        if dir == 'd':
            if coords[0]+1 >= self.board_height:
                return None
            word = self.board[coords[0]+1][coords[1]].split('_')
            if 'u' in word[2] and 'g' != word[-1]:
                return [coords[0]+1, coords[1]]
            else:
                return None
        if dir == 'l':
            if coords[1]-1 < 0:
                return None
            word = self.board[coords[0]][coords[1]-1].split('_')
            if 'r' in word[2] and 'g' != word[-1]:
                return [coords[0], coords[1]-1]
            else:
                return None
        if dir == 'r':
            if coords[1]+1 >= self.board_width:
                return None
            word = self.board[coords[0]][coords[1] + 1].split('_')
            if 'l' in word[2] and 'g' != word[-1]:
                return [coords[0], coords[1]+1]
            else:
                return None

        return None

    def _fill_piece(self, coords):
        self.board[coords[0]][coords[1]] = self.board[coords[0]][coords[1]][0:-1] + 'g'

    def _recolor(self, coords, color):
        # piece = self.representation[coords[0]][coords[1]]
        piece_name = self.board[coords[0]][coords[1]].split('_')
        piece = pieces[piece_name[0]][piece_name[1]]["array"]
        color_rep = {"p": pcolors.HEADER, "y": pcolors.WARNING, "g": pcolors.OKGREEN, "b": pcolors.OKBLUE}[color]
        self.representation[coords[0]][coords[1]] = self.color_piece(piece, color_rep)

    def _generate_representation(self):
        self.representation = [[pieces[item.split('_')[0]][item.split('_')[1]]["array"]
                                for item in row]
                               for row in self.board]
        for i in range(self.board_width):
            for j in range(self.board_height):
                color = self.board[j][i].split('_')[3]
                self._recolor([j, i], color)
        self._recolor(self.selected, "b")

    def display(self):
        for idx, row in enumerate(self.representation):

            if idx == self.entry[0]:
                st = True
            else:
                st = False
            if idx == self.exit[0]-1:
                en = True
            else:
                en = False

            print("   \u001b[38;5;234m+\x1b[0m", end='')
            [print("\u001b[38;5;234m=======+\x1b[0m", end='') for _ in range(self.board_width)]
            print()
            for i in range(3):
                if st:
                    print("\x1b[32m>>>", end='')
                else:
                    print('   ', end='')
                top = ['\u001b/[38;5;234m|\x1b/[0m']
                for line in range(self.board_width):
                    top.append(row[line][i])
                    top.append('\u001b/[38;5;234m|\x1b/[0m')
                    # if line%3==0:
                    #     top.append(' . ')
                # top = [row[line][i] for line in range(width)]
                if en:
                    top.append('\x1b/[32m>>>')
                out = self.replacer(str(top))
                # out= ' | '.join(a + b for a, b in zip(out[::3], out[1::3]))
                print(out)
        print("   \u001b[38;5;234m+\x1b[0m", end='')
        [print("\u001b[38;5;234m=======+\x1b[0m", end='') for _ in range(self.board_width)]
        print()
        hashes = int((time.time() - self.clock)%60)
        bar = "[" + "#" * hashes + " " * (30 - hashes) + "]"
        print("\x1b[32mGAME OF PIPE ", end='')
        print(bar, end='\x1b[0m\n')
        print(self.flows)

    def rotate(self):
        piece = self.board[self.selected[0]][self.selected[1]]
        if piece.split('_')[-1] != 'g':
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
    def generate_board(board_width=4, board_height=4, seed=random.getrandbits(32)):
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

    @staticmethod
    def _piece_from_name(name):
        parsed = name.split('_')
        return pieces[parsed[0]][parsed[1]]



