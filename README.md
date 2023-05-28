#


## Installation

```bash
conda create -p ./env python=3.10
conda activate ./env
env/bin/pip install pygame numpy
env/bin/pip -v install opencv-python
conda install pytorch torchvision -c pytorch
conda env export > environment.yml
```


https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html