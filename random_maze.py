import random
import matplotlib.pyplot as plt
import numpy as np

# Set maze dimensions (width and height)
mx = 20  # Maze width
my = 20  # Maze height

# Initialize the maze with all cells set to 0 (unvisited)
maze = [[0 for x in range(mx)] for y in range(my)]

# Define movement directions: [right, down, left, up]
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]

# Color representation for the maze (black and white in RGB)
color = [(0, 0, 0), (255, 255, 255)]

# Start the maze generation from a random cell
cx = random.randint(0, mx - 1)  # Random starting x-coordinate
cy = random.randint(0, my - 1)  # Random starting y-coordinate
maze[cy][cx] = 1  # Mark the starting cell as visited (1)
stack = [(cx, cy, 0)]  # Stack to hold the position and direction

# Depth-first search (DFS) based maze generation
while len(stack) > 0:
    # Get current position and direction from the top of the stack
    (cx, cy, cd) = stack[-1]

    # Prevent frequent changes in direction to avoid zigzag paths
    if len(stack) > 2:
        if cd != stack[-2][2]:
            dirRange = [cd]  # Limit to the previous direction
        else:
            dirRange = range(4)  # Allow movement in any direction
    else:
        dirRange = range(4)  # In the first moves, allow movement in any direction

    # Find all valid neighboring cells to move into
    nlst = []  # List to store available neighboring cells
    for i in dirRange:
        nx = cx + dx[i]  # Calculate neighboring x-coordinate
        ny = cy + dy[i]  # Calculate neighboring y-coordinate
        # Check if the neighboring cell is within the maze bounds
        if 0 <= nx < mx and 0 <= ny < my:
            if maze[ny][nx] == 0:  # Check if the neighboring cell is unvisited
                ctr = 0  # Counter for the number of occupied neighbors
                for j in range(4):  # Check all 4 neighbors of the current neighbor
                    ex = nx + dx[j]
                    ey = ny + dy[j]
                    # If a neighboring cell is occupied (visited), increment the counter
                    if 0 <= ex < mx and 0 <= ey < my and maze[ey][ex] == 1:
                        ctr += 1
                if ctr == 1:  # Only add the cell if it has exactly one visited neighbor
                    nlst.append(i)

    # If there are available neighbors, pick one randomly and move there
    if len(nlst) > 0:
        ir = nlst[random.randint(0, len(nlst) - 1)]  # Select a random valid direction
        cx += dx[ir]  # Update x-coordinate
        cy += dy[ir]  # Update y-coordinate
        maze[cy][cx] = 1  # Mark the new cell as visited
        stack.append((cx, cy, ir))  # Push the new position onto the stack
    else:
        stack.pop()  # Backtrack if no valid neighbors are available

# Convert the maze list into a NumPy array for further processing
maze = np.array(maze)

# Adjust the maze to set walls as 1 and paths as 0 (invert the values)
maze -= 1
maze = abs(maze)

# Ensure the start and end points are clear (set them as paths)
maze[0][0] = 0  # Start point
maze[mx-1][my-1] = 0  # End point

# Save the generated maze to a file in NumPy format
np.save('maze', np.array(maze))
