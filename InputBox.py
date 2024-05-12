import pygame

class InputBox():
    def __init__(self,  x_coord, y_coord, width, height, color_fore_active, color_fore_inactive, color_back, text=''):
        self.image_fore = pygame.Rect(x_coord, y_coord, width, height)
        self.image_back = pygame.Rect(x_coord - 3, y_coord - 3, width + 6, height + 6)
        self.text = text
        self.active_color = color_fore_active
        self.inactive_color = color_fore_inactive
        self.color_back = color_back
        self.active = False
        self.is_hovered = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_back, self.image_back, 0)
        cur_color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(surface, cur_color, self.image_fore, 0)
        cur_text_color = self.inactive_color if self.active else self.active_color
        font = pygame.font.SysFont('couriernew', 25)
        txt_surface = font.render(self.text, True, cur_text_color)
        text_rect = txt_surface.get_rect(center=self.image_fore.center)
        surface.blit(txt_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.image_fore.collidepoint(mouse_pos)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE and self.text != '':
                self.text = self.text[:-1]
            elif (event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                               pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9] and  1 <=
                  int(self.text + event.unicode) <= 150):
                self.text += event.unicode
