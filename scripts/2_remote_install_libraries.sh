#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$0")"
BASE_DIR="$(cd "${SCRIPT_DIR}"/.. && pwd)"
. "${SCRIPT_DIR}/config"
. "${SCRIPT_DIR}/_include.sh"


log "Install necessary packages on remote server"
echo "
set -euo pipefail
cd
rm -rf zeubor
mkdir zeubor
cd zeubor
source \"\$HOME/miniconda3/etc/profile.d/conda.sh\"
conda create -y -p ./env python=3.10
conda init bash
conda activate ./env
env/bin/pip install pygame numpy
env/bin/pip -v install opencv-python
conda install -y pytorch torchvision -c pytorch
echo -e '\033[0;32m successfully installed libraries\033[0m'
" | _ssh "bash -s"
