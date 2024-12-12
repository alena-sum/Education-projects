from random import shuffle, randint, choice
from colorama import Fore, Style
import sys

import config

sys.setrecursionlimit(100000000)

class Labirint():
    def __init__(self, height, width, for_print):
        self.labirint = [[{config.UP: True, config.DOWN: True, config.LEFT: True, config.RIGHT: True}
                      for i in range(width)] for j in range(height)]
        self.height = height
        self.width = width
        self.useful_list = [config.UP, config.DOWN, config.LEFT, config.RIGHT]
        self.for_print = for_print
        self.exit_coords = []
        if for_print == [[" H " for i in range(self.get_coordinate(width))] for j in range(self.get_coordinate(height))]:
            choice = ["x", "y"][randint(0, 1)]
            x_coord, y_coord = -1, -1
            if choice == "x":
                x_coord = self.get_coordinate(randint(0, width - 1))
            else:
                y_coord = self.get_coordinate(randint(0, height - 1))
            self.exit_coords = [x_coord, y_coord]
        else:
            for i in range(self.get_coordinate(height)):
                for j in range(self.get_coordinate(width)):
                    if for_print[i][j] == Fore.RED + " E " + Style.RESET_ALL:
                        if j == self.get_coordinate(width) - 1:
                            self.exit_coords = [-1, i]
                        elif i == self.get_coordinate(height) - 1:
                            self.exit_coords = [j, -1]
    def get_coordinate(self, coord):
        return coord * 2 + 1

    def make_with_mst(self):
        x_coord, y_coord = randint(0, self.width - 1), randint(0, self.height - 1)
        used = [[0 for i in range(self.width)] for j in range(self.height)]
        neighbours = []
        for i in range(self.height * self.width - 1):
            used[y_coord][x_coord] = 1
            for direction in self.labirint[y_coord][x_coord]:
                if direction == config.UP and y_coord > 0 and used[y_coord - 1][x_coord] == 0:
                    neighbours.append([x_coord, y_coord - 1, config.DOWN])
                if direction == config.DOWN and y_coord < self.height - 1 and used[y_coord + 1][x_coord] == 0:
                    neighbours.append([x_coord, y_coord + 1, config.UP])
                if direction == config.RIGHT and x_coord < self.width - 1 and used[y_coord][x_coord + 1] == 0:
                    neighbours.append([x_coord + 1, y_coord, config.LEFT])
                if direction == config.LEFT and x_coord > 0 and used[y_coord][x_coord - 1] == 0:
                    neighbours.append([x_coord - 1, y_coord, config.RIGHT])
            x_coord, y_coord, direct = choice(neighbours)
            for_pop = []
            for j in range(len(neighbours)):
                if neighbours[j][0] == x_coord and neighbours[j][1] == y_coord:
                    for_pop += [j]
            while len(for_pop) != 0:
                neighbours.pop(for_pop[-1])
                for_pop.pop()

            self.labirint[y_coord][x_coord][direct] = False
            if direct == config.UP:
                self.labirint[y_coord - 1][x_coord][config.DOWN] = False
            if direct == config.DOWN:
                self.labirint[y_coord + 1][x_coord][config.UP] = False
            if direct == config.LEFT:
                self.labirint[y_coord][x_coord - 1][config.RIGHT] = False
            if direct == config.RIGHT:
                self.labirint[y_coord][x_coord + 1][config.LEFT] = False

    def make_with_dfs(self, used, x_coord, y_coord):
        used[y_coord][x_coord] = 1
        shuffle(self.useful_list)
        for direction in self.useful_list:
            if direction == config.UP and y_coord > 0 and used[y_coord - 1][x_coord] == 0:
                self.labirint[y_coord][x_coord][direction] = False
                self.labirint[y_coord - 1][x_coord][config.DOWN] = False
                self.make_with_dfs(used, x_coord, y_coord - 1)
            if direction == config.DOWN and y_coord < self.height - 1 and used[y_coord + 1][x_coord] == 0:
                self.labirint[y_coord][x_coord][direction] = False
                self.labirint[y_coord + 1][x_coord][config.UP] = False
                self.make_with_dfs(used, x_coord, y_coord + 1)
            if direction == config.RIGHT and x_coord < self.width - 1 and used[y_coord][x_coord + 1] == 0:
                self.labirint[y_coord][x_coord][direction] = False
                self.labirint[y_coord][x_coord + 1][config.LEFT] = False
                self.make_with_dfs(used, x_coord + 1, y_coord)
            if direction == config.LEFT and x_coord > 0 and used[y_coord][x_coord - 1] == 0:
                self.labirint[y_coord][x_coord][direction] = False
                self.labirint[y_coord][x_coord - 1][config.RIGHT] = False
                self.make_with_dfs(used, x_coord - 1, y_coord)

    def build_labirint(self):
        for i in range(self.height):
            for j in range(self.width):
                x_in_for_print = self.get_coordinate(j)
                y_in_for_print = self.get_coordinate(i)
                self.for_print[y_in_for_print][x_in_for_print] = "   "
                if not self.labirint[i][j][config.UP] and self.for_print[y_in_for_print - 1][x_in_for_print] == " H ":
                    self.for_print[y_in_for_print - 1][x_in_for_print] = "   "
                if not self.labirint[i][j][config.DOWN] and self.for_print[y_in_for_print + 1][x_in_for_print] == " H ":
                    self.for_print[y_in_for_print + 1][x_in_for_print] = "   "
                if not self.labirint[i][j][config.RIGHT] and self.for_print[y_in_for_print][x_in_for_print + 1] == " H ":
                    self.for_print[y_in_for_print][x_in_for_print + 1] = "   "
                if not self.labirint[i][j][config.LEFT] and self.for_print[y_in_for_print][x_in_for_print - 1] == " H ":
                    self.for_print[y_in_for_print][x_in_for_print - 1] = "   "
        self.for_print[self.exit_coords[1]][self.exit_coords[0]] = Fore.RED + " E " + Style.RESET_ALL
        self.for_print[1][0] = Fore.GREEN + " S " + Style.RESET_ALL

    def print_labirint(self):
        self.build_labirint()
        for i in range(self.get_coordinate(self.height)):
            for j in range(self.get_coordinate(self.width)):
                print(Style.BRIGHT + self.for_print[i][j] + Style.RESET_ALL, end='')
            print()
    def make_labirint_from_file(self):
        for i in range(self.height):
            for j in range(self.width):
                if j != 0 and self.for_print[self.get_coordinate(i)][self.get_coordinate(j) - 1] == '   ':
                    self.labirint[i][j][config.LEFT] = False
                if j != self.width - 1 and self.for_print[self.get_coordinate(i)][self.get_coordinate(j) + 1] == '   ':
                    self.labirint[i][j][config.RIGHT] = False
                if i != 0 and self.for_print[self.get_coordinate(i) - 1][self.get_coordinate(j)] == '   ':
                    self.labirint[i][j][config.UP] = False
                if i != self.height - 1 and self.for_print[self.get_coordinate(i) + 1][self.get_coordinate(j)] == '   ':
                    self.labirint[i][j][config.DOWN] = False






