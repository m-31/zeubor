#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$0")"
BASE_DIR="$(cd "${SCRIPT_DIR}"/.. && pwd)"
. "${SCRIPT_DIR}/config"
. "${SCRIPT_DIR}/_include.sh"

cd "${SCRIPT_DIR}" || exit 1


./1_remote_install_conda.sh
./2_remote_install_libraries.sh
./3_copy_to_remote.sh
./4_remote_execute_application.sh

echo "TODO Copy results from remote server"

log "That's all folks!"
