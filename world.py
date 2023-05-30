from datetime import datetime

import cv2
import torch

from algivore import Algivore
from net import Net
from trainer import Trainer


def game():
    """Main game loop."""

    net = Net()
    trainer = Trainer(net)

    # TODO: goal: trainer.train(10000)  # Train for 10000 episodes
    trainer.train(100)  # Train for 100 episodes

    torch.save(net.state_dict(), f"algivore_{datetime.now().isoformat().replace(':', '_')}.pt")  # Save the trained model

    # Create an algivore
    algivore = Algivore(net)

    # Main game loop
    while cv2.waitKey(1) != ord('q'):
        algivore.create_image()
        image = algivore.image
        cv2.imshow('image', image)
        algivore.analyze_image_and_set_movements()
        algivore.move()
        if algivore.detect_collision() > 0:
            print(f"Eaten {algivore.detect_collision()} algae")
    cv2.destroyAllWindows()


game()
