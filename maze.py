import pygame
import random
import colors
from cell import Cell

# pygame setup
pygame.init()


class Maze:
    def __init__(self):
        self.SCREEN_WIDTH: int = 800
        self.SCREEN_HEIGHT: int = 800
        self.CELL_SIZE: int = 40

        self.ROWS: int = self.SCREEN_WIDTH // self.CELL_SIZE
        self.COLS: int = self.SCREEN_HEIGHT // self.CELL_SIZE

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running: bool = True
        self.clock = pygame.time.Clock()

        self.grid = [[Cell(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE) for x in range(self.COLS)]
                     for y in range(self.ROWS)]

        self.current_cell: Cell = self.grid[0][0]
        self.stack: list[Cell] = []

        self.explore_cell: Cell = self.grid[0][random.randint(0, self.COLS - 1)]
        self.end: Cell = self.grid[self.ROWS - 1][random.randint(0, self.COLS - 1)]

        self.explored_stack: list[Cell] = []

        # For test
        # random.seed(10)

    def display(self) -> None:

        self.screen.fill(colors.BG_COLOR)  # Remplissage de l'écran en noir

        for row in range(self.ROWS):  # Boucle sur les lignes en premier

            for col in range(self.COLS):  # Boucle sur les colonnes ensuite

                self.grid[row][col].draw(self.screen)

                if self.current_cell and not self.maze_complete():
                    pygame.draw.rect(self.screen,
                                     colors.BLUE_COLOR,
                                     pygame.Rect(self.current_cell.x + 1, self.current_cell.y + 1,
                                                 self.CELL_SIZE, self.CELL_SIZE))

                if self.maze_complete():

                    if self.grid[row][col] == self.end:
                        pygame.draw.circle(self.screen,
                                           colors.RED_COLOR,
                                           (self.grid[row][col].x + self.CELL_SIZE // 2,
                                            self.grid[row][col].y + self.CELL_SIZE // 2),
                                           self.CELL_SIZE // 4)  # Dessiner un cercle au centre de la cellule

                    if self.explore_cell:
                        pygame.draw.rect(self.screen,
                                         colors.BLUE_COLOR,
                                         pygame.Rect(self.explore_cell.x + 1, self.explore_cell.y + 1,
                                                     self.CELL_SIZE, self.CELL_SIZE))

        pygame.display.flip()  # Actualisation de l'écran

    def handling_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running: bool = False

    def update(self) -> None:

        if not self.maze_complete():

            self.current_cell.is_visited = True

            self.current_cell.check_neighbors(self.grid)

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
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if not self.grid[row][col].is_visited:
                    return False
        return True

    def find_exit(self) -> None:
        row, col = self.explore_cell.get_cell_coordinates()

        paths: list = self.check_path_possibilities()

        not_explored: list = [path for path in paths if not path.is_explored]

        if self.explore_cell != self.end:

            self.explore_cell.is_explored = True

            if not_explored:
                if col + 1 < self.COLS and self.grid[row][col + 1] in not_explored:
                    next_explore = self.grid[row][col + 1]
                else:
                    next_explore = random.choice(not_explored)

                self.explored_stack.append(self.explore_cell)

                self.explore_cell = next_explore

            else:
                self.explore_cell = self.explored_stack[-1]
                self.explored_stack.pop()

    def check_path_possibilities(self) -> list:

        row, col = self.explore_cell.get_cell_coordinates()

        paths: list = []

        # Vérifier les cellules voisines pour déterminer les options de déplacement
        if not self.explore_cell.walls["right"] and col + 1 < self.COLS:
            paths.append(self.grid[row][col + 1])

        if not self.explore_cell.walls["top"] and row > 0:
            paths.append(self.grid[row - 1][col])

        if not self.explore_cell.walls["left"] and col > 0:
            paths.append(self.grid[row][col - 1])

        if not self.explore_cell.walls["bottom"] and row + 1 < self.COLS:
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
