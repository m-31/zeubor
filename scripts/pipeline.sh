#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$0")"
BASE_DIR="$(cd "${SCRIPT_DIR}"/.. && pwd)"
. "${SCRIPT_DIR}/config"
. "${SCRIPT_DIR}/_include.sh"

cd "${SCRIPT_DIR}" || exit 1

echo "Copy sources to remote server"
./1_copy_to_remote.sh

echo "Install conda on remote server"
_ssh "bash -s" < ./2_remote_install_conda.sh

echo "Build application on remote server"
_ssh "bash -s" < ./3_remote_build_application.sh

echo "Execute application on remote server"
_ssh "bash -s" < ./4_remote_execute_application.sh

echo "TODO Copy results from remote server"

echo "That's all folks!"
