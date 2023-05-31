import random

import numpy as np


class Alga:
    def __init__(self, focal_length):
        self.position = np.array([random.uniform(-focal_length / 200, focal_length / 200) for i in range(3)])
        self.radius = random.uniform(100 / focal_length, 110 / focal_length)
