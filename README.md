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

### list all python files without main*.py

```bash
for f in *.py; do if [[ ! $f == main* ]]; then echo "=== $f ==="; cat $f; fi; done > result.txt
```

Projection: ((5808032238.387375, -4091067353.1002054), 21923655.165025793)
Exception: OpenCV(4.7.0) :-1: error: (-5:Bad argument) in function 'circle'
> Overload resolution failed:
>  - Can't parse 'center'. Sequence item with index 0 has a wrong type
>  - Can't parse 'center'. Sequence item with index 0 has a wrong type

Episode 25
Projection: ((7300494533.319192, 2348668838.2530236), 30287512.15543457)
Exception: OpenCV(4.7.0) :-1: error: (-5:Bad argument) in function 'circle'
> Overload resolution failed:
>  - Can't parse 'center'. Sequence item with index 0 has a wrong type
>  - Can't parse 'center'. Sequence item with index 0 has a wrong type

Projection: ((36743079287.07832, 8554433331.05296), 164586943.52009797)
Exception: OpenCV(4.7.0) :-1: error: (-5:Bad argument) in function 'circle'
> Overload resolution failed:
>  - Can't parse 'center'. Sequence item with index 0 has a wrong type
>  - Can't parse 'center'. Sequence item with index 0 has a wrong type

## TODO

### normalize the input to float:

- algae within the sphere around (0, 0, 0) with radius 1


### run remotely on lambda service to use GPU


### use SAC neural net
