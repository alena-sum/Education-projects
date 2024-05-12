from colorama import Fore, Style
from Solution import Solution
from Player import Player
from Network import Network
import MakeScreen
import pygame
import json
import time

class Game:
    def __init__(self, args, buttons):
        self.args = args
        self.net = Network()
        self.buttons = buttons
        self.name = ""

    def send_maze(self, maze):
        data = "choose maze:" + str(self.net.id) + ":" + str(maze)
        reply = self.net.send(data)
        return reply

    def parse_maze(self, data):
        try:
            d = data.split(":")[2]
            return eval(d)
        except:
            return 0

    def send_start(self, value):
        data = "start:" + str(self.net.id) + ":" + str(value)
        reply = self.net.send(data)
        return reply

    def parse_start(self, data):
        try:
            d = data.split(":")[2]
            return int(d)
        except:
            return 0

    def send_name(self, name):
        data = "name:" + str(self.net.id) + ":" + str(name)
        reply = self.net.send(data)
        return reply

    def parse_name(self, data):
        try:
            d = data.split(":")[2]
            return str(d)
        except:
            return ""
    def send_time(self, player):
        data = "time:" + str(self.net.id) + ":" + str(round(player.end_time - player.start_time, 2))
        reply = self.net.send(data)
        return reply

    def parse_time(self, data):
        try:
            d = data.split(":")[2]
            return str(d)
        except:
            return ""
    def after_play(self, labirint, width, height, type):
        print(Fore.BLUE + Style.BRIGHT + "What do you want to do next?" + Style.RESET_ALL)
        print(Fore.BLUE + "<1>" + Style.RESET_ALL + "See the solution.")
        print(Fore.BLUE + "<2>" + Style.RESET_ALL + "Upload to file.")
        print(Fore.BLUE + "<3>" + Style.RESET_ALL + "Exit.")
        print("Your choice: ", end="")
        choice = int(input())
        if choice == 1:
            use = [[0 for i in range(width)] for j in range(height)]
            labirint.make_way_dfs(use, 0, 0)
            labirint.make_solution()
            labirint.print_solution()
            print(Fore.BLUE + Style.BRIGHT + "Do you want to return?" + Style.RESET_ALL + "\nAnswer, 'yes' or 'no': ")
            answer = str(input())
            if answer == "yes":
                self.after_play(labirint, width, height, type)
            else:
                exit()
        elif choice == 2:
            data = {'maze': labirint.for_print}
            with open("file.json", "w") as f:
                json.dump(data, f)
            self.after_play(labirint, width, height, type)
        elif choice == 3:
            exit()

    def about_solution(self, labirint, width, height, type):
        print("Please, write down 'start' to start the game: ")
        start = str(input())
        if start == "start":
            cnt = 0
            while True:
                if cnt == 0:
                    print("We are waiting to another player...")
                cnt += 1
                if self.parse_start(self.send_start("1")) == 1:
                    break
            labirint.build_labirint()
            player = Player(labirint.for_print, height, width, labirint.exit_coords[0], labirint.exit_coords[1],
                            self.net, self.buttons)
            player.start_time = time.time()
            player.play()
            player.end_time = time.time()
            self.send_time(player)
            cnt = 0
            while True:
                cnt += 1
                if player.parse_finish(player.send_finish("1")) == 1:
                    break
                if cnt == 1:
                    print("We are waiting when another player finish...")
            print(Fore.BLUE + Style.BRIGHT + "Do you want to see results?" + Style.RESET_ALL + "\nAnswer, 'yes' or 'no': ")
            answer = str(input())
            if answer[-3:] == "yes":
                print(Fore.GREEN + Style.BRIGHT + "RESULTS" + Style.RESET_ALL)
                print(Fore.GREEN + "                      " + self.name + "             " + self.parse_name(self.send_name(self.name)))
                total1, total2 = ("WIN" if player.win else "LOSE"), ("WIN" if not player.win else "LOSE")
                print("Total                  " + Style.RESET_ALL + total1 + "               " + total2)
                print(Fore.GREEN + "Count of mistakes        " + Style.RESET_ALL + str(player.cnt_mistakes) + "                 " + str(player.parse_mistake(player.send_mistake())))
                print(Fore.GREEN + "Time                     " + Style.RESET_ALL + str(round(player.end_time - player.start_time, 2)) + "                 " + self.parse_time(self.send_time(player)))
                self.after_play(labirint, width, height, type)
            else:
                exit()

    def generate_labirint(self, type):
        print(Fore.BLUE + "Please, tell, what size should be labirint.")
        print("height: ", end="")
        height = int(input())
        print("width: ", end="" + Style.RESET_ALL)
        width = int(input())
        labirint = Solution([[" H " for i in range(width * 2 + 1)] for j in range(height * 2 + 1)], height, width)
        use = [[0 for i in range(width)] for j in range(height)]
        if type == 1:
            labirint.make_with_dfs(use, 0, 0)
        else:
            labirint.make_with_mst()
        labirint.print_labirint()
        self.send_maze(labirint.for_print)
        self.about_solution(labirint, width, height, type)

    def start(self, type):
        enemy_maze = self.parse_maze(self.send_maze("0"))
        if enemy_maze == 0:
            print(Fore.BLUE + Style.BRIGHT + "Hello! What do you want to do?" + Style.RESET_ALL)
            print(Fore.BLUE + "<1>" + Style.RESET_ALL + "Load labirint from file.")
            print(Fore.BLUE + "<2>" + Style.RESET_ALL + "Generate new labirint.")
            print("Your choice: ", end="")
            answer = int(input())
            if answer == 1:
                array = [[]]
                with open("file.json", "r") as f:
                    array = json.load(f)["maze"]
                if array == [[]]:
                    print('File is empty now.')
                    print(Style.BRIGHT + "Do you want to generate new one?" + Style.RESET_ALL + "\nAnswer, 'yes' or 'no': ")
                    ans = str(input())
                    if ans == "no":
                        exit()
                    else:
                        self.generate_labirint(type)
                else:
                    self.send_maze(array)
                    labirint = Solution(array, (len(array) - 1) // 2, (len(array[0]) - 1) // 2)
                    labirint.make_labirint_from_file()
                    labirint.print_labirint()
                    self.about_solution(labirint, labirint.width, labirint.height, type)
            else:
                self.generate_labirint(type)
        else:
            print("Your opponent set the maze settings for you :)")
            labirint = Solution(enemy_maze, (len(enemy_maze) - 1) // 2, (len(enemy_maze[0]) - 1) // 2)
            labirint.make_labirint_from_file()
            labirint.print_labirint()
            self.about_solution(labirint, labirint.width, labirint.height, type)

    def prev_game(self):
        print("Please, write down your name: ")
        self.name = str(input())
        self.send_name(self.name)
        generate_type = self.args.type
        enemy_maze = self.parse_maze(self.send_maze("0"))
        if enemy_maze == 0:
            if self.args.type == 0:
                print(Fore.BLUE + Style.BRIGHT + "Please, choose type of building labirint.\nAnswer, '1' (DFS) or '2' (MST):" + Style.RESET_ALL)
                ans = int(input())
                generate_type = ans
        print(Fore.RED + Style.BRIGHT + "Please select whether you want to play a console game or a graphics game.\nAnswer "
                                        "'console' or 'graphics': " + Style.RESET_ALL)
        answer = str(input())
        if answer == 'console':
            self.start(generate_type)
        elif answer == 'graphics':
            pygame.init()
            screen = pygame.display.set_mode((MakeScreen.WIDTH, MakeScreen.HEIGHT))
            pygame.display.set_caption('Maze generator')
            MakeScreen.print_field(screen, generate_type, self.net, self.name)

