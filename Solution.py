import config
from Labirint import Labirint
from colorama import Fore, Style

class Solution(Labirint):
    def __init__(self, for_print, height, width):
        super().__init__(height, width, for_print)
        self.for_print = for_print
        self.solution = []
        self.parents = {}
        self.for_print_solution = [['   ' for i in range(len(for_print[0]))] for j in range(len(for_print))]

    def make_way_dfs(self, used, x_coord, y_coord):
        used[y_coord][x_coord] = 1
        for direction in self.useful_list:
            if not self.labirint[y_coord][x_coord][direction]:
                if direction == config.UP and y_coord > 0 and used[y_coord - 1][x_coord] == 0:
                    self.parents[(x_coord, y_coord - 1)] = [x_coord, y_coord]
                    self.make_way_dfs(used, x_coord, y_coord - 1)
                elif direction == config.DOWN and y_coord < self.height - 1 and used[y_coord + 1][x_coord] == 0:
                    self.parents[(x_coord, y_coord + 1)] = [x_coord, y_coord]
                    self.make_way_dfs(used, x_coord, y_coord + 1)
                elif direction == config.RIGHT and x_coord < self.width - 1 and used[y_coord][x_coord + 1] == 0:
                    self.parents[(x_coord + 1, y_coord)] = [x_coord, y_coord]
                    self.make_way_dfs(used, x_coord + 1, y_coord)
                elif direction == config.LEFT and x_coord > 0 and used[y_coord][x_coord - 1] == 0:
                    self.parents[(x_coord - 1, y_coord)] = [x_coord, y_coord]
                    self.make_way_dfs(used, x_coord - 1, y_coord)

    def make_solution(self):
        x_coord, y_coord = self.exit_coords[0], self.exit_coords[1]
        if x_coord == -1:
            x_coord = self.width - 1
            y_coord = (y_coord - 1) // 2
        else:
            y_coord = self.height - 1
            x_coord = (x_coord - 1) // 2
        self.solution.append([x_coord, y_coord])
        while not (x_coord == 0 and y_coord == 0):
            x_coord, y_coord = self.parents[(x_coord, y_coord)][0], self.parents[(x_coord, y_coord)][1]
            self.solution.append([x_coord, y_coord])

    def get_solution(self):
        for i in range(len(self.for_print)):
            for j in range(len(self.for_print_solution[0])):
                self.for_print_solution[i][j] = self.for_print[i][j]
        for coords in self.solution:
            self.for_print_solution[self.get_coordinate(coords[1])][self.get_coordinate(coords[0])] =\
                (Fore.BLUE + " ■ " + Style.RESET_ALL)
        for i in range(1, len(self.for_print_solution) - 1):
            for j in range(1, len(self.for_print_solution[0]) - 1):
                if (self.for_print_solution[i][j - 1] == Fore.BLUE + " ■ " + Style.RESET_ALL and
                        self.for_print_solution[i][j + 1] == Fore.BLUE + " ■ " + Style.RESET_ALL and
                        self.for_print_solution[i][j] != ' H '):
                    self.for_print_solution[i][j] = Fore.BLUE + " ■ " + Style.RESET_ALL
                if (self.for_print_solution[i - 1][j] == Fore.BLUE + " ■ " + Style.RESET_ALL and
                        self.for_print_solution[i + 1][j] == Fore.BLUE + " ■ " + Style.RESET_ALL and
                        self.for_print_solution[i][j] != ' H '):
                    self.for_print_solution[i][j] = Fore.BLUE + " ■ " + Style.RESET_ALL
    def print_solution(self):
        if self.for_print == [[" H " for i in range(self.get_coordinate(self.width))] for j in range(self.get_coordinate(self.height))]:
            self.build_labirint()
        self.get_solution()
        for i in range(self.get_coordinate(self.height)):
            for j in range(self.get_coordinate(self.width)):
                print(Style.BRIGHT + self.for_print_solution[i][j] + Style.RESET_ALL, end='')
            print()

