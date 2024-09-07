import sys

def main():
    if len(sys.argv) < 2:
        print("You need a valid input maze file.")
        return -1

    file_name = sys.argv[1]
    print(f"Creating maze with file {file_name}")
    
    # Create the maze
    maze = Maze(file_name)
    
    print("\nUnsolved maze:")
    maze.print_maze()

    # Solve the maze using DFS
    if maze.solve_dfs(maze.start_col, maze.start_row):
        print("\nSolved maze:")
        maze.print_maze()

        # Check if the solution is valid (this method needs to be implemented)
        if check_maze(maze):  # You will need to define check_maze method
            print("Solution to maze is valid")
        else:
            print("Incorrect solution to maze")
    else:
        print("\nMaze is unsolvable")
    
    print("\nDestroying maze")
    
    # Destroy the maze (not really necessary in Python, but can reset attributes if needed)
    maze.destroy()

    return 0

if __name__ == "__main__":
    main()
