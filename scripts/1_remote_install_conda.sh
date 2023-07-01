#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$0")"
BASE_DIR="$(cd "${SCRIPT_DIR}"/.. && pwd)"
. "${SCRIPT_DIR}/config"
. "${SCRIPT_DIR}/_include.sh"

log "Install conda on remote server"

echo "
set -euo pipefail
cd
wget -O Miniconda3-latest-Linux-x86_64.sh 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh'
rm -rf miniconda3
bash Miniconda3-latest-Linux-x86_64.sh -b -u -p miniconda3
echo -e '\033[0;32m successfully installed miniconda3\033[0m'
" | _ssh "bash -s"