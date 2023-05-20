import pygame
import numpy as np
import random

# Dimensions
WIDTH, HEIGHT = 800, 600

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Ball:
    def __init__(self):
        self.position = np.array([random.uniform(-10, 10) for i in range(3)])

    def project(self, camera_position, focal_length):
        """Project the 3D position onto 2D plane."""
        diff = self.position - camera_position
        z = diff[2]
        if z < 0.1:
            # Object is too close to the camera, return None
            return None
        projected_position = focal_length * (diff / z)
        projected_position = projected_position.astype(int)
        # Return position (shifted to the center of the screen) and size
        return (
            projected_position[0] + WIDTH // 2,
            projected_position[1] + HEIGHT // 2,
            focal_length // z
        )

def init():
    # Generate balls
    global balls
    balls = [Ball() for _ in range(100)]  # 100 balls

    # Camera settings
    global camera_position, focal_length
    camera_position = np.array([0, 0, -20])
    focal_length = 200

def run():
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for ball in balls:
            projection = ball.project(camera_position, focal_length)
            if projection is not None:
                pygame.draw.circle(screen, (255, 255, 255), (projection[0], projection[1]), projection[2])

        pygame.display.flip()

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
