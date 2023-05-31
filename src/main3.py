import cv2
import numpy as np

from alga import Alga
from camera import Camera

# Dimensions
WIDTH, HEIGHT = 1500, 1000
FOCAL_LENGTH = 2000
STEP_WIDTH = 0.10  # Distance the camera moves each step

# Generate algae field
algae = [Alga(FOCAL_LENGTH) for _ in range(1000)]

# Camera settings
game_camera = Camera([0.0, 0.0, -FOCAL_LENGTH / 10.0],
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

def introduction():
    """Print instructions on screen and wait for user to press <space>."""
    global image
    # print instructions on screen
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "Use arrow keys to move the camera angle", (10, 30), font, 1, (255, 255, 255), 2)
    cv2.putText(image, "Use left or right arrow key with <SHIFT> to rotate the camera", (10, 60), font, 1, (255, 255, 255), 2)
    cv2.putText(image, "Press <space> to stop or start movement", (10, 90), font, 1, (255, 255, 255), 2)
    cv2.putText(image, "Press <i> or <h> for this instructions", (10, 120), font, 1, (255, 255, 255), 2)
    cv2.putText(image, "Press <space> to start", (10, 150), font, 1, (255, 0, 0), 2)
    draw_algae()
    cv2.imshow('image', image)
    cv2.waitKey(0)
    # Assuming here that some other mechanism would stop the display and return control to the script
    return True

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
        # Move camera
        game_camera.move_in_direction(step_width)
        cv2.imshow('image', image)
    cv2.destroyAllWindows()

introduction()
game()