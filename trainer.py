import copy
import random
import torch
from torch import nn, optim
import torch.nn.functional as F

from net import Net
from replay_memory import ReplayMemory, Transition


class Trainer:
    def __init__(self, algivore, memory_size=10000, batch_size=64, target_update=10, gamma=0.99, lr=0.01):
        self.algivore = algivore
        self.memory = ReplayMemory(memory_size)
        self.batch_size = batch_size
        self.target_update = target_update
        self.gamma = gamma

        self.algivore.net = Net()  # Q-Network
        self.algivore.target_net = copy.deepcopy(self.algivore.net)  # Target Network
        self.optimizer = optim.Adam(self.algivore.net.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def select_action(self, state):
        # Implement an epsilon-greedy strategy
        epsilon = 0.1  # Exploration rate
        if random.random() < epsilon:
            # Explore: choose a random action
            action = torch.tensor(
                [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 1)])
        else:
            # Exploit: choose the action with the highest Q-value
            with torch.no_grad():
                q_values = self.algivore.net(state)
                action = q_values[0]

        return action

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            # Not enough experiences in memory, so return
            return

        # Sample a batch of experiences from memory
        transitions = self.memory.sample(self.batch_size)
        batch = Transition(*zip(*transitions))

        # Compute the current Q-value estimates
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        q_values = self.algivore.net(state_batch)
        q_values = q_values.gather(1, action_batch.unsqueeze(1))

        # Compute the target Q-values
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
        next_q_values = torch.zeros(self.batch_size)
        next_q_values[non_final_mask] = self.algivore.target_net(non_final_next_states).max(1)[0].detach()
        target_q_values = batch.reward + (self.gamma * next_q_values)

        # Compute the loss between the current and target Q-values
        loss = F.mse_loss(q_values, target_q_values.unsqueeze(1))

        # Update the Q-network weights
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def train(self, episodes):
        for episode in range(episodes):
            self.optimizer.zero_grad()

            self.algivore.create_image_and_detect_collision()
            state = torch.from_numpy(self.algivore.image).float().unsqueeze(0)  # Add a batch dimension
            state = state.permute(0, 3, 1, 2)  # Rearrange dimensions to: batch x channels x height x width

            action = self.select_action(state)
            self.algivore.delta_x, self.algivore.delta_y, self.algivore.delta_z, self.algivore.speed = action.tolist()
            self.algivore.move()

            next_state = torch.from_numpy(self.algivore.image).float().unsqueeze(0)  # Add a batch dimension
            next_state = next_state.permute(0, 3, 1, 2)  # Rearrange dimensions to: batch x channels x height x width
            reward = self.algivore.eaten  # The reward is the number of algae eaten
            done = False  # You would need to determine when an episode is done

            self.memory.push(state, action, next_state, reward, done)
            self.optimize_model()

            if episode % self.target_update == 0:  # Update the target network every TARGET_UPDATE episodes
                self.algivore.target_net.load_state_dict(self.algivore.net.state_dict())
