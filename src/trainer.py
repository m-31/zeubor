import copy
import json
import os
import platform
import random
from datetime import datetime
import numpy as np
import torch
from torch import nn, optim
import torch.nn.functional as F

from src.action_space import action_space
from src.algivore import Algivore
from replay_memory import ReplayMemory, Transition


def write_info(file_path, training_info, add_separator):
    _, ext = os.path.splitext(file_path)
    with open(file_path, 'a') as f:
        if ext == '.txt' and add_separator:
            f.write('-' * 80 + '\n')
        if ext == '.json':
            info = dict()
            for key, value in training_info.items():
                if type(value) in [int, float, bool, str]:
                    info[key] = value
                else:
                    info[key] = str(value)
            json.dump(info, f, indent=2)
            f.write("\n")
        elif ext == '.txt':
            f.write(f"{training_info['timestamp']}\n")
            for key, value in training_info.items():
                if key != 'timestamp':
                    f.write(f"  {key}: {value}\n")


class Trainer:
    def __init__(self, net, memory_size=10000, batch_size=64, target_update=10, gamma=0.99, lr=0.01):
        self.max_eaten = None
        self.start_time = None
        self.end_time = None
        self.memory = ReplayMemory(memory_size)
        self.batch_size = batch_size
        self.target_update = target_update
        self.gamma = gamma

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = net.to(self.device)  # Q-Network
        self.target_net = copy.deepcopy(self.net).to(self.device)  # Target Network
        self.optimizer = optim.Adam(self.net.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

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

    def train(self, episodes, steps=1000):
        self.max_eaten = 0
        self.start_time = datetime.now()
        for episode in range(episodes):
            print(f'Episode {episode}')
            algivore = Algivore(self.net)
            self.optimizer.zero_grad()

            for step in range(steps):
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
                    self.max_eaten = max(self.max_eaten, algivore.eaten)
                    print(f'  Done after {step} steps, eaten {algivore.eaten} algae')
                    break

            if episode % self.target_update == 0:  # Update the target network every TARGET_UPDATE episodes
                self.target_net.load_state_dict(self.net.state_dict())
        self.end_time = datetime.now()
        print()
        print(f'Max eaten: {self.max_eaten}')
        print('-' * 80)
        timestamp = datetime.now().isoformat()
        model_name = f"algivore_{timestamp.replace(':', '_')}"
        torch.save(self.net.state_dict(), f"./models/{model_name}.pt")  # Save the trained model

        # Information about the training
        info = {
            "timestamp": timestamp,
            "episodes": episodes,
            "steps": steps,
            "max_eaten": self.max_eaten,
            "duration": self.end_time - self.start_time,
            "model": f"{model_name}.pt",
            "machine": platform.machine(),
            "processor": platform.processor(),
            "system": platform.system(),
            "platform": platform.platform(),
            "node": platform.node(),
        }
        # setting device on GPU if available, else CPU
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        info["device"] = device
        if device.type == 'cuda':
            info["cuda_device"] = torch.cuda.get_device_name(0)
            info["cuda_allocated"] = round(torch.cuda.memory_allocated(0) / 1024 ** 3, 1)  # GB
            info["cuda_cached"] = round(torch.cuda.memory_reserved(0) / 1024 ** 3, 1)  # GB

        # Append information about the trained model to the respective files
        write_info(f"./models/{model_name}.json", info, False)
        write_info('./models/algivore_info.txt', info, True)
