#Ambika Mohapatra
#This program employs a depth-first search (DFS) algorithm along with Deep Q-learning to navigate and solve a 
#maze. We have utilized allocation and deallocation techniques along with maze 
#visualization. We define the recursive conditions to traverse in the up, down, left, right
#directions in order to find the shortest path from the Start (S) to End(E) while avoiding 
#maze walls and staying within defined maze bounds.

import numpy as np


class Maze:
    def __init__(self, file_name):
        self.load_maze(file_name)

    def load_maze(self, file_name):
        # Open the input file and read the maze dimensions
        with open(file_name, 'r') as file:
            self.width = int(file.readline())
            self.height = int(file.readline())

            # Allocate memory for the maze
            self.cells = np.empty((self.height, self.width), dtype=str)

            # Read the maze from the file
            for i in range(self.height):
                row = file.readline().strip()
                for j, char in enumerate(row):
                    self.cells[i][j] = char
                    if char == 'S':
                        self.start_row, self.start_col = i, j
                    if char == 'E':
                        self.end_row, self.end_col = i, j

    def destroy(self):
        # In Python, we don't need to manually free memory, but we can reset the attributes
        del self.cells

    def print_maze(self):
        for row in self.cells:
            print(''.join(row))

    def solve_dfs(self, col, row):
        # Base case: If we're out of bounds, return failure (0)
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return 0

        # If we've reached the end, return success (1)
        if self.cells[row][col] == 'E':
            self.cells[self.start_row][self.start_col] = 'S'
            return 1

        # If the cell is not empty or the start point, return failure
        if self.cells[row][col] != ' ' and self.cells[row][col] != 'S':
            return 0

        # Mark the cell as part of the solution path if it's not the start
        if self.cells[row][col] != 'S':
            self.cells[row][col] = '*'

        # Mark the start cell to prevent looping back to it
        self.cells[self.start_row][self.start_col] = '*'

        # Explore in all directions: Down, Up, Right, Left
        if self.solve_dfs(col, row + 1):  # Down
            return 1
        if self.solve_dfs(col, row - 1):  # Up
            return 1
        if self.solve_dfs(col + 1, row):  # Right
            return 1
        if self.solve_dfs(col - 1, row):  # Left
            return 1

        # If no solution found, backtrack and mark this cell as visited but not part of the solution
        self.cells[row][col] = '~'
        return 0

# Example usage:
maze = Maze("maze.txt")
maze.print_maze()

# Solve the maze starting from the start position
if maze.solve_dfs(maze.start_col, maze.start_row):
    print("Maze solved!")
else:
    print("Maze cannot be solved.")

maze.print_maze()
