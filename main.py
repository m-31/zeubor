import pygame
import numpy as np
import random

# Dimensions
WIDTH, HEIGHT = 1500, 1000

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def rotation_matrix_from_vectors(vec1, vec2):
    """Find the rotation matrix that aligns vec1 to vec2."""
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    if s < 1e-10:  # vectors are parallel
        return np.eye(3) if c > 0 else -np.eye(3)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2 + 1e-10))
    return rotation_matrix

class Ball:
    def __init__(self):
        self.position = np.array([random.uniform(-10, 10) for i in range(3)])
        self.radius = random.uniform(1.0, 1.1)

    def project(self, camera_position, camera_direction, focal_length):
        """Project the 3D position onto 2D plane."""
        rotation_matrix = rotation_matrix_from_vectors(np.array([0, 0, 1]), camera_direction)
        rotated_position = rotation_matrix.dot(self.position - camera_position)
        z = rotated_position[2]

        if z < -self.radius:
            # The ball is entirely behind the photo plate
            return None

        if z < self.radius:
            # The ball intersects with the photo plate
            intersection_radius = np.sqrt(self.radius ** 2 - z ** 2)
            projected_radius = int(intersection_radius * focal_length / abs(z))
        else:
            # The ball is entirely in front of the photo plate
            projected_radius = int(self.radius * focal_length / abs(z))

        projected_position = focal_length * (rotated_position / z) if z != 0 else rotated_position
        projected_position = projected_position.astype(int)

        xp, yp = projected_position[0] + WIDTH // 2, projected_position[1] + HEIGHT // 2

        return (xp, yp, projected_radius)

# Generate balls
balls = [Ball() for _ in range(100)]  # 100 balls

# Camera settings
camera_position = np.array([0.0, 0.0, -20])
camera_direction = np.array([0.0, 0.0, 1.0])  # Pointing towards positive z-axis
focal_length = 200

# Animation settings
step_width = 0.01  # Distance the camera moves each step
clock = pygame.time.Clock()  # Clock to control frame rate

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    number = 0
    for ball in balls:
        number += 1
        projection = ball.project(camera_position, camera_direction, focal_length)
        if projection is not None:
            pygame.draw.circle(screen, (255, 255, 255 - 1 * number), (projection[0], projection[1]), projection[2])
        else:
            print("Ball " + str(number) + " is too far away or too close to the camera.")

    pygame.display.flip()

    # Move camera
    camera_position += step_width * camera_direction / np.linalg.norm(camera_direction)

    # Control frame rate
    clock.tick(50)  # Max 50 frames per second

pygame.quit()
