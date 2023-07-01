import os

import cv2
import torch

from algivore import Algivore
from net import Net

def game():
    """Main game loop."""

    name = "2023-05-31T12_39_03.864447" # cuda
    # name = "2023-05-30T21_01_13.081814" # cpu
    model_name = f"algivore_{name}"
    #list directory contents
    print(os.listdir("."))

    print(os.listdir("../models"))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = Net()
    net.load_state_dict(torch.load(f"../models/{model_name}.pt", map_location=device))  # load the trained model
    net.to(device)
    net.eval()

    # Create an algivore
    algivore = Algivore(net)

    # Main game loop
    iteration = 1
    while cv2.waitKey(1) != ord('q'):
        algivore.create_image()
        image = algivore.image
        cv2.imshow('image', image)
        algivore.analyze_image_and_set_movements()
        algivore.move()
        eaten = algivore.detect_collision()
        if eaten > 0:
            print(f"{iteration}: eaten {eaten} algae")
        iteration += 1
    cv2.destroyAllWindows()


game()
