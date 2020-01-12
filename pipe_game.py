from board import gameboard
import os
import keyboard

if __name__ == '__main__':
    def init():
        bd = gameboard()
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.display()
        return bd

    def rot():
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.rotate()
        bd.display()

    def select(dir):
        os.system('cls' if os.name == 'nt' else 'clear')
        bd.select(direction=dir)
        bd.display()

    def ex():
        print("EXITING...")
        exit()

    bd=init()
    keyboard.add_hotkey('space', rot)
    keyboard.add_hotkey('right', select, args='r')
    keyboard.add_hotkey('left', select, args='l')
    keyboard.add_hotkey('up', select, args='u')
    keyboard.add_hotkey('down', select, args='d')
    keyboard.wait('esc')
    os.system('cls' if os.name == 'nt' else 'clear')

