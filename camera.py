import numpy as np


class Camera:
    def __init__(self, position, direction, width, height, focal_length):
        self.position = np.array(position)
        self.direction = np.array(direction)
        self.width = width
        self.height = height
        self.focal_length = focal_length

    def rotate_horizontal(self, angle):
        rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]])
        self.direction = np.dot(rotation_matrix, self.direction)

    def rotate_vertical(self, angle):
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]])
        self.direction = np.dot(rotation_matrix, self.direction)