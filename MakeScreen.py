import sys
import time

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
solution_button = Button(SOLUTION_X, SOLUTION_Y, SOLUTION_WIDTH, SOLUTION_HEIGHT, "Solution", BROWN, DARKBROWN,
                         LIGHTBROWN)
solve_button = Button(SOLUTION_X, SOLUTION_Y, SOLUTION_WIDTH, SOLVE_HEIGHT, "START", BROWN, DARKBROWN,
                         LIGHTBROWN)
upload_button = Button(SOLUTION_X, UPLOAD_Y, SOLUTION_WIDTH, SOLUTION_HEIGHT, "Upload", BROWN, DARKBROWN,
                         LIGHTBROWN)
back_button = Button(BACK_X, BACK_Y, BACK_WIDTH, BACK_HEIGHT, "BACK", BROWN, DARKBROWN, LIGHTBROWN)

def get_coordinate(coord):
    return coord * 2 + 1

def draw_text(screen, text, size, coord_x, coord_y, color):
    font = pygame.font.SysFont('couriernew', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(coord_x, coord_y))
    screen.blit(text_surface, text_rect)

def send_mistake(player, net):
    data = "mistake:" + str(net.id) + ":" + str(player.mistakes)
    reply = net.send(data)
    return reply
def parse_mistake(data):
    try:
        d = data.split(":")[2]
        return int(d)
    except:
        return 0

def send_maze(net, maze):
    data = "choose maze:" + str(net.id) + ":" + str(maze)
    reply = net.send(data)
    return reply

def parse_maze(data):
    try:
        d = data.split(":")[2]
        return eval(d)
    except:
        return 0

def send_start(net, value):
    data = "start:" + str(net.id) + ":" + str(value)
    reply = net.send(data)
    return reply

def parse_start(data):
    try:
        d = data.split(":")[2]
        return int(d)
    except:
        return 0

def send_finish(net, value):
    data = "finish:" + str(net.id) + ":" + str(value)
    reply = net.send(data)
    return reply

def parse_finish(data):
    try:
        d = data.split(":")[2]
        return int(d)
    except:
        return 0
def send_time(net, player):
    data = "time:" + str(net.id) + ":" + str(round(player.end_time - player.start_time, 2))
    reply = net.send(data)
    return reply

def parse_time(data):
    try:
        d = data.split(":")[2]
        return str(d)
    except:
        return 0
def send_name(net, name):
    data = "name:" + str(net.id) + ":" + str(name)
    reply = net.send(data)
    return reply

def parse_name(data):
    try:
        d = data.split(":")[2]
        return str(d)
    except:
        return 0

def draw_screen(screen, generate_press, in_menu, incorrect_input, sol_press, solve_press, maze, sol, player, exit, net, after_game, name):
    screen.fill(MILKY)
    if in_menu:
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
        enter_button.is_active = False
        solve_button.is_active = True
        generate_new_button.is_active = False
        back_button.is_active = False
        load_maze_button.is_active = False
        labirint = DrawnLabirint(maze, len(maze[0]), len(maze), BROWN, MILKY, GREEN, sol)
        if sol_press:
            solution_button.is_active = False
            solve_button.is_active = False
            back_button.is_active = True
            upload_button.is_active = False
            labirint.draw_solution(screen)

            back_button.check_hover(pygame.mouse.get_pos())
            back_button.draw(screen)
        elif solve_press:
            if parse_start(send_start(net, "1")) == 1:
                solution_button.is_active = False
                solve_button.is_active = False
                upload_button.is_active = False
                back_button.is_active = False
                if player.start_time == 0:
                    player.start_time = time.time()
                labirint.draw_solve(screen, get_coordinate(player.x), get_coordinate(player.y))
                if exit[0] == -1: exit[0] = len(maze[0]) - 1
                if exit[1] == -1: exit[1] = len(maze) - 1
                if [get_coordinate(player.x), get_coordinate(player.y)] == [exit[0] - 1, exit[1]] or [get_coordinate(player.x), get_coordinate(player.y)] == [exit[0], exit[1] - 1]:
                    player.finish = True
                    if player.end_time == 0:
                        player.end_time = time.time()
                    send_time(net, player)
                    if parse_finish(send_finish(net, "1")) == 0:
                        player.win = True
                    total = 'YOU LOSE'
                    color = RED
                    if player.win:
                        total = 'YOU WIN!'
                        color = GREEN
                    draw_text(screen, total, 37, 900, 300, color)
                draw_text(screen, 'You: ' + str(player.mistakes), 30, 900, 400, DARKBROWN)
                # send network stuff
                player.enemy_mistakes = parse_mistake(send_mistake(player, net))

                draw_text(screen, "Enemy: " + str(player.enemy_mistakes), 30, 900, 460, DARKBROWN)
            else:
                solve_button.is_active = False
                pygame.draw.rect(screen, DARKBROWN, (WIDTH * 0.2 - BORDER_WIDTH, HEIGHT * 0.4 - BORDER_WIDTH, WIDTH * 0.6 + BORDER_WIDTH * 2, HEIGHT * 0.2 + BORDER_WIDTH * 2), 0, 10)
                pygame.draw.rect(screen, LIGHTBROWN, (WIDTH * 0.2, HEIGHT * 0.4, WIDTH * 0.6, HEIGHT * 0.2), 0, 10)
                draw_text(screen, "Waiting for opponent...", 30, WIDTH / 2, HEIGHT / 2, DARKBROWN)
        elif after_game:
            solution_button.is_active = True
            upload_button.is_active = True
            back_button.is_active = False
            solve_button.is_active = False

            draw_text(screen, "RESULTS", 60, 410, 110, DARKBROWN)
            pygame.draw.rect(screen, DARKBROWN, (TABLE_X - BORDER_WIDTH, TABLE_Y - BORDER_WIDTH, TABLE_WIDTH + 2 * BORDER_WIDTH, TABLE_HEIGHT + 2 * BORDER_WIDTH), 0, 10)
            pygame.draw.rect(screen, LIGHTBROWN, (TABLE_X, TABLE_Y, TABLE_WIDTH, TABLE_HEIGHT), 0, 10)
            for i in range(3):
                if i != 2:
                    pygame.draw.line(screen, DARKBROWN, (TABLE_X + (i + 1) * TABLE_WIDTH / 3, TABLE_Y + BORDER_WIDTH), (TABLE_X + (i + 1) * TABLE_WIDTH / 3, TABLE_Y + TABLE_HEIGHT - BORDER_WIDTH), 3)
                pygame.draw.line(screen, DARKBROWN, (TABLE_X + BORDER_WIDTH, TABLE_Y + (i + 1) * TABLE_HEIGHT / 4), (TABLE_X + TABLE_WIDTH - BORDER_WIDTH, TABLE_Y + (i + 1) * TABLE_HEIGHT / 4), 3)
            draw_text(screen, name, 30, TABLE_X + TABLE_WIDTH / 2, TABLE_Y + TABLE_HEIGHT / 8, DARKBROWN)
            draw_text(screen, parse_name(send_name(net, name)), 30, TABLE_X + 5 * TABLE_WIDTH / 6, TABLE_Y + TABLE_HEIGHT / 8, DARKBROWN)
            draw_text(screen, "Total", 30, TABLE_X + TABLE_WIDTH / 6, TABLE_Y + 3 * TABLE_HEIGHT / 8, DARKBROWN)
            draw_text(screen, "Mistakes", 30, TABLE_X + TABLE_WIDTH / 6, TABLE_Y + 5 * TABLE_HEIGHT / 8, DARKBROWN)
            draw_text(screen, "Time", 30, TABLE_X + TABLE_WIDTH / 6, TABLE_Y + 7 * TABLE_HEIGHT / 8, DARKBROWN)
            total1, total2 = ("WIN" if player.win else "LOSE"), ("LOSE" if player.win else "WIN")
            draw_text(screen, total1, 30, TABLE_X + TABLE_WIDTH / 2, TABLE_Y + TABLE_HEIGHT * 3 / 8, DARKBROWN)
            draw_text(screen, total2, 30, TABLE_X + 5 * TABLE_WIDTH / 6, TABLE_Y + TABLE_HEIGHT * 3 / 8, DARKBROWN)
            draw_text(screen, str(player.mistakes), 30, TABLE_X + TABLE_WIDTH / 2, TABLE_Y + TABLE_HEIGHT * 5 / 8, DARKBROWN)
            draw_text(screen, str(player.enemy_mistakes), 30, TABLE_X + TABLE_WIDTH * 5 / 6, TABLE_Y + TABLE_HEIGHT * 5 / 8, DARKBROWN)
            draw_text(screen, str(round(player.end_time - player.start_time, 2)), 30, TABLE_X + TABLE_WIDTH / 2, TABLE_Y + TABLE_HEIGHT * 7 / 8, DARKBROWN)
            draw_text(screen, parse_time(send_time(net, player)), 30, TABLE_X + TABLE_WIDTH * 5 / 6, TABLE_Y + 7 * TABLE_HEIGHT / 8, DARKBROWN)
            solution_button.check_hover(pygame.mouse.get_pos())
            solution_button.draw(screen)
            upload_button.check_hover(pygame.mouse.get_pos())
            upload_button.draw(screen)
        else:
            labirint.draw(screen)
            solve_button.check_hover(pygame.mouse.get_pos())
            solve_button.draw(screen)

def handle_events(event, player):
    input_width.handle_event(event)
    input_height.handle_event(event)
    if player != None:
        player.handle_event(event)
    generate_new_button.handle_event(event)
    enter_button.handle_event(event)
    solution_button.handle_event(event)
    back_button.handle_event(event)
    solve_button.handle_event(event)
    load_maze_button.handle_event(event)
    upload_button.handle_event(event)

def print_field(screen, gen_type, net, name):
    enemy_maze = parse_maze(send_maze(net, "0"))
    generate_press = False
    in_menu = True
    incorrect_input = False
    solution_press = False
    solve_press = False
    after_game = False
    player = None
    maze = []
    sol = []
    exit_coords = []
    if enemy_maze != 0:
        in_menu = False
        maze = enemy_maze
        labirint = Solution(maze, (len(maze) - 1) // 2, (len(maze[0]) - 1) // 2)
        labirint.make_labirint_from_file()
        exit_coords = labirint.exit_coords
        use = [[0 for i in range(labirint.width)] for j in range(labirint.height)]
        labirint.make_way_dfs(use, 0, 0)
        labirint.make_solution()
        labirint.get_solution()
        sol = labirint.for_print_solution
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
                    send_maze(net, maze)
                    use = [[0 for i in range(int(input_width.text))] for j in range(int(input_height.text))]
                    labirint.make_way_dfs(use, 0, 0)
                    labirint.make_solution()
                    labirint.get_solution()
                    sol = labirint.for_print_solution
                else:
                    incorrect_input = True
            if event.type == pygame.USEREVENT and event.button == solution_button:
                solution_press = True
                send_start(net, "1")
            # I make solve_press and solution_press in false, because this button(back_button) is on solve page and on
            # solution page, so if we are on solution page we need to make solution_press false and if we are on solve
            # page we need to make solve_press false(solve_press may be true before we click on back_button)
            if event.type == pygame.USEREVENT and event.button == back_button:
                solution_press = False
                solve_press = False
                after_game = True
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
                    send_maze(net, maze)
            if event.type == pygame.USEREVENT and event.button == upload_button:
                data = {'maze': maze}
                with open("file.json", "w") as f:
                    json.dump(data, f)
            if player != None and player.finish and parse_finish(send_finish(net, str(int(player.finish)))) == 1:
                after_game = True
                solve_press = False
            handle_events(event, player)
        draw_screen(screen, generate_press, in_menu, incorrect_input, solution_press, solve_press, maze, sol, player, exit_coords, net, after_game, name)
        pygame.display.flip()
