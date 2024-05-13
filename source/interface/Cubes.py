import pygame
import random
color_up = (196, 30, 58)
side_x_1 = 43
side_y_1 = 48

side_x_2 = 70
side_y_2 = 45
side_z = 60


class Cubes():
    class FirstType():
        def __init__(self, x_coord, y_coord):
            self.x = x_coord
            self.y = y_coord
            self.is_hovered = False
            self.is_fixed = False
            self.color = (105, 139, 34)
            self.image = pygame.Rect(self.x - 15 * side_x_1 / 8, self.y, 23 * side_x_1 / 8,
                                        1.8 * side_y_1 + side_z)
            self.to_fix =  [(self.x + 2, self.y - 6), (self.x + side_x_1 + 6, self.y + side_y_1 - 1),
                    (self.x + side_x_1 + 6, self.y + side_y_1 + side_z + 4),
                    (self.x - 7 * side_x_1 / 8 - 1, self.y + 1.8 * side_y_1 + side_z + 7),
                    (self.x - 15 * side_x_1 / 8 - 6, self.y + 0.8 * side_y_1 + side_z + 2),
                    (self.x - 15 * side_x_1 / 8 - 6, self.y + 0.8 * side_y_1 - 3)]
        def check_hover(self, mouse_pos):
            self.is_hovered = self.image.collidepoint(mouse_pos)
        def draw_cube(self, surface):
            first = [(self.x, self.y), (self.x + side_x_1, self.y + side_y_1),
                    (self.x - 7 * side_x_1 / 8, self.y + 1.8 * side_y_1),
                    (self.x - 15 * side_x_1 / 8, self.y + 0.8 * side_y_1)]
            second = [(self.x + side_x_1, self.y + side_y_1), (self.x - 7 * side_x_1 / 8, self.y + 1.8 * side_y_1),
                    (self.x - 7 * side_x_1 / 8, self.y + 1.8 * side_y_1 + side_z),
                    (self.x + side_x_1, self.y + side_y_1 + side_z)]
            third = [(self.x - 7 * side_x_1 / 8, self.y + 1.8 * side_y_1),
                    (self.x - 15 * side_x_1 / 8, self.y + 0.8 * side_y_1),
                    (self.x - 15 * side_x_1 / 8, self.y + 0.8 * side_y_1 + side_z),
                    (self.x - 7 * side_x_1 / 8, self.y + 1.8 * side_y_1 + side_z)]
            pygame.draw.polygon(surface, (255, 255, 255), first, width=0)
            pygame.draw.polygon(surface, (200, 200, 200), second, width=0)
            pygame.draw.polygon(surface, (225, 225, 225), third, width=0)
            pygame.draw.polygon(surface, (0, 0, 0), first, width=2)
            pygame.draw.polygon(surface, (0, 0, 0), second, width=2)
            pygame.draw.polygon(surface, (0, 0, 0), third, width=2)
            pygame.draw.polygon(surface, self.color, self.to_fix, 3)

        def draw_fixing(self, surface):
            color = self.color if self.color == (196, 30, 58) else (255, 255, 255)
            cur_color = color if self.is_hovered else self.color
            pygame.draw.polygon(surface, cur_color, self.to_fix, 3)
        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        def draw_point(self, x_coord, y_coord, angle, color, surface):
            target_rect = pygame.Rect((x_coord, y_coord, 14, 9))
            shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size))
            rotated_surf = pygame.transform.rotate(shape_surf, angle)
            surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))

        # left side:
        def one_left(self, surface):
            self.draw_point(self.x - 65, self.y + 89, -52, (0, 0, 0), surface)

        def two_left(self, surface):
            self.draw_point(self.x - 76, self.y + 93, -52, (0, 0, 0), surface)
            self.draw_point(self.x - 54, self.y + 85, -52, (0, 0, 0), surface)

        def three_left(self, surface):
            self.one_left(surface)
            self.two_left(surface)

        def four_left(self, surface):
            self.two_left(surface)
            self.draw_point(self.x - 76, self.y + 63, -52, (0, 0, 0), surface)
            self.draw_point(self.x - 54, self.y + 113, -52, (0, 0, 0), surface)

        def five_left(self, surface):
            self.four_left(surface)
            self.one_left(surface)

        def six_left(self, surface):
            self.four_left(surface)
            self.draw_point(self.x - 76, self.y + 78, -52, (0, 0, 0), surface)
            self.draw_point(self.x - 54, self.y + 99, -52, (0, 0, 0), surface)
        #right side
        def one_right(self, surface):
            self.draw_point(self.x - 2, self.y + 93, 25, (0, 0, 0), surface)

        def two_right(self, surface):
            self.draw_point(self.x - 27, self.y + 90, 25, (0, 0, 0), surface)
            self.draw_point(self.x + 22, self.y + 97, 25, (0, 0, 0), surface)

        def three_right(self, surface):
            self.one_right(surface)
            self.two_right(surface)

        def four_right(self, surface):
            self.two_right(surface)
            self.draw_point(self.x - 27, self.y + 118, 25, (0, 0, 0), surface)
            self.draw_point(self.x + 22, self.y + 67, 25, (0, 0, 0), surface)

        def five_right(self, surface):
            self.four_right(surface)
            self.one_right(surface)

        def six_right(self, surface):
            self.four_right(surface)
            self.draw_point(self.x - 27, self.y + 104, 25, (0, 0, 0), surface)
            self.draw_point(self.x + 22, self.y + 82, 25, (0, 0, 0), surface)
        #main side
        def one_up(self, surface):
            self.draw_point(self.x - 23, self.y + 40, 21, color_up, surface)
            self.five_left(surface)
            self.four_right(surface)
        def two_up(self, surface):
            self.draw_point(self.x + 9, self.y + 40, 21, color_up, surface)
            self.draw_point(self.x - 57, self.y + 38, 21, color_up, surface)
            self.four_left(surface)
            self.one_right(surface)
        def three_up(self, surface):
            self.draw_point(self.x - 23, self.y + 40, 21, color_up, surface)
            self.draw_point(self.x + 9, self.y + 40, 21, color_up, surface)
            self.draw_point(self.x - 57, self.y + 38, 21, color_up, surface)
            self.two_left(surface)
            self.six_right(surface)
        def four_up(self, surface):
            self.draw_point(self.x + 9, self.y + 40, 21, color_up, surface)
            self.draw_point(self.x - 57, self.y + 38, 21, color_up, surface)
            self.draw_point(self.x - 35, self.y + 60, 21, color_up, surface)
            self.draw_point(self.x - 13, self.y + 16, 21, color_up, surface)
            self.six_left(surface)
            self.two_right(surface)
        def five_up(self, surface):
            self.draw_point(self.x + 9, self.y + 40, 21, color_up, surface)
            self.draw_point(self.x - 57, self.y + 38, 21, color_up, surface)
            self.draw_point(self.x - 35, self.y + 60, 21, color_up, surface)
            self.draw_point(self.x - 13, self.y + 16, 21, color_up, surface)
            self.draw_point(self.x - 23, self.y + 40, 21, color_up, surface)
            self.one_left(surface)
            self.three_right(surface)
        def six_up(self, surface):
            self.draw_point(self.x + 9, self.y + 40, 21, color_up, surface)
            self.draw_point(self.x - 57, self.y + 38, 21, color_up, surface)
            self.draw_point(self.x - 35, self.y + 60, 21, color_up, surface)
            self.draw_point(self.x - 13, self.y + 16, 21, color_up, surface)
            self.draw_point(self.x - 2, self.y + 29, 21, color_up, surface)
            self.draw_point(self.x - 45, self.y + 49, 21, color_up, surface)
            self.three_left(surface)
            self.five_right(surface)

    class SecondType():
        def __init__(self, x_coord, y_coord):
            self.x = x_coord
            self.y = y_coord
            self.is_hovered = False
            self.is_fixed = False
            self.color = (105, 139, 34)
            self.image = pygame.Rect(self.x - 5 * side_x_2 / 6, self.y, 11 * side_x_2 / 6,
                                        2 * side_y_2 + side_z)
            self.to_fix = [(self.x, self.y - 6), (self.x + side_x_2 + 6, self.y + side_y_2 - 2),
                        (self.x + side_x_2 + 6, self.y + side_y_2 + side_z + 3),
                        (self.x + side_x_2 / 6 + 1, self.y + side_y_2 * 2 + side_z + 7),
                        (self.x - side_x_2 * 5 / 6 - 5, self.y + side_y_2 + side_z + 3),
                        (self.x - side_x_2 * 5 / 6 - 5, self.y + side_y_2 - 3)]
        def check_hover(self, mouse_pos):
            self.is_hovered = self.image.collidepoint(mouse_pos)
        def draw_cube(self, surface):
            first = [(self.x, self.y), (self.x + side_x_2, self.y + side_y_2),
                    (self.x + side_x_2 / 6, self.y + side_y_2 * 2),
                    (self.x - side_x_2 * 5 / 6, self.y + side_y_2)]
            second = [(self.x + side_x_2, self.y + side_y_2), (self.x + side_x_2 / 6, self.y + side_y_2 * 2),
                    (self.x + side_x_2 / 6, self.y + side_y_2 * 2 + side_z),
                    (self.x + side_x_2, self.y + side_y_2 + side_z)]
            third = [(self.x + side_x_2 / 6, self.y + side_y_2 * 2), (self.x - side_x_2 * 5 / 6, self.y + side_y_2),
                    (self.x - side_x_2 * 5 / 6, self.y + side_y_2 + side_z),
                    (self.x + side_x_2 / 6, self.y + side_y_2 * 2 + side_z)]
            pygame.draw.polygon(surface, (255, 255, 255), first, width=0)
            pygame.draw.polygon(surface, (200, 200, 200), second, width=0)
            pygame.draw.polygon(surface, (225, 225, 225), third, width=0)
            pygame.draw.polygon(surface, (0, 0, 0), first, width=2)
            pygame.draw.polygon(surface, (0, 0, 0), second, width=2)
            pygame.draw.polygon(surface, (0, 0, 0), third, width=2)
            pygame.draw.polygon(surface, self.color, self.to_fix, 3)

        def draw_fixing(self, surface):
            color = self.color if self.color == (196, 30, 58) else (255, 255, 255)
            cur_color = color if self.is_hovered else self.color
            pygame.draw.polygon(surface, cur_color, self.to_fix, 3)
        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        def draw_point(self, x_coord, y_coord, angle, color, surface):
            target_rect = pygame.Rect((x_coord, y_coord, 14, 10))
            shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size))
            rotated_surf = pygame.transform.rotate(shape_surf, angle)
            surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))
        #left side:
        def one_left(self, surface):
            self.draw_point(self.x - 30, self.y + 93, -32, (0, 0, 0), surface)
        def two_left(self, surface):
            self.draw_point(self.x - 12, self.y + 90, -32, (0, 0, 0), surface)
            self.draw_point(self.x - 50, self.y + 95, -32, (0, 0, 0), surface)
        def three_left(self, surface):
            self.one_left(surface)
            self.two_left(surface)
        def four_left(self, surface):
            self.two_left(surface)
            self.draw_point(self.x - 50, self.y + 68, -32, (0, 0, 0), surface)
            self.draw_point(self.x - 12, self.y + 117, -32, (0, 0, 0), surface)
        def five_left(self, surface):
            self.four_left(surface)
            self.one_left(surface)
        def six_left(self, surface):
            self.four_left(surface)
            self.draw_point(self.x - 12, self.y + 103, -32, (0, 0, 0), surface)
            self.draw_point(self.x - 50, self.y + 82, -32, (0, 0, 0), surface)
        #right side:
        def one_right(self, surface):
            self.draw_point(self.x + 36, self.y + 93, 46, (0, 0, 0), surface)
        def two_right(self, surface):
            self.draw_point(self.x + 18, self.y + 91, 46, (0, 0, 0), surface)
            self.draw_point(self.x + 51, self.y + 95, 46, (0, 0, 0), surface)
        def three_right(self, surface):
            self.one_right(surface)
            self.two_right(surface)
        def four_right(self, surface):
            self.two_right(surface)
            self.draw_point(self.x + 51, self.y + 67, 46, (0, 0, 0), surface)
            self.draw_point(self.x + 18, self.y + 118, 46, (0, 0, 0), surface)
        def five_right(self, surface):
            self.four_right(surface)
            self.one_right(surface)
        def six_right(self, surface):
            self.four_right(surface)
            self.draw_point(self.x + 18, self.y + 104, 46, (0, 0, 0), surface)
            self.draw_point(self.x + 51, self.y + 81, 46, (0, 0, 0), surface)
        
        #main side
        def one_up(self, surface):
            self.draw_point(self.x + 1, self.y + 40, 36, color_up, surface)
            self.two_left(surface)
            self.four_right(surface)
        def two_up(self, surface):
            self.draw_point(self.x + 31, self.y + 40, 36, color_up, surface)
            self.draw_point(self.x - 33, self.y + 40, 36, color_up, surface)
            self.four_left(surface)
            self.one_right(surface)
        def three_up(self, surface):
            self.draw_point(self.x + 1, self.y + 40, 36, color_up, surface)
            self.draw_point(self.x + 31, self.y + 40, 36, color_up, surface)
            self.draw_point(self.x - 33, self.y + 40, 36, color_up, surface)
            self.five_left(surface)
            self.six_right(surface)
        def four_up(self, surface):
            self.draw_point(self.x + 31, self.y + 43, 36, color_up, surface)
            self.draw_point(self.x - 33, self.y + 40, 36, color_up, surface)
            self.draw_point(self.x - 6, self.y + 20, 36, color_up, surface)
            self.draw_point(self.x + 2, self.y + 63, 36, color_up, surface)
            self.six_left(surface)
            self.two_right(surface)
        def five_up(self, surface):
            self.draw_point(self.x + 31, self.y + 43, 36, color_up, surface)
            self.draw_point(self.x - 33, self.y + 40, 36, color_up, surface)
            self.draw_point(self.x - 6, self.y + 20, 36, color_up, surface)
            self.draw_point(self.x + 2, self.y + 63, 36, color_up, surface)
            self.draw_point(self.x + 1, self.y + 40, 36, color_up, surface)
            self.one_left(surface)
            self.three_right(surface)
        def six_up(self, surface):
            self.draw_point(self.x + 31, self.y + 43, 36, color_up, surface)
            self.draw_point(self.x - 33, self.y + 40, 36, color_up, surface)
            self.draw_point(self.x - 6, self.y + 20, 36, color_up, surface)
            self.draw_point(self.x + 2, self.y + 63, 36, color_up, surface)
            self.draw_point(self.x + 13, self.y + 32, 36, color_up, surface)
            self.draw_point(self.x - 16, self.y + 51, 36, color_up, surface)
            self.three_left(surface)
            self.five_right(surface)
    class ThirdType():
        def __init__(self, x_coord, y_coord):
            self.x = x_coord
            self.y = y_coord
            self.is_hovered = False
            self.is_fixed = False
            self.color = (105, 139, 34)
            self.image = pygame.Rect(self.x - 5 * side_x_2 / 6, self.y, 11 * side_x_2 / 6,
                                        2 * side_y_2 + side_z)
            self.to_fix = [(self.x - 2, self.y - 6), (self.x + 15 * side_x_1 / 8 + 6, self.y + 0.8 * side_y_1 - 3),
                        (self.x + 15 * side_x_1 / 8 + 6, self.y + 0.8 * side_y_1 + side_z + 2),
                        (self.x + 7 * side_x_1 / 8 + 1, self.y + 1.8 * side_y_1 + side_z + 7),
                        (self.x - side_x_1 - 6, self.y + side_y_1 + side_z + 4),
                        (self.x - side_x_1 - 6, self.y + side_y_1 - 3)]

        def check_hover(self, mouse_pos):
            self.is_hovered = self.image.collidepoint(mouse_pos)

        def draw_cube(self, surface):
            first = [(self.x, self.y), (self.x + 15 * side_x_1 / 8, self.y + 0.8 * side_y_1),
                    (self.x + 7 * side_x_1 / 8, self.y + 1.8 * side_y_1), (self.x - side_x_1, self.y + side_y_1)]
            second = [(self.x + 15 * side_x_1 / 8, self.y + 0.8 * side_y_1),
                    (self.x + 7 * side_x_1 / 8, self.y + 1.8 * side_y_1),
                    (self.x + 7 * side_x_1 / 8, self.y + 1.8 * side_y_1 + side_z),
                    (self.x + 15 * side_x_1 / 8, self.y + 0.8 * side_y_1 + side_z)]
            third = [(self.x + 7 * side_x_1 / 8, self.y + 1.8 * side_y_1), (self.x - side_x_1, self.y + side_y_1),
                    (self.x - side_x_1, self.y + side_y_1 + side_z),
                    (self.x + 7 * side_x_1 / 8, self.y + 1.8 * side_y_1 + side_z)]
            pygame.draw.polygon(surface, (255, 255, 255), first, width=0)
            pygame.draw.polygon(surface, (200, 200, 200), second, width=0)
            pygame.draw.polygon(surface, (225, 225, 225), third, width=0)
            pygame.draw.polygon(surface, (0, 0, 0), first, width=2)
            pygame.draw.polygon(surface, (0, 0, 0), second, width=2)
            pygame.draw.polygon(surface, (0, 0, 0), third, width=2)
            pygame.draw.polygon(surface, self.color, self.to_fix, 3)

        def draw_fixing(self, surface):
            color = self.color if self.color == (196, 30, 58) else (255, 255, 255)
            cur_color = color if self.is_hovered else self.color
            pygame.draw.polygon(surface, cur_color, self.to_fix, 3)
        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        def draw_point(self, x_coord, y_coord, angle, color, surface):
            target_rect = pygame.Rect((x_coord, y_coord, 14, 9))
            shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size))
            rotated_surf = pygame.transform.rotate(shape_surf, angle)
            surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))
        #left side:
        def one_left(self, surface):
            self.draw_point(self.x - 8, self.y + 93, -25, (0, 0, 0), surface)
        def two_left(self, surface):
            self.draw_point(self.x + 18, self.y + 90, -25, (0, 0, 0), surface)
            self.draw_point(self.x - 34, self.y + 96, -25, (0, 0, 0), surface)
        def three_left(self, surface):
            self.one_left(surface)
            self.two_left(surface)
        def four_left(self, surface):
            self.two_left(surface)
            self.draw_point(self.x + 18, self.y + 121, -25, (0, 0, 0), surface)
            self.draw_point(self.x - 34, self.y + 67, -25, (0, 0, 0), surface)
        def five_left(self, surface):
            self.four_left(surface)
            self.one_left(surface)
        def six_left(self, surface):
            self.four_left(surface)
            self.draw_point(self.x + 18, self.y + 105, -25, (0, 0, 0), surface)
            self.draw_point(self.x - 34, self.y + 81, -25, (0, 0, 0), surface)
        #right side
        def one_right(self, surface):
            self.draw_point(self.x + 53, self.y + 88, 52, (0, 0, 0), surface)

        def two_right(self, surface):
            self.draw_point(self.x + 41, self.y + 84, 52, (0, 0, 0), surface)
            self.draw_point(self.x + 64, self.y + 92, 52, (0, 0, 0), surface)

        def three_right(self, surface):
            self.one_right(surface)
            self.two_right(surface)

        def four_right(self, surface):
            self.two_right(surface)
            self.draw_point(self.x + 41, self.y + 115, 52, (0, 0, 0), surface)
            self.draw_point(self.x + 64, self.y + 60, 52, (0, 0, 0), surface)

        def five_right(self, surface):
            self.four_right(surface)
            self.one_right(surface)

        def six_right(self, surface):
            self.four_right(surface)
            self.draw_point(self.x + 41, self.y + 99, 52, (0, 0, 0), surface)
            self.draw_point(self.x + 64, self.y + 76, 52, (0, 0, 0), surface)
        #main side
        def one_up(self, surface):
            self.draw_point(self.x + 11, self.y + 40, -21, color_up, surface)
            self.five_left(surface)
            self.four_right(surface)
        def two_up(self, surface):
            self.draw_point(self.x + 47, self.y + 38, -21, color_up, surface)
            self.draw_point(self.x - 23, self.y + 42, -21, color_up, surface)
            self.four_left(surface)
            self.one_right(surface)
        def three_up(self, surface):
            self.draw_point(self.x + 11, self.y + 40, -21, color_up, surface)
            self.draw_point(self.x + 47, self.y + 38, -21, color_up, surface)
            self.draw_point(self.x - 23, self.y + 42, -21, color_up, surface)
            self.two_left(surface)
            self.six_right(surface)
        def four_up(self, surface):
            self.draw_point(self.x + 47, self.y + 38, -21, color_up, surface)
            self.draw_point(self.x - 23, self.y + 42, -21, color_up, surface)
            self.draw_point(self.x + 23, self.y + 63, -21, color_up, surface)
            self.draw_point(self.x + 1, self.y + 19, -21, color_up, surface)
            self.six_left(surface)
            self.two_right(surface)
        def five_up(self, surface):
            self.draw_point(self.x + 47, self.y + 38, -21, color_up, surface)
            self.draw_point(self.x - 23, self.y + 42, -21, color_up, surface)
            self.draw_point(self.x + 23, self.y + 63, -21, color_up, surface)
            self.draw_point(self.x + 1, self.y + 19, -21, color_up, surface)
            self.draw_point(self.x + 11, self.y + 40, -21, color_up, surface)
            self.one_left(surface)
            self.three_right(surface)
        def six_up(self, surface):
            self.draw_point(self.x + 47, self.y + 38, -21, color_up, surface)
            self.draw_point(self.x - 23, self.y + 42, -21, color_up, surface)
            self.draw_point(self.x + 23, self.y + 63, -21, color_up, surface)
            self.draw_point(self.x + 1, self.y + 19, -21, color_up, surface)
            self.draw_point(self.x - 10, self.y + 31, -21, color_up, surface)
            self.draw_point(self.x + 35, self.y + 49, -21, color_up, surface)
            self.three_left(surface)
            self.five_right(surface)


    def __init__(self, x_coord, y_coord):
        self.states = random.choice([self.FirstType, self.SecondType, self.ThirdType])(x_coord,y_coord)
        self.x_coord = x_coord
        self.y_coord = y_coord
