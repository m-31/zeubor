import pygame

from alga import Alga
from camera import Camera

# Dimensions
WIDTH, HEIGHT = 1500, 1000
FOCAL_LENGTH = 2000

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Generate algae field
algae = [Alga(FOCAL_LENGTH) for _ in range(1000)]

# Camera settings
game_camera = Camera([0.0, 0.0, -FOCAL_LENGTH / 10.0],
                     [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],  # Pointing towards positive z-axis
                     WIDTH, HEIGHT,
                     FOCAL_LENGTH)


# Animation settings
step_width = 0.10  # Distance the camera moves each step
step_angle = 0.01  # Angle the camera rotates when pressing a key

clock = pygame.time.Clock()  # Clock to control frame rate

# Game loop
running = True

# Dictionary to keep track of key states
key_states = {}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            key_states[event.key] = False

    screen.fill((0, 0, 0))
    for alga in algae:
        # projection = project(alga.position, alga.radius, game_camera)
        # if projection is not None:
        #     pygame.draw.ellipse(screen, (0, 255, 0),
        #                         pygame.Rect(projection[0] - projection[2] // 2, projection[1] - projection[3] // 2,
        #                                     projection[2], projection[3]))
        projection = game_camera.project_sphere(alga.position, alga.radius)
        if projection is not None:
            pygame.draw.circle(screen, (0, 255, 0), projection[0], projection[1] + 1)

    pygame.display.flip()

    # Rotate camera based on key states
    if key_states.get(pygame.K_LEFT):
        game_camera.rotate_horizontal(-step_angle)
    if key_states.get(pygame.K_RIGHT):
        game_camera.rotate_horizontal(step_angle)
    if key_states.get(pygame.K_UP):
        game_camera.rotate_vertical(-step_angle)
    if key_states.get(pygame.K_DOWN):
        game_camera.rotate_vertical(step_angle)

    # Move camera
    game_camera.move_in_direction(step_width)

    print(game_camera.position, game_camera.z)

    # Control frame rate
    clock.tick(50)  # Max 50 frames per second

pygame.quit()
