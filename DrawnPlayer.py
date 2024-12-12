import pygame

class DrawnPlayer():
    def __init__(self, height, width, maze):
        self.x = 0
        self.y = 0
        self.height = height
        self.width = width
        self.maze = maze

    def get_coordinate(self, coord):
        return coord * 2 + 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN: #and self.active:
            if event.key == pygame.K_DOWN and self.y < self.height - 1 and self.maze[self.get_coordinate(self.y) + 1][self.get_coordinate(self.x)] != " H ":
                self.y += 1
            if event.key == pygame.K_UP and self.y > 0 and self.maze[self.get_coordinate(self.y) - 1][self.get_coordinate(self.x)] != " H ":
                self.y -= 1
            if event.key == pygame.K_RIGHT and self.x < self.width - 1 and self.maze[self.get_coordinate(self.y)][self.get_coordinate(self.x) + 1] != " H ":
                self.x += 1
            if event.key == pygame.K_LEFT and self.x > 0 and self.maze[self.get_coordinate(self.y)][self.get_coordinate(self.x) - 1] != " H ":
                self.x -= 1

