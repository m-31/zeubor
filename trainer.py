import copy
import random

import cv2
import numpy as np
import torch
from torch import nn, optim
import torch.nn.functional as F

from action_space import action_space
from algivore import Algivore
from replay_memory import ReplayMemory, Transition


class Trainer:
    def __init__(self, net, memory_size=10000, batch_size=64, target_update=10, gamma=0.99, lr=0.01):
        self.memory = ReplayMemory(memory_size)
        self.batch_size = batch_size
        self.target_update = target_update
        self.gamma = gamma

        self.net = net  # Q-Network
        self.target_net = copy.deepcopy(self.net)  # Target Network
        self.optimizer = optim.Adam(self.net.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def select_action(self, state):
        epsilon = 0.1  # Exploration rate
        if random.random() < epsilon:
            # Define probabilities for each action, speed == 1 is 50 times more likely than speed == 0
            action_probabilities = []
            for action in action_space:
                if action[3] == 0:
                    action_probabilities.append(1 / (50 * 27 + 27))
                else:
                    action_probabilities.append(50 / (50 * 27 + 27))
            action_index = np.random.choice(len(action_space),
                                            p=action_probabilities)  # Random action with given probabilities
        else:
            with torch.no_grad():
                state = state.to(self.device)
                q_values = self.net(state)
                action_index = q_values.max(1)[1].item()  # Action with maximum Q-value

        return action_index

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        transitions = self.memory.sample(self.batch_size)
        batch = Transition(*zip(*transitions))  # Unzips the transitions to Transition of batches

        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                                batch.next_state)), device=self.device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state
                                           if s is not None])

        state_batch = torch.cat(batch.state)
        action_batch = torch.tensor(batch.action, device=self.device)
        reward_batch = torch.tensor(batch.reward, device=self.device).float()

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken
        state_action_values = self.net(state_batch).gather(1, action_batch.unsqueeze(1))

        # Compute V(s_{t+1}) for all next states.
        next_state_values = torch.zeros(self.batch_size, device=self.device)
        next_state_values[non_final_mask] = self.net(non_final_next_states).max(1)[0].detach()

        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self.gamma) + reward_batch

        # Compute Huber loss
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def train(self, episodes):
        for episode in range(episodes):
            print(f'Episode {episode}')
            algivore = Algivore(self.net)
            self.optimizer.zero_grad()

            for step in range(1000):
                # print(f'  Step {step}')
                algivore.create_image()
                state = torch.from_numpy(algivore.image).float().unsqueeze(0).to(self.device)  # Add a batch dimension
                state = state.permute(0, 3, 1, 2)  # Rearrange dimensions to: batch x channels x height x width

                action = self.select_action(state)

                action_values = action_space[action]  # Retrieve the action from the action space
                algivore.delta_x, algivore.delta_y, algivore.delta_z, algivore.speed = list(action_values)
                algivore.move()
                newly_eaten = algivore.detect_collision()
                if newly_eaten > 0:
                    print(f'  {step}: eaten {newly_eaten} algae')
                # if cv2.waitKey(1) != ord('q'):
                #     cv2.imshow('image', algivore.image)
                # else:
                #     cv2.destroyAllWindows()

                next_state = torch.from_numpy(algivore.image).float().unsqueeze(0).to(
                    self.device)  # Add a batch dimension
                next_state = next_state.permute(0, 3, 1,
                                                2)  # Rearrange dimensions to: batch x channels x height x width
                reward = newly_eaten * 10  # The reward is the number of algae eaten
                if np.linalg.norm(algivore.camera.position) > algivore.FOCAL_LENGTH / 200.0:
                    reward -= 100  # Punish the algivore for going too far away from the origin
                    print('  Punished for going too far away from the origin')
                done = reward < 0 or step >= 1000 - 1

                self.memory.push(state, action, next_state, reward, done)
                self.optimize_model()

                if done:
                    print(f'  Done after {step} steps, eaten {algivore.eaten} algae')
                    break

            if episode % self.target_update == 0:  # Update the target network every TARGET_UPDATE episodes
                self.target_net.load_state_dict(self.net.state_dict())
