import sys
import pygame
from config import *
from Button import Button
from InputBox import InputBox
from DrawnLabirint import DrawnLabirint
from Solution import Solution
from DrawnPlayer import DrawnPlayer
import json

load_maze_button = Button(LOAD_X, LOAD_Y, LOAD_WIDTH, LOAD_HEIGHT, "Load maze from file", BROWN, DARKBROWN,
                              LIGHTBROWN)
generate_new_button = Button(LOAD_X, GENERATE_Y, LOAD_WIDTH, LOAD_HEIGHT, "Generate a new maze", BROWN, DARKBROWN,
                              LIGHTBROWN)
input_width = InputBox(INPUT_X, INPUT_Y1, INPUT_WIDTH, INPUT_HEIGHT, DARKBROWN, LIGHTBROWN, DARKBROWN)
input_height = InputBox(INPUT_X, INPUT_Y2, INPUT_WIDTH, INPUT_HEIGHT, DARKBROWN, LIGHTBROWN, DARKBROWN)
enter_button = Button(ENTER_X, ENTER_Y, ENTER_WIDTH, ENTER_HEIGHT, "OK", BROWN, DARKBROWN, LIGHTBROWN)
exit_button = Button(EXIT_X, EXIT_Y, EXIT_WIDTH, ENTER_HEIGHT, "EXIT", BROWN, DARKBROWN, LIGHTBROWN)
solution_button = Button(SOLUTION_X, SOLUTION_Y, SOLUTION_WIDTH, SOLUTION_HEIGHT, "Solution", BROWN, DARKBROWN,
                         LIGHTBROWN)
solve_button = Button(SOLUTION_X, SOLVE_Y, SOLUTION_WIDTH, SOLUTION_HEIGHT, "Solve", BROWN, DARKBROWN,
                         LIGHTBROWN)
upload_button = Button(SOLUTION_X, UPLOAD_Y, SOLUTION_WIDTH, SOLUTION_HEIGHT, "Upload", BROWN, DARKBROWN,
                         LIGHTBROWN)
back_button = Button(BACK_X, BACK_Y, BACK_WIDTH, BACK_HEIGHT, "BACK", BROWN, DARKBROWN, LIGHTBROWN)


def get_coordinate(coord):
    return coord * 2 + 1

def draw_screen(screen, generate_press, in_menu, incorrect_input, sol_press, solve_press, maze, sol, player, exit):
    screen.fill(MILKY)
    if in_menu:
        exit_button.is_active = False
        enter_button.is_active = False
        generate_new_button.is_active = True
        solution_button.is_active = False
        solve_button.is_active = False
        back_button.is_active = False
        load_maze_button.is_active = True
        upload_button.is_active = False

        font = pygame.font.SysFont('couriernew', 60)
        text_surface = font.render('MENU', True, DARKBROWN)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 250))
        screen.blit(text_surface, text_rect)
        load_maze_button.check_hover(pygame.mouse.get_pos())
        load_maze_button.draw(screen)
        generate_new_button.check_hover(pygame.mouse.get_pos())
        generate_new_button.draw(screen)
        if incorrect_input:
            font = pygame.font.SysFont('couriernew', 30)
            text_surface = font.render('Please, correct the input!', True, RED)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, 720))
            screen.blit(text_surface, text_rect)

        if generate_press:
            enter_button.is_active = True
            font = pygame.font.SysFont('couriernew', 30)
            text_surface = font.render('width:', True, DARKBROWN)
            text_rect = text_surface.get_rect(center=(355, 565))
            screen.blit(text_surface, text_rect)
            text_surface = font.render('height:', True, DARKBROWN)
            text_rect = text_surface.get_rect(center=(355, 645))
            screen.blit(text_surface, text_rect)

            input_width.check_hover(pygame.mouse.get_pos())
            input_width.draw(screen)
            input_height.check_hover(pygame.mouse.get_pos())
            input_height.draw(screen)

            enter_button.check_hover(pygame.mouse.get_pos())
            enter_button.draw(screen)
    else:
        exit_button.is_active = True
        enter_button.is_active = False
        solution_button.is_active = True
        solve_button.is_active = True
        generate_new_button.is_active = False
        back_button.is_active = False
        load_maze_button.is_active = False
        upload_button.is_active = True

        labirint = DrawnLabirint(maze, len(maze[0]), len(maze), BROWN, MILKY, GREEN, sol)
        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen)
        if sol_press:
            solution_button.is_active = False
            solve_button.is_active = False
            back_button.is_active = True
            upload_button.is_active = False
            labirint.draw_solution(screen)

            back_button.check_hover(pygame.mouse.get_pos())
            back_button.draw(screen)
        elif solve_press:
            solution_button.is_active = False
            solve_button.is_active = False
            upload_button.is_active = False
            back_button.is_active = True

            labirint.draw_solve(screen, get_coordinate(player.x), get_coordinate(player.y))
            if exit[0] == -1: exit[0] = len(maze[0]) - 1
            if exit[1] == -1: exit[1] = len(maze) - 1
            if [get_coordinate(player.x), get_coordinate(player.y)] == [exit[0] - 1, exit[1]] or [get_coordinate(player.x), get_coordinate(player.y)] == [exit[0], exit[1] - 1]:
                font = pygame.font.SysFont('couriernew', 40)
                text_surface = font.render('YOU WIN!', True, GREEN)
                text_rect = text_surface.get_rect(center=(900, 300))
                screen.blit(text_surface, text_rect)

            back_button.check_hover(pygame.mouse.get_pos())
            back_button.draw(screen)
        else:
            labirint.draw(screen)

            solution_button.check_hover(pygame.mouse.get_pos())
            solution_button.draw(screen)
            solve_button.check_hover(pygame.mouse.get_pos())
            solve_button.draw(screen)
            upload_button.check_hover(pygame.mouse.get_pos())
            upload_button.draw(screen)

def handle_events(event, player):
    input_width.handle_event(event)
    input_height.handle_event(event)
    if player != None:
        player.handle_event(event)
    generate_new_button.handle_event(event)
    enter_button.handle_event(event)
    exit_button.handle_event(event)
    solution_button.handle_event(event)
    back_button.handle_event(event)
    solve_button.handle_event(event)
    load_maze_button.handle_event(event)
    upload_button.handle_event(event)

def print_field(screen, gen_type):
    generate_press = False
    in_menu = True
    incorrect_input = False
    solution_press = False
    solve_press = False
    player = None
    maze = []
    sol = []
    exit_coords = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == generate_new_button:
                generate_press = not generate_press
            if event.type == pygame.USEREVENT and event.button == enter_button:
                if input_width.text != '' and input_height.text != '' and int(input_height.text) >= 2 and int(input_width.text) >= 2:
                    in_menu = False
                    labirint = Solution([[" H " for i in range(get_coordinate(int(input_width.text)))] for j in range(get_coordinate(int(input_height.text)))], int(input_height.text), int(input_width.text))
                    exit_coords = labirint.exit_coords
                    use = [[0 for i in range(int(input_width.text))] for j in range(int(input_height.text))]
                    if gen_type == 1:
                        labirint.make_with_dfs(use, 0, 0)
                    else:
                        labirint.make_with_mst()
                    labirint.build_labirint()
                    maze = labirint.for_print
                    use = [[0 for i in range(int(input_width.text))] for j in range(int(input_height.text))]
                    labirint.make_way_dfs(use, 0, 0)
                    labirint.make_solution()
                    labirint.get_solution()
                    sol = labirint.for_print_solution
                else:
                    incorrect_input = True
            if event.type == pygame.USEREVENT and event.button == exit_button:
                in_menu = True
                incorrect_input = False
                generate_press = False
                solution_press = False
                solve_press = False
            if event.type == pygame.USEREVENT and event.button == solution_button:
                solution_press = True
            # I make solve_press and solution_press in false, because this button(back_button) is on solve page and on
            # solution page, so if we are on solution page we need to make solution_press false and if we are on solve
            # page we need to make solve_press false(solve_press may be true before we click on back_button)
            if event.type == pygame.USEREVENT and event.button == back_button:
                solution_press = False
                solve_press = False
            if event.type == pygame.USEREVENT and event.button == solve_button:
                solve_press = True
                player = DrawnPlayer((len(maze) - 1) // 2, (len(maze[0]) - 1) // 2, maze)
            if event.type == pygame.USEREVENT and event.button == load_maze_button:
                with open("file.json", "r") as f:
                    maze = json.load(f)["maze"]
                if maze != []:
                    in_menu = False
                    labirint = Solution(maze, (len(maze) - 1) // 2, (len(maze[0]) - 1) // 2)
                    labirint.make_labirint_from_file()
                    exit_coords = labirint.exit_coords
                    use = [[0 for i in range(labirint.width)] for j in range(labirint.height)]
                    labirint.make_way_dfs(use, 0, 0)
                    labirint.make_solution()
                    labirint.get_solution()
                    sol = labirint.for_print_solution
            if event.type == pygame.USEREVENT and event.button == upload_button:
                data = {'maze': maze}
                with open("file.json", "w") as f:
                    json.dump(data, f)
            handle_events(event, player)
        draw_screen(screen, generate_press, in_menu, incorrect_input, solution_press, solve_press, maze, sol, player, exit_coords)
        pygame.display.flip()
