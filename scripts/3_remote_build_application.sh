#!/bin/bash

set -euo pipefail

export PATH="${HOME}/miniconda3/bin:${PATH}"
cd "$HOME/zeubor" || exit 1

source "$HOME/miniconda3/etc/profile.d/conda.sh"

conda create -y -p ./env python=3.10
conda init bash
conda activate ./env
env/bin/pip install pygame numpy
env/bin/pip -v install opencv-python
conda install -y pytorch torchvision -c pytorch
