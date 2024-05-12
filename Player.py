import keyboard
from colorama import Fore, Style, Back, init
import os

import config

init()

class Player():
    def __init__(self, field, height, width, exit_x, exit_y, net, buttons):
        self.cur_x_coord = 0
        self.cur_y_coord = 0
        self.for_print_player = field
        self.height = height
        self.width = width
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.cnt_mistakes = 0
        self.enemy_mistakes = 0
        self.net = net
        self.buttons = buttons
        self.win = False
        self.start_time = 0
        self.end_time = 0

    def get_coordinate(self, coord):
        return coord * 2 + 1

    def send_mistake(self):
        data = "mistake:" + str(self.net.id) + ":" + str(self.cnt_mistakes)
        reply = self.net.send(data)
        return reply

    def parse_mistake(self, data):
        try:
            d = data.split(":")[2]
            return int(d)
        except:
            return 0

    def send_finish(self, value):
        data = "finish:" + str(self.net.id) + ":" + str(value)
        reply = self.net.send(data)
        return reply

    def parse_finish(self, data):
        try:
            d = data.split(":")[2]
            return int(d)
        except:
            return 0

    def update_position(self, prev_x, prev_y):
        self.for_print_player[prev_y][prev_x] = "   "
        self.for_print_player[self.get_coordinate(self.cur_y_coord)][self.get_coordinate(self.cur_x_coord)] =\
            (Fore.BLACK + Back.WHITE + "-_-" + Style.RESET_ALL)

    def up(self):
        if (self.for_print_player[self.get_coordinate(self.cur_y_coord) - 1][self.get_coordinate(self.cur_x_coord)] ==
                " H "):
            self.cnt_mistakes += 1
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
            self.cnt_mistakes += 1
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
            self.cnt_mistakes += 1
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
            self.cnt_mistakes += 1
            print(Fore.RED + "You can't go left! Please, choose another direction." + Style.RESET_ALL)
        else:
            self.cur_x_coord -= 1
            self.update_position(self.get_coordinate(self.cur_x_coord + 1), self.get_coordinate(self.cur_y_coord))
            self.clear_field()
            self.print_for_player()
            self.exit()

    def print_for_player(self):
        self.enemy_mistakes = self.parse_mistake(self.send_mistake())
        print("Number of your mistakes: ", self.cnt_mistakes)
        print("Number of enemy mistakes: ", self.enemy_mistakes)
        for i in range(self.get_coordinate(self.height)):
            for j in range(self.get_coordinate(self.width)):
                print(Style.BRIGHT + self.for_print_player[i][j] + Style.RESET_ALL, end='')
            print()

    def clear_field(self):
        print("\033[H\033[J")
        # os.system('cls' if os.name == 'nt' else 'clear')

    def exit(self):
        x_coord, y_coord = self.exit_x, self.exit_y
        if x_coord == -1:
            x_coord = self.width - 1
            y_coord = (y_coord - 1) // 2
        else:
            y_coord = self.height - 1
            x_coord = (x_coord - 1) // 2
        if self.cur_x_coord == x_coord and self.cur_y_coord == y_coord:
            keyboard.clear_hotkey(self.buttons[0])
            keyboard.clear_hotkey(self.buttons[1])
            keyboard.clear_hotkey(self.buttons[3])
            keyboard.clear_hotkey(self.buttons[2])
            if self.parse_finish(self.send_finish("1")) == 0:
                self.win = True
                print(Fore.GREEN + "YOU WIN! CONGRATULATIONS!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "YOU LOSE! MY REGRETS :(" + Style.RESET_ALL)
            print(Style.BRIGHT + "If you want to exit, please, press Ctrl + Q" + Style.RESET_ALL)

    def play(self):
        self.update_position(1, 1)
        self.print_for_player()
        keyboard.add_hotkey(self.buttons[0], self.up)
        keyboard.add_hotkey(self.buttons[1], self.down)
        keyboard.add_hotkey(self.buttons[2], self.right)
        keyboard.add_hotkey(self.buttons[3], self.left)
        keyboard.wait("Ctrl + Q")

