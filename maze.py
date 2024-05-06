import pygame
import random
import colors
from cell import Cell

# pygame setup
pygame.init()


class Maze:
    def __init__(self):
        self.screen_width: int = 600
        self.screen_height: int = 600
        self.cell_size: int = 30

        self.rows: int = self.screen_width // self.cell_size
        self.cols: int = self.screen_height // self.cell_size

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running: bool = True
        self.clock = pygame.time.Clock()

        self.grid = [[Cell(x * self.cell_size, y * self.cell_size, self.cell_size) for x in range(self.cols)]
                     for y in range(self.rows)]

        self.current_cell = self.grid[0][0]
        self.stack: list[object] = []

        self.start = self.grid[0][random.randint(0, self.cols - 1)]
        self.end = self.grid[self.rows - 1][random.randint(0, self.cols - 1)]

    def display(self) -> None:

        self.screen.fill(colors.bg_color)  # Remplissage de l'écran en noir

        for row in range(self.rows):  # Boucle sur les lignes en premier

            for col in range(self.cols):  # Boucle sur les colonnes ensuite

                self.grid[row][col].draw(self.screen)

                if self.current_cell and not self.maze_complete():
                    pygame.draw.rect(self.screen,
                                     colors.blue_color,
                                     pygame.Rect(self.current_cell.x + 1, self.current_cell.y + 1,
                                                 self.cell_size, self.cell_size))

                if self.maze_complete():

                    if self.grid[row][col] == self.start:
                        pygame.draw.circle(self.screen,
                                           colors.green_color,
                                           (self.grid[row][col].x + self.cell_size // 2,
                                            self.grid[row][col].y + self.cell_size // 2),
                                           self.cell_size // 4)  # Dessiner un cercle au centre de la cellule

                    if self.grid[row][col] == self.end:
                        pygame.draw.circle(self.screen,
                                           colors.red_color,
                                           (self.grid[row][col].x + self.cell_size // 2,
                                            self.grid[row][col].y + self.cell_size // 2),
                                           self.cell_size // 4)  # Dessiner un cercle au centre de la cellule

        pygame.display.flip()  # Actualisation de l'écran

    def handling_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running: bool = False

    def update(self) -> None:

        self.current_cell.is_visited = True

        self.current_cell.check_neighbors(self.current_cell, self.grid)

        next_cell = self.current_cell.next_cell(self.current_cell, self.current_cell.neighbors, self.grid, self.stack)

        if next_cell is not None:
            self.current_cell = next_cell
        else:
            if self.stack:
                self.current_cell = self.stack.pop()

    def maze_complete(self) -> bool:
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].is_visited:
                    return False
        return True

    def run(self) -> None:
        while self.running:

            self.handling_events()
            self.display()
            self.update()
            self.clock.tick(60)


fen = Maze()
fen.run()
pygame.quit()
