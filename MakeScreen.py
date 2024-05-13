import sys

import pygame
import source.interface.Cubes
from source.interface.Button import Button
from source.interface.Table import Table
from source.interface.Clock import Clock
import random
import time

coords_x = [590, 760, 930, 680, 860]
coords_y = [220, 220, 220, 390, 390]

WIDTH = 1030
HEIGHT = 800
FPS = 60
COUNTDOWN = 5 * FPS
GREEN = (105, 139, 34)
BROWN = (115, 66, 34)
DARKBROWN = (77, 34, 14)
LIGHTBROWN = (188, 152, 126)
RED = (196, 30, 58)
usercomb = ["0"] * 16
compcomb = ["0"] * 16
is_fixed_dice = [False] * 5
start_timer_seconds = 0

first_cube = source.interface.Cubes.Cubes(coords_x[0], coords_y[0])
second_cube = source.interface.Cubes.Cubes(coords_x[1], coords_y[1])
third_cube = source.interface.Cubes.Cubes(coords_x[2], coords_y[2])
fourth_cube = source.interface.Cubes.Cubes(coords_x[3], coords_y[3])
fifth_cube = source.interface.Cubes.Cubes(coords_x[4], coords_y[4])
cubes = [first_cube, second_cube, third_cube, fourth_cube, fifth_cube]
nums = [random.randint(1, 6) for i in range(5)]
start_button = Button(607, 663, 300, 100, "START", BROWN, DARKBROWN, LIGHTBROWN)
throw_button = Button(585, 663, 344, 100, "Roll the dice", BROWN, DARKBROWN, LIGHTBROWN)
table = Table(20, 20, 470, 750, LIGHTBROWN, BROWN)
clock = Clock(760, 20, 220, 85, LIGHTBROWN, BROWN)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Dice poker')
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # (0, 0), pygame.RESIZABLE)


def choose_num(num, i):
    if num == 1: cubes[i].states.one_up(screen)
    if num == 2: cubes[i].states.two_up(screen)
    if num == 3: cubes[i].states.three_up(screen)
    if num == 4: cubes[i].states.four_up(screen)
    if num == 5: cubes[i].states.five_up(screen)
    if num == 6: cubes[i].states.six_up(screen)

def roll_dice(combs):
    for i in range(5):
        if is_fixed_dice[i] == False:
            cubes[i].states = random.choice([source.interface.Cubes.Cubes.FirstType,
                                             source.interface.Cubes.Cubes.SecondType,
                                             source.interface.Cubes.Cubes.ThirdType])(coords_x[i], coords_y[i])
            nums[i] = int(combs[i])

def draw_screen(in_start, users_turn):
    screen.fill(GREEN)
    if in_start:
        start_button.active = True
        clock.draw(screen, 5 * 60)
        start_button.check_hover(pygame.mouse.get_pos())
        start_button.draw(screen)
        table.draw(usercomb, compcomb, screen)
    else:
        start_button.active = False
        if users_turn:
            table.active = True
            throw_button.active = True
            throw_button.check_hover(pygame.mouse.get_pos())
            for i in range(15):
                table.check_hover(pygame.mouse.get_pos(), i)
        else:
            table.active = False
            throw_button.active = False
            for i in range(15):
                table.is_hovered[i] = False
            for cube in [first_cube.states, second_cube.states, third_cube.states, fourth_cube.states, fifth_cube.states]:
                cube.color = GREEN
        clock.draw(screen, 5 * 60 - int(time.time() - start_timer_seconds))
        throw_button.draw(screen)
        for i in range(15):
            table.draw(usercomb, compcomb, screen)
    for i in range(5):
        cubes[i].states.draw_cube(screen)
        choose_num(nums[i], i)
        if users_turn:
            cubes[i].states.check_hover(pygame.mouse.get_pos())
            cubes[i].states.draw_fixing(screen)
            counter = 0
        elif not in_start:
            pygame.draw.rect(screen, DARKBROWN, (0.3 * WIDTH - 7, 0.4 * HEIGHT - 7, 0.4 * WIDTH + 14, 0.2 * HEIGHT + 14), 0, 10)
            pygame.draw.rect(screen, LIGHTBROWN, (0.3 * WIDTH, 0.4 * HEIGHT, 0.4 * WIDTH, 0.2 * HEIGHT), 0, 10)
            font = pygame.font.SysFont('couriernew', 40)
            text_surface = font.render("Now it is comp's turn!", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)


def change_user_comb(new_user_comb):
    for i in range(1, 16):
        if new_user_comb[i] != '-1':
            usercomb[i] = new_user_comb[i]


def change_comp_comb(new_comp_comb):
    for i in range(1, 16):
        if new_comp_comb[i] != '-1':
            compcomb[i] = new_comp_comb[i]

def do_fix(kind):
    if kind == first_cube.states: is_fixed_dice[0] = not is_fixed_dice[0]
    if kind == second_cube.states: is_fixed_dice[1] = not is_fixed_dice[1]
    if kind == third_cube.states: is_fixed_dice[2] = not is_fixed_dice[2]
    if kind == fourth_cube.states: is_fixed_dice[3] = not is_fixed_dice[3]
    if kind == fifth_cube.states: is_fixed_dice[4] = not is_fixed_dice[4]


def return_fixed_cubes():
    fixed_cubes = ""
    for i in range(5):
        fixed_cubes += str(int(is_fixed_dice[i])) + " "
    return fixed_cubes


def print_field():
    in_start = True
    users_turn = False
    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button in [first_cube.states, second_cube.states,
                                                                   third_cube.states, fourth_cube.states,
                                                                   fifth_cube.states]:
                event.button.is_fixed = not event.button.is_fixed
                event.button.color = RED if event.button.is_fixed else GREEN
                do_fix(event.button)
            if event.type == pygame.USEREVENT and event.button == start_button:
                global start_timer_seconds
                start_timer_seconds = time.time()
                a = "1"
                with open('./source/connection.json') as f:
                    a = f.readline()
                    cubs = f.readline().split()
                    new_user_comb = f.readline().split()
                    number_of_throw = f.readline()
                    roll_dice(cubs)
                    change_user_comb(new_user_comb)
                in_start = False
                users_turn = True
            if event.type == pygame.USEREVENT and event.button == throw_button and int(number_of_throw) < 2:
                with open('./source/connection.json', 'w') as f:
                    f.write("next\n")
                with open('./source/connection.json', 'a') as f:
                    f.write(return_fixed_cubes())
                time.sleep(1)
                a = "1"
                while a != "my_throw" and a != "my_throw\n":
                    with open('./source/connection.json') as f:
                        a = f.readline()
                        cubs = f.readline().split()
                        new_user_comb = f.readline().split()
                        number_of_throw = f.readline()
                        if (a != "my_throw" and a != "my_throw\n"):
                            time.sleep(0.001)
                            continue
                        roll_dice(cubs)
                        change_user_comb(new_user_comb)
                is_fixed_dice = [False] * 5
            if event.type == pygame.USEREVENT and event.button == table:
                users_turn = False

            first_cube.states.handle_event(event)
            second_cube.states.handle_event(event)
            third_cube.states.handle_event(event)
            fourth_cube.states.handle_event(event)
            fifth_cube.states.handle_event(event)
            start_button.handle_event(event)
            throw_button.handle_event(event)
            for i in range(15):
                table.handle_event(event, i, usercomb[i + 1])

        if counter > 40:
            users_turn = True
            counter = 0
        draw_screen(in_start, users_turn)
        if not users_turn and not in_start:
            counter += 1
        pygame.display.flip()

if __name__ == "__main__":
   print_field() 