import pygame
import config

class DrawnLabirint():
    def __init__(self, labirint, width, height, color_fore1, color_fore2, color_fore3, solution):
        self.height = height
        self.width = width
        self.maze = labirint
        self.sol = solution
        self.coefficient = min((config.WIDTH - config.SPACE_X) // width, (config.HEIGHT - config.SPACE_Y) // height)
        self.col_fore1 = color_fore1
        self.col_fore2 = color_fore2
        self.col_fore3 = color_fore3
        self.x = (config.WIDTH - width * self.coefficient - config.SPACE_X) / 2
        self.y = (config.HEIGHT - height * self.coefficient) / 2
    def draw_cell(self, surface, x_coord, y_coord, col):
        pygame.draw.rect(surface, col, (x_coord, y_coord, self.coefficient, self.coefficient), 0)
    def draw(self, surface):
        for i in range(self.height):
            for j in range(self.width):
                cur_color = self.col_fore1
                if self.maze[i][j] == ' H ':
                    cur_color = self.col_fore1
                else:
                    cur_color = self.col_fore2
                self.draw_cell(surface, self.x + self.coefficient * j, self.y + self.coefficient * i,
                               cur_color)

    def draw_solution(self, surface):
        for i in range(self.height):
            for j in range(self.width):
                cur_color = self.col_fore3
                if self.sol[i][j] == ' H ':
                    cur_color = self.col_fore1
                elif self.sol[i][j] == '   ':
                    cur_color = self.col_fore2
                else:
                    cur_color = self.col_fore3
                self.draw_cell(surface, self.x + self.coefficient * j, self.y + self.coefficient * i,
                               cur_color)

    def draw_solve(self, surface, pos_x, pos_y):
        for i in range(self.height):
            for j in range(self.width):
                cur_color = self.col_fore3
                if self.maze[i][j] == ' H ':
                    cur_color = self.col_fore1
                else:
                    cur_color = self.col_fore2
                if i == pos_y and j == pos_x:
                    cur_color = self.col_fore3
                self.draw_cell(surface, self.x + self.coefficient * j, self.y + self.coefficient * i,
                               cur_color)


