import random
import pygame


class Cell:
    def __init__(self, x: int, y: int, cell_size: int):
        self.x: int = x
        self.y: int = y
        self.cell_size: int = cell_size
        self.walls: dict = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.isVisited: bool = False
        self.neighbors: list[object] = []

    def draw(self, screen) -> None:
        if self.walls['top']:
            pygame.draw.line(screen,
                             (255, 255, 255),
                             (self.x, self.y),
                             (self.x + self.cell_size, self.y),
                             2)
        if self.walls['right']:
            pygame.draw.line(screen,
                             (255, 255, 255),
                             (self.x + self.cell_size, self.y),
                             (self.x + self.cell_size, self.y + self.cell_size),
                             2)
        if self.walls['bottom']:
            pygame.draw.line(screen,
                             (255, 255, 255),
                             (self.x + self.cell_size, self.y + self.cell_size),
                             (self.x, self.y + self.cell_size),
                             2)
        if self.walls['left']:
            pygame.draw.line(screen,
                             (255, 255, 255),
                             (self.x, self.y + self.cell_size),
                             (self.x, self.y),
                             2)

        if self.isVisited:
            pygame.draw.rect(screen,
                             (255, 0, 255),
                             pygame.Rect(self.x + 1, self.y + 1, self.cell_size, self.cell_size))

        # for neighbor in self.neighbors:
        #     pygame.draw.rect(screen,
        #                      (0, 0, 255),
        #                      pygame.Rect(neighbor.x, neighbor.y, self.cell_size, self.cell_size))

    def remove_wall(self, wall: dict) -> None:
        self.walls[wall] = False

    def check_neighbors(self, current_cell, grid) -> None:

        self.neighbors: list[object] = []

        row, col = current_cell.y // self.cell_size, current_cell.x // self.cell_size

        # Top
        if row > 0:
            top = grid[row - 1][col]
            self.neighbors.append(top)

        # Left
        if col > 0:
            left = grid[row][col - 1]
            self.neighbors.append(left)

        # Right
        if col < len(grid[row]) - 1:
            right = grid[row][col + 1]
            self.neighbors.append(right)

        # Bottom
        if row < len(grid) - 1:
            bottom = grid[row + 1][col]
            self.neighbors.append(bottom)

    def next_cell(self, current_cell, neighbors, grid, stack: list[object]):

        row, col = current_cell.y // self.cell_size, current_cell.x // self.cell_size

        unvisited_neighbors = [neighbor for neighbor in neighbors if not neighbor.isVisited]

        # The neighbor chosen become the current cell
        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            # Top
            if row > 0 and next_cell == grid[row - 1][col]:
                # Remove the top wall
                current_cell.remove_wall('top')
                next_cell.remove_wall('bottom')

            # Left
            elif col > 0 and next_cell == grid[row][col - 1]:
                # Remove the left wall
                current_cell.remove_wall('left')
                next_cell.remove_wall('right')

            # Right
            elif col < len(grid[row]) - 1 and next_cell == grid[row][col + 1]:
                # Remove the right wall
                current_cell.remove_wall('right')
                next_cell.remove_wall('left')

            # Bottom
            elif row < len(grid) - 1 and next_cell == grid[row + 1][col]:
                # Remove the bottom wall
                current_cell.remove_wall('bottom')
                next_cell.remove_wall('top')

            stack.append(current_cell)
            return next_cell

        elif stack:
            return stack.pop()

        else:
            return None
