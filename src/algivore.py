import cv2
import numpy as np
import torch

from action_space import index_to_action
from alga import Alga
from camera import Camera
from net import Net


class Algivore:
    # Dimensions
    WIDTH, HEIGHT = 100, 100
    FOCAL_LENGTH = 2000
    STEP_WIDTH = 0.10   # Distance the algivore moves each step
    STEP_ANGLE = 0.002  # Angle the algivore rotates when changing direction

    def __init__(self, net):
        """Initialize algivore."""
        # initialize algae field
        self.algae = [Alga(self.FOCAL_LENGTH) for _ in range(9000)]
        # number of algae eaten
        self.eaten = 0
        # position and orientation
        self.camera = Camera([0.0, 0.0, -self.FOCAL_LENGTH / 200.0],
                             [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],  # Pointing towards positive z-axis
                             self.WIDTH, self.HEIGHT,
                             self.FOCAL_LENGTH)
        # change orientation in x direction
        self.delta_x = 0.0
        # change orientation in y direction
        self.delta_y = 0.0
        # change orientation in z direction (turning)
        self.delta_z = 0.0
        # change position in z direction (moving)
        self.speed = self.STEP_WIDTH
        # image to draw on
        self.image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        # neural net
        self.net = net

    def create_image(self):
        """Draw algae on image."""
        self.image.fill(0)
        for alga in self.algae:
            projection = self.camera.project_sphere(alga.position, alga.radius)
            if projection is not None:
                try:
                    cv2.circle(self.image, (int(projection[0][0]), int(projection[0][1])), int(projection[1]), (0, 255, 0), thickness=-1)
                except Exception as exception:
                    print(f"Projection: {projection}\nException: {exception}")

    def detect_collision(self):
        """Detect collisions with algae, a collision means this algivore eats it. returns eaten algae."""
        algae_to_remove = []
        for alga in self.algae:
            projection = self.camera.project_sphere(alga.position, alga.radius)
            if projection is not None:
                if np.linalg.norm(self.camera.position - alga.position) < 5 * alga.radius:  # TODO: reduce to 1 * when working
                    self.eaten += 1
                    algae_to_remove.append(alga)
        result = len(algae_to_remove)
        for alga in algae_to_remove:
            self.algae.remove(alga)
        return result

    def analyze_image_and_set_movements(self):
        # Convert the image to a PyTorch tensor
        image_tensor = torch.from_numpy(self.image).float().unsqueeze(0)  # Add a batch dimension
        image_tensor = image_tensor.permute(0, 3, 1, 2)  # Rearrange dimensions to: batch x channels x height x width
        # Run the image through the model and select action
        with torch.no_grad():
            q_values = self.net(image_tensor)
            action_index = q_values.max(1)[1].item()  # Action with maximum Q-value
        action = index_to_action(action_index)  # Convert action index to action
        self.delta_x, self.delta_y, self.delta_z, self.speed = action

    def move(self):
        """Move algivore and eat algae."""
        # print(f"move deltax, deltay, deltaz, speed: {self.delta_x}, {self.delta_y}, {self.delta_z}, {self.speed}")
        self.camera.rotate_horizontal(self.delta_x * self.STEP_ANGLE)
        self.camera.rotate_vertical(self.delta_y * self.STEP_ANGLE)
        self.camera.rotate_z(self.delta_z * self.STEP_ANGLE)
        self.camera.move_in_direction(self.speed * self.STEP_WIDTH)
        #print(self.camera.position)

