import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import copy

class MazeEnvironment:
    def __init__(self, maze, init_position, goal):
        rows = len(maze)
        cols = len(maze)
        
        self.boundary = np.array([rows, cols])
        self.init_position = init_position
        self.current_position = np.array(init_position)
        self.goal = goal
        self.maze = maze
        
        self.visited = set()
        self.visited.add(tuple(self.current_position))
        
        # Identify empty cells and calculate Euclidean distance from the goal (excluding the goal itself)
        self.allowed_states = np.transpose(np.where(self.maze == 0)).tolist()
        self.distances = np.linalg.norm(np.array(self.allowed_states) - np.array(self.goal), axis=1)
        
        goal_index = np.where(self.distances == 0)[0][0]
        del self.allowed_states[goal_index]
        self.distances = np.delete(self.distances, goal_index)
        
        self.action_map = {0: [0, 1], 1: [0, -1], 2: [1, 0], 3: [-1, 0]}
        self.directions = {0: '→', 1: '←', 2: '↓', 3: '↑'}
        
        # Agent actions: 0 -> right, 1 -> left, 2 -> down, 3 -> up
    
    # A reset strategy that places the agent closer to the goal at high epsilon values
    def reset_policy(self, eps, reg=7):
        scaling = (reg * (1 - eps**(2/reg)))**(reg / 2)
        return sp.softmax(-self.distances / scaling).squeeze()
    
    # Reset environment with random resets or by following the reset policy
    def reset(self, epsilon, prand=0):
        if np.random.rand() < prand:
            idx = np.random.choice(len(self.allowed_states))
        else:
            p = self.reset_policy(epsilon)
            idx = np.random.choice(len(self.allowed_states), p=p)
        
        self.current_position = np.array(self.allowed_states[idx])
        self.visited = set()
        self.visited.add(tuple(self.current_position))
        
        return self.state()
    
    # Update the environment state based on agent's action
    def state_update(self, action):
        game_active = True
        reward = -0.05  # Penalty for each move
        
        move = self.action_map[action]
        next_position = self.current_position + np.array(move)
        
        # Reward of 1 if the goal is reached
        if np.array_equal(self.current_position, self.goal):
            reward = 1
            game_active = False
            return [self.state(), reward, game_active]
        
        # Penalty if the cell has been visited
        if tuple(self.current_position) in self.visited:
            reward = -0.2
        
        # Penalty if the move is invalid (out of bounds or hits a wall)
        if self.is_state_valid(next_position):
            self.current_position = next_position
        else:
            reward = -1
        
        self.visited.add(tuple(self.current_position))
        return [self.state(), reward, game_active]
    
    # Return the current state for the network input
    def state(self):
        state_copy = copy.deepcopy(self.maze)
        state_copy[tuple(self.current_position)] = 2
        return state_copy
    
    # Check if the position is within the maze boundaries
    def check_boundaries(self, position):
        out_of_bounds = any(pos < 0 for pos in position) or any(pos >= bound for pos, bound in zip(position, self.boundary))
        return out_of_bounds
    
    # Check if the position contains a wall
    def check_walls(self, position):
        return self.maze[tuple(position)] == 1
    
    # Verify if the next position is valid
    def is_state_valid(self, next_position):
        return not (self.check_boundaries(next_position) or self.check_walls(next_position))
    
    # Visualize the maze and save the current state
    def draw(self, filename):
        plt.figure()
        plt.imshow(self.maze, interpolation='none', aspect='equal', cmap='Greys')
        ax = plt.gca()
        
        plt.xticks([], [])
        plt.yticks([], [])
        
        ax.plot(self.goal[1], self.goal[0], 'bs', markersize=4)
        ax.plot(self.current_position[1], self.current_position[0], 'rs', markersize=4)
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
