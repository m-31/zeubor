import cv2
from algivore import Algivore


def game():
    """Main game loop."""

    # Create an algivore
    algivore = Algivore()

    while cv2.waitKey(1) != ord('q'):
        algivore.create_image_and_detect_collision()
        image = algivore.image
        cv2.imshow('image', image)
        algivore.move()
    cv2.destroyAllWindows()


game()
