# Zeubor

## Description
Artificial creatures living in a simulated world.

The creatures are controlled by neural nets. The three-dimensional environment is full of algae, the creatures are algivores that eat all the algae. To accomplish this the algivore gets a visual picture of the environment, that is an image of all algae in its visual field. The algivore can move one step forward (speed), turn left (x-delta) for a certain degree, turn right (y-delta) for a certain degree or turn around the visual axe (z-delta) for a certain degree. If the algivore touches an alga it gets eaten. Thus, the neural net of the algivore must try to get one in the image projection big algae (big means nearby) into the center of it's vision to move towards it and eventually eat it.

If the neural net is good, the algivore can eat all the algae. Its quality can be measured how fast it eats algae. 


## History
This project is a revival of a previous (2015) Java project that produced some videos like these:

[![artificial neural net Dido eats algae (neuron input fire shown)](https://img.youtube.com/vi/67bmCxAf7Z4/0.jpg)](https://www.youtube.com/watch?v=67bmCxAf7Z4)

[![artificial neural net Dido eats algae](https://img.youtube.com/vi/gOjHac_wn5s/0.jpg)](https://www.youtube.com/watch?v=gOjHac_wn5s)

[![eight artificial neural nets fight for algae (neuron input fire shown)](https://img.youtube.com/vi/sZgOu3N5F78/0.jpg)](https://www.youtube.com/watch?v=sZgOu3N5F78)


## Current Implementation

The current implementation uses Deep Q-Learning (DQN). 

We use a reinforcement learning system where an AI agent (the 'algivore') moves in a 3D environment, interacts with objects (the 'algae'), and learns to optimize its behavior through repeated interactions. The agent's view of the environment is simulated through a camera perspective, and the learning mechanism uses a convolutional neural network trained using Q-learning. The objective for the AI agent is to consume as many algae as possible.

| File             | Description                                                                                                                                                                                                                                                                                              |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| action_space.py  | This script defines an action space consisting of possible movements along three dimensions (dx, dy, dz) and two possible speeds (0,1). The script also provides functions to map actions to indices and vice versa.                                                                                     |
| alga.py          | This script creates a class Alga, where each instance represents an alga object with a position in the 3D environment and a radius. The position is initialized randomly within a certain range relative to a focal length parameter.                                                                    |
| algivore.py      | This script creates a class Algivore, where each instance represents an algivore object that can interact with the algae. The algivore can move in the environment, detect collisions with algae (i.e., eat algae), and use a neural network to analyze its current state and decide on its next action. |
| camera.py        | This script creates a Camera class that handles the perspective from the algivore's point of view, including its position and orientation, and the projection of the 3D world onto a 2D image                                                                                                            |
| net.py           | This script defines a convolutional neural network class (Net) which can process the algivore's current state (in the form of an image) and output Q-values for possible actions. The network is constructed using PyTorch                                                                               |
| replay_memory.py | This script defines a replay memory, which is a data structure used in reinforcement learning to store past experiences that the model can learn from.                                                                                                                                                   |
| trainer.py       | This script defines a class for training the neural network based on interactions in the environment. It uses Q-learning, an algorithm commonly used in reinforcement learning, and it also includes an epsilon-greedy strategy for action selection to balance exploration and exploitation.            |



## Installation

```bash
conda create -p ./env python=3.10
conda activate ./env
env/bin/pip install pygame numpy
env/bin/pip -v install opencv-python
conda install pytorch torchvision -c pytorch
conda env export > environment.yml
```

----

https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

### list all python files without main*.py

```bash
for f in *.py; do if [[ ! $f == main* ]]; then echo "=== $f ==="; cat $f; fi; done > result.txt
```

## TODO

### normalize the input to float:

- algae within the sphere around (0, 0, 0) with radius 1


### run remotely on lambda service to use GPU


### use SAC neural net
