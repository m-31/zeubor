#!/bin/bash

set -euo pipefail

export PATH="${HOME}/miniconda3/bin:${PATH}"
cd "$HOME/zeubor" || exit 1

source "$HOME/miniconda3/etc/profile.d/conda.sh"

conda init bash
conda activate ./env
python src/world.py
