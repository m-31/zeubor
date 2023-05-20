import random

import numpy as np


class Alga:
    def __init__(self):
        self.position = np.array([random.uniform(-10, 10) for i in range(3)])
        self.radius = random.uniform(1.0, 1.1)
