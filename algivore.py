import cv2
import numpy as np

from alga import Alga
from camera import Camera


class Algivore:
    # Dimensions
    WIDTH, HEIGHT = 100, 100
    FOCAL_LENGTH = 2000
    STEP_WIDTH = 0.10   # Distance the algivore moves each step
    STEP_ANGLE = 0.002  # Angle the algivore rotates when changing direction

    def __init__(self):
        """Initialize algivore."""
        # initialize algae field
        self.algae = [Alga(self.FOCAL_LENGTH) for _ in range(1000)]
        # number of algae eaten
        self.eaten = 0
        # position and orientation
        self.camera = Camera([0.0, 0.0, -self.FOCAL_LENGTH / 10.0],
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

    def create_image_and_detect_collision(self):
        self.image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        """Draw algae on image and detect collisions."""
        algae_to_remove = []
        for alga in self.algae:
            projection = self.camera.project_sphere(alga.position, alga.radius)
            if projection is not None:
                cv2.circle(self.image, (int(projection[0][0]), int(projection[0][1])), int(projection[1]), (0, 255, 0), thickness=-1)
                # detect collision between algivore and algae by checking the distance between them
                if np.linalg.norm(self.camera.position - alga.position) < alga.radius:
                    self.eaten += 1
                    algae_to_remove.append(alga)
        for alga in algae_to_remove:
            self.algae.remove(alga)

    def move(self):
        """Move algivore and eat algae."""
        self.camera.rotate_horizontal(self.delta_x)
        self.camera.rotate_vertical(self.delta_y)
        self.camera.rotate_z(self.delta_z)
        self.camera.move_in_direction(self.speed)

