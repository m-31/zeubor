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

    def project_sphere(self, sphere_position, sphere_radius):
        # Step 1: Translate the point
        translated_position = np.array(sphere_position) - self.position

        # Step 2: Convert to the camera's coordinate system
        camera_coords_position = self.get_rotation_matrix().T @ translated_position

        # Check if the sphere is behind the camera
        if camera_coords_position[2] <= 0:
            return None

        # Step 3: Perform the perspective projection transformation
        # We perform the division only for the x and y coordinates
        projected_x = self.focal_length * (camera_coords_position[0] / camera_coords_position[2])
        projected_y = self.focal_length * (camera_coords_position[1] / camera_coords_position[2])

        # Calculate the projected radius of the sphere using the formula discussed above
        projected_radius = (self.focal_length / camera_coords_position[2]) * sphere_radius

        # The final 2D coordinates of the sphere's center and its radius
        return (projected_x + self.width / 2, projected_y + self.height / 2), abs(projected_radius)

    def check(self):
        """Check if x, y, z are orthogonal."""
        assert np.linalg.norm(np.cross(self.x, self.y) - self.z) < 1e-10
        assert np.linalg.norm(np.cross(self.y, self.z) - self.x) < 1e-10
        assert np.linalg.norm(np.cross(self.z, self.x) - self.y) < 1e-10
        assert np.abs(np.linalg.norm(self.x) - 1) < 1e-10
        assert np.abs(np.linalg.norm(self.y) - 1) < 1e-10
        assert np.abs(np.linalg.norm(self.z) - 1) < 1e-10