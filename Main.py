from colorama import Fore, Style
from Solution import Solution
from Player import Player
import MakeScreen
import pygame
import argparse
import json

parser = argparse.ArgumentParser(description="Choosing a type of generate\n")
parser.add_argument("-t", "--type", default=0, help="type of generate,\n 0 -> Create in game"
                                                    "\n 1 -> DFS,\n 2 -> MST")
args = parser.parse_args()

def about_solution(labirint, width, height, type):
    print(Fore.BLUE + Style.BRIGHT + "What do you want to do next?" + Style.RESET_ALL)
    print(Fore.BLUE + "<1>" + Style.RESET_ALL + "See the solution.")
    print(Fore.BLUE + "<2>" + Style.RESET_ALL + "Try to solve.")
    print(Fore.BLUE + "<3>" + Style.RESET_ALL + "Upload to file.")
    print(Fore.BLUE + "<4>" + Style.RESET_ALL + "Return to start.")
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
            about_solution(labirint, width, height, type)
        else:
            exit()
    elif choice == 2:
        labirint.build_labirint()
        player = Player(labirint.for_print, height, width, labirint.exit_coords[0], labirint.exit_coords[1])
        player.play()
        print(Fore.BLUE + Style.BRIGHT + "Do you want to restart?" + Style.RESET_ALL + "\nAnswer, 'yes' or 'no': ")
        answer = str(input())
        if answer == "yes":
            start(type)
        else:
            print(Fore.BLUE + Style.BRIGHT + "Do you want to return maby?" + Style.RESET_ALL + "\nAnswer, 'yes' or"
                                                                                               "'no': ")
            ans = str(input())
            if ans == "yes":
                about_solution(labirint, width, height, type)
            else:
                exit()
    elif choice == 3:
        data = {'maze': labirint.for_print}
        with open("file.json", "w") as f:
            json.dump(data, f)
        about_solution(labirint, width, height, type)
    else:
        start(type)

def generate_labirint(type):
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
    about_solution(labirint, width, height, type)

def start(type):
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
                generate_labirint(type)
        else:
            labirint = Solution(array, (len(array) - 1) // 2, (len(array[0]) - 1) // 2)
            labirint.make_labirint_from_file()
            labirint.print_labirint()
            about_solution(labirint, labirint.width, labirint.height, type)
    else:
        generate_labirint(type)

def prev_game():
    generate_type = args.type
    if args.type == 0:
        print(Fore.BLUE + Style.BRIGHT + "Please, choose type of building labirint.\nAnswer, '1' (DFS) or '2' (MST):" + Style.RESET_ALL)
        ans = int(input())
        generate_type = ans
    print(Fore.RED + Style.BRIGHT + "Please select whether you want to play a console game or a graphics game.\nAnswer "
                                    "'console' or 'graphics': " + Style.RESET_ALL)
    answer = str(input())
    if answer == 'console':
        start(generate_type)
    elif answer == 'graphics':
        pygame.init()
        screen = pygame.display.set_mode((MakeScreen.WIDTH, MakeScreen.HEIGHT))
        pygame.display.set_caption('Maze generator')
        MakeScreen.print_field(screen, generate_type)


prev_game()
