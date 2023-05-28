import cv2
from algivore import Algivore
from trainer import Trainer


def game():
    """Main game loop."""

    # Create an algivore
    algivore = Algivore()

    trainer = Trainer(algivore)

    trainer.train(10000)  # Train for 10000 episodes
    while cv2.waitKey(1) != ord('q'):
        algivore.create_image_and_detect_collision()
        image = algivore.image
        cv2.imshow('image', image)
        algivore.analyze_image_and_set_movements()
        algivore.move()
    cv2.destroyAllWindows()


game()
