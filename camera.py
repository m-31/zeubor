import numpy as np

class Camera:
    def __init__(self, position, x, y, z, width, height, focal_length):
        self.position = np.array(position)
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        self.width = width
        self.height = height
        self.focal_length = focal_length

    def rotate(self, theta, v1, v2):
        ct = np.cos(theta)
        st = np.sin(theta)

        vn = v1 * ct + v2 * st
        v2[:] = v2 * ct - v1 * st
        v1[:] = vn

    def rotate_horizontal(self, angle):
        self.rotate(angle, self.x, self.z)
        self.check()

    def rotate_vertical(self, angle):
        self.rotate(angle, self.y, self.z)
        self.check()

    def get_rotation_matrix(self):
        return np.column_stack((self.x, self.y, self.z))

    def move_in_direction(self, step):
        self.position += step * self.z
        self.check()


    def check(self):
        """Check if x, y, z are orthogonal."""
        assert np.linalg.norm(np.cross(self.x, self.y) - self.z) < 1e-10
        assert np.linalg.norm(np.cross(self.y, self.z) - self.x) < 1e-10
        assert np.linalg.norm(np.cross(self.z, self.x) - self.y) < 1e-10
        assert np.abs(np.linalg.norm(self.x) - 1) < 1e-10
        assert np.abs(np.linalg.norm(self.y) - 1) < 1e-10
        assert np.abs(np.linalg.norm(self.z) - 1) < 1e-10