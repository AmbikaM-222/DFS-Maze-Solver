import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import copy
import torch
import torch.nn as nn
import torch.optim as optim
import collections

# Define a transition named tuple
Transition = collections.namedtuple('Experience',
                                    field_names=['state', 'action',
                                                 'next_state', 'reward',
                                                 'is_game_on'])

class Agent:
    def __init__(self, maze, memory_buffer, use_softmax=True):
        self.env = maze  # The Maze class from the first code
        self.buffer = memory_buffer  # This is a reference to an external memory buffer
        self.num_act = 4  # Four possible actions (up, down, left, right)
        self.use_softmax = use_softmax  # Whether to use softmax policy or epsilon-greedy
        self.total_reward = 0  # Initialize total reward
        self.min_reward = -self.env.cells.size  # Set a minimum reward based on the maze size
        self.isgameon = True  # Game status flag

    # Function to make a move in the maze environment
    def make_a_move(self, net, epsilon, device='cuda'):
        action = self.select_action(net, epsilon, device)  # Select an action based on the policy
        current_state = self.env.state()  # Get the current state of the maze
        next_state, reward, self.isgameon = self.env.state_update(action)  # Update the state after the move
        self.total_reward += reward  # Update the total reward

        if self.total_reward < self.min_reward:  # Check if the reward goes below a threshold
            self.isgameon = False  # End the game if the reward is too low
        if not self.isgameon:
            self.total_reward = 0  # Reset reward if the game ends

        # Store the transition (experience) in the memory buffer
        transition = Transition(current_state, action, next_state, reward, self.isgameon)
        self.buffer.push(transition)

    # Function to select an action based on the policy (epsilon-greedy or softmax)
    def select_action(self, net, epsilon, device='cuda'):
        state = torch.Tensor(self.env.state()).to(device).view(1, -1)  # Get the current state as a tensor
        qvalues = net(state).cpu().detach().numpy().squeeze()  # Get Q-values from the neural network

        # If softmax is being used, sample actions based on softmax of Q-values
        if self.use_softmax:
            p = sp.softmax(qvalues / epsilon).squeeze()
            p /= np.sum(p)
            action = np.random.choice(self.num_act, p=p)
        # Else, use epsilon-greedy action selection
        else:
            if np.random.random() < epsilon:
                action = np.random.randint(self.num_act, size=1)[0]  # Random action with probability epsilon
            else:
                action = np.argmax(qvalues, axis=0)  # Best action with probability 1-epsilon
                action = int(action)

        return action

    # Function to plot the policy map based on Q-values from the neural network
    def plot_policy_map(self, net, filename, offset):
        net.eval()  # Set the network to evaluation mode
        with torch.no_grad():
            fig, ax = plt.subplots()
            ax.imshow(self.env.cells, 'Greys')  # Plot the maze using matplotlib

            # Loop through all allowed (free) cells
            for free_cell in self.env.allowed_states:
                self.env.current_position = np.asarray(free_cell)  # Set current position to the free cell
                qvalues = net(torch.Tensor(self.env.state()).view(1, -1).to('cuda'))  # Get Q-values
                action = int(torch.argmax(qvalues).detach().cpu().numpy())  # Choose the best action
                policy = self.env.directions[action]  # Get the direction of the action

                ax.text(free_cell[1] - offset[0], free_cell[0] - offset[1], policy)  # Mark the policy on the plot

            ax = plt.gca()
            plt.xticks([], [])
            plt.yticks([], [])

            # Mark the goal on the plot
            ax.plot(self.env.end_col, self.env.end_row, 'bs', markersize=4)
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.show()
