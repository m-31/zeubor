import pygame
import numpy as np
import random

# Dimensions
WIDTH, HEIGHT = 2000, 1200

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Ball:
    def __init__(self):
        self.position = np.array([random.uniform(-10, 10) for i in range(3)])
        self.radius = random.uniform(0.1, 1)

    def project(self, camera_position, focal_length):
        """Project the 3D position onto 2D plane."""
        diff = self.position - camera_position
        z = diff[2]
        projected_radius = int(self.radius * focal_length / abs(z))
        projected_position = focal_length * (diff / z) if z != 0 else diff
        projected_position = projected_position.astype(int)

        xp, yp = projected_position[0] + WIDTH // 2, projected_position[1] + HEIGHT // 2

        # If the ball is too close or the photo plate is completely inside the ball, cover the photo plate
        if abs(z) < self.radius or projected_radius > np.sqrt((WIDTH // 2) ** 2 + (HEIGHT // 2) ** 2):
            return (-WIDTH // 2, -HEIGHT // 2, max(WIDTH, HEIGHT))

        # If the ball doesn't touch the photo plate at all, return None
        if xp + projected_radius < -WIDTH // 2 or xp - projected_radius > WIDTH // 2 or yp + projected_radius < -HEIGHT // 2 or yp - projected_radius > HEIGHT // 2:
            return None

        # Return position and size
        return xp, yp, projected_radius


# Generate balls
balls = [Ball() for _ in range(1000)]  # 100 balls

# Camera settings
camera_position = np.array([0, 0, -20])
focal_length = 200

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
