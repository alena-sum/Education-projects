import pygame

options = ["ones", "twos", "threes", "fours", "fives", "sixes", "=(+)", "3x", "4x", "3x + 2y", "small street",
           "large street", "general", "chance", "="]

class Table():
    def __init__(self, x_coord, y_coord, width, height, color_fore, color_back):
        self.image_back = pygame.Rect(x_coord - 7, y_coord - 7, width + 14, height + 14)
        self.image_fore = pygame.Rect(x_coord, y_coord, width, height)
        self.color_fore = color_fore
        self.color_back = color_back
        self.x = x_coord
        self.y = y_coord
        self.width = width
        self.height = height
        self.is_hovered = [False] * 15
        self.is_clicked = [False] * 15
        self.is_clicked[6] = True
        self.is_clicked[14] = True
        self.active = False
        self.chosen_points = ["0"] * 16
        self.images = []
        for i in range(1, 16):
            self.images.append(pygame.Rect(x_coord + width // 3, y_coord + i * height // 16, width // 3 + 2, height // 16 + 1))


    def draw(self, user_points, comp_points, surface):
        pygame.draw.rect(surface, self.color_back, self.image_back, 0, 10)
        pygame.draw.rect(surface, self.color_fore, self.image_fore, 0, 10)
        font = pygame.font.SysFont('couriernew', 20)
        text_surface = font.render("Your score", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 32))
        surface.blit(text_surface, text_rect)
        text_surface = font.render("Comp's score", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + 5 * self.width // 6, self.y + self.height // 32))
        surface.blit(text_surface, text_rect)
        if not self.active:
            user_points = self.chosen_points
        for i in range(1, 16):
            width = 2
            if i == 7 or i == 8 or i == 15 or i == 1:
                width = 3
            #options
            text_surface = font.render(options[i - 1], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + self.width // 6, self.y + (2 * i + 1) * self.height // 32))
            surface.blit(text_surface, text_rect)
            #user's points
            cur_color_text = (0, 0, 0) if (i in [7, 15] or not self.is_hovered[i - 1]) else (255, 255, 255)
            cur_color_cell = self.color_fore if (i in [7, 15] or not self.is_hovered[i - 1]) else self.color_back
            pygame.draw.rect(surface, cur_color_cell, self.images[i - 1], 0)
            text_surface = font.render(user_points[i], True, cur_color_text)
            text_rect = text_surface.get_rect(
                center=(self.x + self.width // 2, self.y + (2 * i + 1) * self.height // 32))
            surface.blit(text_surface, text_rect)
            #comp's points
            text_surface = font.render(comp_points[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(self.x + 5 * self.width // 6, self.y + (2 * i + 1) * self.height // 32))
            surface.blit(text_surface, text_rect)
            pygame.draw.line(surface, self.color_back, (self.x + 5, self.y + i * self.height // 16),
                             (self.x + self.width - 5, self.y + i * self.height // 16), width=width)
        pygame.draw.line(surface, self.color_back, (self.x + self.width // 3, self.y + 5),
                         (self.x + self.width // 3, self.y + self.height - 5), width=2)
        pygame.draw.line(surface, self.color_back, (self.x + 2 * self.width // 3, self.y + 5),
                         (self.x + 2 * self.width // 3, self.y + self.height - 5), width=2)

    def check_hover(self, mouse_pos, cell):
        self.is_hovered[cell] = self.images[cell].collidepoint(mouse_pos)

    def handle_event(self, event, cell, value):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered[cell] and not self.is_clicked[cell] and self.active:
            self.is_clicked[cell] = True
            self.chosen_points[cell + 1] = value
            high_sum = sum(int(self.chosen_points[i]) for i in range(1, 7))
            self.chosen_points[7] = str(high_sum if high_sum < 63 else high_sum + 35)
            self.chosen_points[15] = str(sum(int(self.chosen_points[i]) for i in range(7, 15)))
            with open('./source/connection.json', 'w') as f:
                f.write(str(cell + 1) if cell + 1 < 7 else str(cell))
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
