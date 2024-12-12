import keyboard
from colorama import Fore, Style, Back, init
import os

import config

init()

class Player():
    def __init__(self, field, height, width, exit_x, exit_y):
        self.cur_x_coord = 0
        self.cur_y_coord = 0
        self.for_print_player = field
        self.height = height
        self.width = width
        self.exit_x = exit_x
        self.exit_y = exit_y

    def get_coordinate(self, coord):
        return coord * 2 + 1

    def update_position(self, prev_x, prev_y):
        self.for_print_player[prev_y][prev_x] = "   "
        self.for_print_player[self.get_coordinate(self.cur_y_coord)][self.get_coordinate(self.cur_x_coord)] =\
            (Fore.BLACK + Back.WHITE + "-_-" + Style.RESET_ALL)

    def up(self):
        if (self.for_print_player[self.get_coordinate(self.cur_y_coord) - 1][self.get_coordinate(self.cur_x_coord)] ==
                " H "):
            print(Fore.RED + "You can't go up! Please, choose another direction." + Style.RESET_ALL)
        else:
            self.cur_y_coord -= 1
            self.update_position(self.get_coordinate(self.cur_x_coord), self.get_coordinate((self.cur_y_coord + 1)))
            self.clear_field()
            self.print_for_player()
            self.exit()

    def down(self):
        if (self.for_print_player[self.get_coordinate(self.cur_y_coord) + 1][self.get_coordinate(self.cur_x_coord)] ==
                " H "):
            print(Fore.RED + "You can't go down! Please, choose another direction." + Style.RESET_ALL)

        else:
            self.cur_y_coord += 1
            self.update_position(self.get_coordinate(self.cur_x_coord), self.get_coordinate((self.cur_y_coord - 1)))
            self.clear_field()
            self.print_for_player()
            self.exit()

    def right(self):
        if (self.for_print_player[self.get_coordinate(self.cur_y_coord)][self.get_coordinate(self.cur_x_coord) + 1] ==
                " H "):
            print(Fore.RED + "You can't go right! Please, choose another direction." + Style.RESET_ALL)
        else:
            self.cur_x_coord += 1
            self.update_position(self.get_coordinate(self.cur_x_coord - 1), self.get_coordinate(self.cur_y_coord))
            self.clear_field()
            self.print_for_player()
            self.exit()

    def left(self):
        if (self.for_print_player[self.get_coordinate(self.cur_y_coord)][self.get_coordinate(self.cur_x_coord) - 1] ==
                " H "):
            print(Fore.RED + "You can't go left! Please, choose another direction." + Style.RESET_ALL)
        else:
            self.cur_x_coord -= 1
            self.update_position(self.get_coordinate(self.cur_x_coord + 1), self.get_coordinate(self.cur_y_coord))
            self.clear_field()
            self.print_for_player()
            self.exit()

    def print_for_player(self):
        for i in range(self.get_coordinate(self.height)):
            for j in range(self.get_coordinate(self.width)):
                print(Style.BRIGHT + self.for_print_player[i][j] + Style.RESET_ALL, end='')
            print()

    def clear_field(self):
        print("\033[H\033[J")
        #os.system('cls' if os.name == 'nt' else 'clear')

    def exit(self):
        x_coord, y_coord = self.exit_x, self.exit_y
        if x_coord == -1:
            x_coord = self.width - 1
            y_coord = (y_coord - 1) // 2
        else:
            y_coord = self.height - 1
            x_coord = (x_coord - 1) // 2
        if self.cur_x_coord == x_coord and self.cur_y_coord == y_coord:
            keyboard.clear_hotkey(config.UP)
            keyboard.clear_hotkey(config.DOWN)
            keyboard.clear_hotkey(config.LEFT)
            keyboard.clear_hotkey(config.RIGHT)
            print(Fore.GREEN + "YOU WIN! CONGRATULATIONS!" + Style.RESET_ALL)
            print(Style.BRIGHT + "If you want to exit, please, press Ctrl + Q" + Style.RESET_ALL)

    def play_for_draw(self):
        self.update_position(0, 1)
        keyboard.add_hotkey(config.UP, self.up)
        keyboard.add_hotkey(config.DOWN, self.down)
        keyboard.add_hotkey(config.RIGHT, self.right)
        keyboard.add_hotkey(config.LEFT, self.left)
        keyboard.wait("Ctrl + Q")
    def play(self):
        self.update_position(1, 1)
        self.print_for_player()
        keyboard.add_hotkey(config.UP, self.up)
        keyboard.add_hotkey(config.DOWN, self.down)
        keyboard.add_hotkey(config.RIGHT, self.right)
        keyboard.add_hotkey(config.LEFT, self.left)
        keyboard.wait("Ctrl + Q")

