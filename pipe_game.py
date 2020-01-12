from board import GameBoard
import os
import keyboard
import argparse
import time
import threading

if __name__ == '__main__':
    def init(seed=None):
        global bd
        bd = GameBoard(seed=seed)
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.display()

    def rot():
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.rotate()
        bd.display()

    def select(dir):
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.select(direction=dir)
        bd.display()

    def inc():
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.increment_flow()
        bd.display()
        threading.Timer(2.0, inc).start()

    def start():
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.start_flow()
        bd.display()
        threading.Timer(2.0, inc).start()

    def ex():
        print("EXITING...")
        exit()


    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", "-s", help="set random seed value")
    args = parser.parse_args()
    if args.seed:
        print("set seed to %s" % args.seed)
        init(seed=args.seed)
    else:
        init()

    # start = time.time()
    # elapsed=time.time()-start
    keyboard.add_hotkey('space', rot)
    keyboard.add_hotkey('right', select, args='r')
    keyboard.add_hotkey('left', select, args='l')
    keyboard.add_hotkey('up', select, args='u')
    keyboard.add_hotkey('down', select, args='d')
    keyboard.add_hotkey('x', inc)
    keyboard.add_hotkey('s', start)
    keyboard.add_hotkey('r', init)
    threading.Timer(5.0, start).start()
    keyboard.wait('esc')
    os.system('cls' if os.name == 'nt' else 'clear')

