import pygame

class Clock():
    def __init__(self, x_coord, y_coord, width, height, color_fore, color_back):
        self.image_back = pygame.Rect(x_coord - 7, y_coord - 7, width + 14, height + 14)
        self.image_fore = pygame.Rect(x_coord, y_coord, width, height)
        self.color_fore = color_fore
        self.color_back = color_back
        self.color_nums = (178, 132, 106)
        self.x = x_coord
        self.y = y_coord
        self.width = width
        self.height = height
        self.nums_coords = [[x_coord + 2, y_coord], [x_coord + 47, y_coord], [x_coord + 111, y_coord],
                            [x_coord + 156, y_coord]]

    def draw_dash(self, x_coord, y_coord, angle, color, surface):
        target_rect = pygame.Rect((x_coord, y_coord, 27, 6))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size))
        rotated_surf = pygame.transform.rotate(shape_surf, angle)
        surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))
    def universal(self, surface, pos, colors):
        x, y = self.nums_coords[pos]
        self.draw_dash(x + 18, y + 8, 0, colors[0], surface)
        self.draw_dash(x + 32, y + 24, 90, colors[1], surface)
        self.draw_dash(x + 32, y + 55, 90, colors[2], surface)
        self.draw_dash(x + 18, y + 40, 0, colors[3], surface)
        self.draw_dash(x + 5, y + 24, 90, colors[4], surface)
        self.draw_dash(x + 5, y + 55, 90, colors[5], surface)
        self.draw_dash(x + 18, y + 71, 0, colors[6], surface)
    def zero(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col1, col1, col1, col2, col1, col1, col1])
    def one(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col2, col1, col1, col2, col2, col2, col2])
    def two(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col1, col1, col2, col1, col2, col1, col1])

    def three(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col1, col1, col1, col1, col2, col2, col1])

    def four(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col2, col1, col1, col1, col1, col2, col2])

    def five(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col1, col2, col1, col1, col1, col2, col1])

    def six(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col1, col2, col1, col1, col1, col1, col1])

    def seven(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col1, col1, col1, col2, col2, col2, col2])

    def eight(self, surface, pos):
        col1 = self.color_back
        self.universal(surface, pos, [col1, col1, col1, col1, col1, col1, col1])

    def nine(self, surface, pos):
        col1, col2 = self.color_back, self.color_nums
        self.universal(surface, pos, [col1, col1, col1, col1, col1, col2, col1])
    def choose(self, num, pos, surface):
        if num == 0: self.zero(surface, pos)
        if num == 1: self.one(surface, pos)
        if num == 2: self.two(surface, pos)
        if num == 3: self.three(surface, pos)
        if num == 4: self.four(surface, pos)
        if num == 5: self.five(surface, pos)
        if num == 6: self.six(surface, pos)
        if num == 7: self.seven(surface, pos)
        if num == 8: self.eight(surface, pos)
        if num == 9: self.nine(surface, pos)
    def draw(self, surface, cur_time):
        pygame.draw.rect(surface, self.color_back, self.image_back, 0, 10)
        pygame.draw.rect(surface, self.color_fore, self.image_fore, 0, 10)
        pygame.draw.rect(surface, self.color_back, (self.x + self.width // 2 - 4, self.y + self.height // 4, 9, 9),
                         0, 2)
        pygame.draw.rect(surface, self.color_back, (self.x + self.width // 2 - 4, self.y + 3 * self.height // 4 - 10,
                                                    9, 9), 0, 2)
        time = [(cur_time // 60) // 10, (cur_time // 60) % 10, (cur_time % 60) // 10, (cur_time % 60) % 10]
        for i in range(4):
            self.choose(time[i], i, surface)

