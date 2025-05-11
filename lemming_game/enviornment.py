import random
# import copy
import numpy as np

MAZE_BANK = {
    "simple": np.array([
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '.', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '#', '.', '#', '.', '.', '#', '.'],
        ['#', '#', '.', '#', '.', '#', '.', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.'],
        ['.', '#', '#', '#', '#', '#', '.', '#', '.', '#'],
        ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.'],
        ['.', '#', '#', '#', '#', '#', '.', '#', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', 'G'],
    ]),

    "bottleneck": np.array([
        ['.', '#', '.', '.', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '.', '#', '#', '#', '#', '.', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '#', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '.', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '#', '.', '#', '.', '.', '.'],
        ['#', '#', '#', '.', '#', '.', '#', '#', '#', '#'],
        ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', 'G'],
    ]),

    "open_trap": np.array([
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '#', '#', '#', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '.', '#', '#', '#', '#', '.', '#', '.'],
        ['.', '#', '.', '#', '.', '.', '#', '.', '#', '.'],
        ['.', '#', '.', '#', '.', '#', '#', '.', '#', '.'],
        ['.', '#', '.', '#', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '.', '#', '#', '#', '#', '#', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', 'G'],
    ])
}


class Lemming:

    def __init__(self, name, maze):
        self.name = name
        self.maze = maze
        self.rows = np.shape(maze)[0]
        self.columns = np.shape(maze)[1]
        self.present_pos = self.spawn_initial_pos()

    def check_pos(self, pos):
        x, y = pos

        # Check bounds
        if x < 0 or x >= self.rows or y < 0 or y >= self.columns:
            return False

        # Check for wall or goal square
        if self.maze[x][y] == '#':
            return False

        return True
    
    def spawn_initial_pos(self):
        while True:
            pos = (random.randint(0, self.rows - 1), random.randint(0, self.columns - 1))
            if self.check_pos(pos):
                return pos
            
    def step(self, action):

        response = {
            'action': False,
            'next_pos': self.present_pos
        }

        x, y = self.present_pos

        delta = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1) #,
            # optional
            # 'stay': (0, 0)
        }

        if action not in delta:
            return response
        
        dx, dy = delta[action]

        x, y = x + dx, y + dy

        next_pos = x, y

        if self.check_pos(next_pos):
            self.present_pos = next_pos
            response['action'] = True
            response['next_pos'] = next_pos
            

        return response
    
    def to_dict(self):
        return {'name': self.name, 'present_pos': self.present_pos}
    
    def __repr__(self):
        return f"Lemming(name={self.name}, pos={self.present_pos})"
    

class Game:

    def __init__(self, maze, num_lemmings=2, max_episodes=100):

        # Initialize the Game.
        self.maze = maze
        self.num_lemmings = num_lemmings
        self.terminated = False
        self.truncated = False
        self.episode_number = 0   
        self.max_episodes = max_episodes 



    def reset(self):
        # spawn num_lemmings
        self.lemmings = [Lemming(str(i), self.maze) for i in range(self.num_lemmings)]
        # set episodic reward array
        self.rewards = np.zeros((1, self.num_lemmings))
        # Reset Episode Number to Zero
        self.episode_number = 0

        return self.get_state()
    
    def get_state(self):
        states = [self.lemmings[i].to_dict()['present_pos'] for i in range(self.num_lemmings)]
        return states
    
    def step(self, actions):
        
        
        try:
            assert len(actions) == self.num_lemmings

        except AssertionError as e:
            print(f'Number of Actions ({len(actions)}) does not equal {self.num_lemmings}')
            return('AssertionError')
        
        prev_positions = [lemming.present_pos for lemming in self.lemmings]

        # Calculate Rewards
        rewards = [-1.0] * len(self.lemmings)
        
        # Move all lemmings
        for i in range(self.num_lemmings):
            result = self.lemmings[i].step(actions[i])
            # If a lemming collides with a wall, penalize with a reward of -10.0
            if not result['action']:
                rewards[i] = -10.0

        next_state = self.get_state()
        self.episode_number += 1
        
        

        # Collision check (non-goal): penalize lemmings for collisions.
        current_positions = [lem.present_pos for lem in self.lemmings]
        if len(set(current_positions)) < len(current_positions):
            for i in range(self.num_lemmings):
                if current_positions.count(current_positions[i]) > 1 and current_positions[i] != (9, 9):
                    self.lemmings[i].present_pos = prev_positions[i]
                    rewards[i] -= 5  # penalty for overlap



        self.terminated = self.is_terminated()
        self.truncated = self.is_truncated()

        # If termination & rewards occur together, provide a reward of 500.0
        if self.terminated and self.truncated:
            rewards = [500.0] * self.num_lemmings

        # successful termination also provides a reward of 500.0
        elif self.terminated:
            rewards = [500.0] * self.num_lemmings

        # truncated episodes provide a penalty of -50.0
        elif self.truncated:
            rewards = [-50.0] * self.num_lemmings

        

        info = {
            'episode': self.episode_number,
            'positions': self.get_state(),
            'terminated': self.terminated,
            'truncated': self.truncated
        }

        return rewards, next_state, self.terminated, self.truncated, info
    
    # An episode Terminates if both lemmings reach the goal simaltaneously.
    def is_terminated(self):
        return all(lemming.present_pos == (9,9) for lemming in self.lemmings)
    
    # An episode truncates if the number of episodes goes beyond the limit set by max_episodes. Default for max_episodes is 500.
    def is_truncated(self):
        return self.episode_number >= self.max_episodes
    
    def get_action_space(self):
        return ['up', 'down', 'left', 'right']
    
    # create random actions for all lemmings.
    def sample_actions(self):
        action_space = self.get_action_space()

        return [random.choice(action_space) for _ in range(self.num_lemmings)]
    
    # Function to print the lemming positional map onto a terminal. 
    def render(self):
        view = self.maze.copy().tolist()
        position_map = {}

        # Mark each lemming's position, avoid overlap unless on goal
        for lemming in self.lemmings:
            x, y = lemming.present_pos
            key = (x, y)

            if key in position_map:
                position_map[key].append(lemming.name)
            else:
                position_map[key] = [lemming.name]

        # Apply markings
        for (x, y), names in position_map.items():
            if len(names) == 1:
                view[x][y] = names[0]
            else:
                view[x][y] = 'X'  # Overlap — optional: ''.join(names)[:2]

        # Print view
        print("\n" + "-" * 25)
        for row in view:
            print(" ".join(row))
        print("-" * 25 + "\n")


    
