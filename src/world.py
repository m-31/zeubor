import cv2

from algivore import Algivore
from net import Net
from trainer import Trainer


def game():
    """Main game loop."""

    net = Net()
    trainer = Trainer(net)
    print("Training...")
    # TODO: goal: trainer.train(10000)  # Train for 10000 episodes
    trainer.train(1)  # Train for 1 episodes
    # trainer.train(10000)

    exit(0)     # no GUI on server

    # Create an algivore
    algivore = Algivore(net)

    print("Starting main loop...")
    # Main game loop
    while cv2.waitKey(1) != ord('q'):
        algivore.create_image()
        image = algivore.image
        cv2.imshow('image', image)
        algivore.analyze_image_and_set_movements()
        algivore.move()
        eaten = algivore.detect_collision()
        if eaten > 0:
            print(f"Eaten {eaten} algae")
    cv2.destroyAllWindows()


game()
