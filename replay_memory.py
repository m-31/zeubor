import random
from collections import namedtuple

import torch

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward', 'done'))


class ReplayMemory:

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        # Modify the reward to be a tensor before saving the transition
        state, action, next_state, reward, done = args
        reward = torch.tensor([reward], device=self.device)

        assert 0 <= action < 54, f'Action {action} out of bounds!'  # TODO, remove if running

        self.memory[self.position] = Transition(state, action, next_state, reward, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
