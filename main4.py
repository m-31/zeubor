import cv2
import numpy as np

from alga import Alga
from camera import Camera

# Dimensions
WIDTH, HEIGHT = 100, 100
FOCAL_LENGTH = 2000
STEP_WIDTH = 0.10   # Distance the algivore moves each step

# Generate algae field
algae = [Alga(FOCAL_LENGTH) for _ in range(9000)]

# Camera settings
game_camera = Camera([0.0, 0.0, -FOCAL_LENGTH / 50.0],
                     [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],  # Pointing towards positive z-axis
                     WIDTH, HEIGHT,
                     FOCAL_LENGTH)

# Create an image
image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

def draw_algae():
    global algae
    for alga in algae:
        projection = game_camera.project_sphere(alga.position, alga.radius)
        if projection is not None:
            cv2.circle(image, (int(projection[0][0]), int(projection[0][1])), int(projection[1]), (0, 255, 0), thickness=-1)

def game():
    """Main game loop."""
    global game_camera, image
    # Animation settings
    step_width = STEP_WIDTH
    step_angle = 0.002  # Angle the camera rotates when pressing a key

    # Create an image

    # Some mechanism would be needed here to capture key events and adjust the camera

    while cv2.waitKey(1) != ord('q'):
        image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        draw_algae()
        game_camera.move_in_direction(step_width)
        cv2.imshow('image', image)
    cv2.destroyAllWindows()

game()