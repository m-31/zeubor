#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$0")"
BASE_DIR="$(cd "${SCRIPT_DIR}"/.. && pwd)"
. "${SCRIPT_DIR}/config"
. "${SCRIPT_DIR}/_include.sh"

log "Execute application on remote server"
_ssh -t "set -eu && source miniconda3/etc/profile.d/conda.sh && cd zeubor && conda init bash && conda activate ./env && python src/world.py"

echo "TODO Copy results from remote server"

log "That's all folks!"
