import pygame
import random
import colors
from cell import Cell

# pygame setup
pygame.init()


class Maze:
    def __init__(self):
        self.screen_width: int = 800
        self.screen_height: int = 800
        self.cell_size: int = 40

        self.rows: int = self.screen_width // self.cell_size
        self.cols: int = self.screen_height // self.cell_size

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running: bool = True
        self.clock = pygame.time.Clock()

        self.grid = [[Cell(x * self.cell_size, y * self.cell_size, self.cell_size) for x in range(self.cols)]
                     for y in range(self.rows)]

        self.current_cell: Cell = self.grid[0][0]
        self.stack: list[Cell] = []

        self.start: Cell = self.grid[0][random.randint(0, self.cols - 1)]
        self.end: Cell = self.grid[self.rows - 1][random.randint(0, self.cols - 1)]

        self.explored_stack: list[Cell] = []
        self.explore_cell: Cell = self.start

        # For test
        # random.seed(10)

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

                    if self.explore_cell:
                        pygame.draw.rect(self.screen,
                                         colors.blue_color,
                                         pygame.Rect(self.explore_cell.x + 1, self.explore_cell.y + 1,
                                                     self.cell_size, self.cell_size))

        pygame.display.flip()  # Actualisation de l'écran

    def handling_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running: bool = False

    def update(self) -> None:

        if not self.maze_complete():

            self.current_cell.is_visited = True

            self.current_cell.check_neighbors(self.current_cell, self.grid)

            next_cell: Cell = self.current_cell.next_cell(self.current_cell,
                                                          self.current_cell.neighbors, self.grid, self.stack)

            if next_cell is not None:
                self.current_cell = next_cell
            else:
                if self.stack:
                    self.current_cell = self.stack.pop()

        else:
            self.find_exit()

    def maze_complete(self) -> bool:
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].is_visited:
                    return False
        return True

    def find_exit(self) -> None:
        row, col = self.explore_cell.y // self.cell_size, self.explore_cell.x // self.cell_size

        paths: list = self.check_path_possibilities()

        not_explored: list = [path for path in paths if not path.is_explored]

        if self.explore_cell != self.end:

            self.explore_cell.is_explored = True

            if not_explored:
                if col + 1 < self.cols and self.grid[row][col + 1] in not_explored:
                    next_explore = self.grid[row][col + 1]
                else:
                    next_explore = random.choice(not_explored)

                self.explored_stack.append(self.explore_cell)

                self.explore_cell = next_explore

            else:
                self.explore_cell = self.explored_stack[-1]
                self.explored_stack.pop()

    def check_path_possibilities(self) -> list:

        row, col = self.explore_cell.y // self.cell_size, self.explore_cell.x // self.cell_size

        paths: list = []

        # Vérifier les cellules voisines pour déterminer les options de déplacement
        if not self.explore_cell.walls["right"] and col + 1 < self.cols:
            paths.append(self.grid[row][col + 1])

        if not self.explore_cell.walls["top"] and row > 0:
            paths.append(self.grid[row - 1][col])

        if not self.explore_cell.walls["left"] and col > 0:
            paths.append(self.grid[row][col - 1])

        if not self.explore_cell.walls["bottom"] and row + 1 < self.rows:
            paths.append(self.grid[row + 1][col])

        return paths

    def run(self) -> None:
        while self.running:

            self.handling_events()
            self.display()
            self.update()
            self.clock.tick(60)


fen: Maze = Maze()
fen.run()
pygame.quit()
