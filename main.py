import pygame

from alga import Alga
from camera import Camera

# Dimensions
WIDTH, HEIGHT = 1500, 1000
FOCAL_LENGTH = 2000
STEP_WIDTH = 0.10  # Distance the camera moves each step

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


def draw_algae():
    global algae
    for alga in algae:
        projection = game_camera.project_sphere(alga.position, alga.radius)
        if projection is not None:
            pygame.draw.circle(screen, (0, 255, 0), projection[0], projection[1] + 1)


def introduction():
    """Print instructions on screen and wait for user to press <space>."""
    global screen
    # Game loop
    running = True
    start_game = True
    # print instructions on screen
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("Arial", 20)
    text = font.render("Use arrow keys to move the camera", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render("Press <space> to stop or start movement", True, (255, 255, 255))
    screen.blit(text, (10, 40))
    text = font.render("Press <i> or <h> for this instructions", True, (255, 255, 255))
    screen.blit(text, (10, 70))
    text = font.render("Press <space> to start", True, (255, 0, 0))
    screen.blit(text, (10, 120))
    draw_algae()
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_game = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
    return start_game


def game():
    """Main game loop."""
    global game_camera, screen
    clock = pygame.time.Clock()  # Clock to control frame rate

    # Animation settings
    step_width = STEP_WIDTH
    step_angle = 0.002  # Angle the camera rotates when pressing a key

    # Dictionary to keep track of key states
    key_states = {}
    shift_down = False  # Flag to track state of Shift key
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                key_states[event.key] = True
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_SHIFT:
                    shift_down = True
            elif event.type == pygame.KEYUP:
                key_states[event.key] = False
                shift_down = False

            if key_states.get(pygame.K_i) or key_states.get(pygame.K_h):
                running = introduction()
                key_states = {}
                shift_down = False
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if step_width > 0:
                    step_width = 0
                else:
                    step_width = STEP_WIDTH

        screen.fill((0, 0, 0))
        draw_algae()
        pygame.display.flip()

        if key_states.get(pygame.K_LEFT) and not shift_down:
            game_camera.rotate_horizontal(-step_angle)
        elif key_states.get(pygame.K_RIGHT) and not shift_down:
            game_camera.rotate_horizontal(step_angle)
        elif key_states.get(pygame.K_UP):
            game_camera.rotate_vertical(-step_angle)
        elif key_states.get(pygame.K_DOWN):
            game_camera.rotate_vertical(step_angle)
        elif key_states.get(pygame.K_LEFT) and shift_down:
            game_camera.rotate_z(step_angle)
        elif key_states.get(pygame.K_RIGHT) and shift_down:
            game_camera.rotate_z(-step_angle)

        # Move camera
        game_camera.move_in_direction(step_width)

        # Control frame rate
        clock.tick(50)  # Max 50 frames per second


if introduction():
    game()

pygame.quit()
