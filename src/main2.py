import numpy as np
import cv2

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


def draw_algae():
    global algae

    # Create a black image (numpy array)
    #img = np.zeros((512, 512, 3), np.uint8)

    # Draw a blue circle on it. The arguments are the image, the center point, the radius, the color (BGR), and the thickness (-1 for filled circle)
    #cv2.circle(img, (256, 256), 50, (255, 0, 0), -1)

    img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    for alga in algae:
        projection = game_camera.project_sphere(alga.position, alga.radius)
        if projection is not None:
            cv2.circle(img, (int(round(projection[0][0])), round(int(projection[0][1]))), int(projection[1] + 1),
                       (0, 255, 0), -1)
    return img

img = draw_algae()

cv2.imshow('image', img)
cv2.imwrite('image.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
