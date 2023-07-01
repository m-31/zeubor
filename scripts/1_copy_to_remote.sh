#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$0")"
BASE_DIR="$(cd "${SCRIPT_DIR}"/.. && pwd)"
. "${SCRIPT_DIR}/config"
. "${SCRIPT_DIR}/_include.sh"

cd "${BASE_DIR}" || exit 1

# Define the name of the archive file
ARCHIVE_NAME="${PROJECT}.tar.gz"

# Create the tar.gz archive of the current directory
tar -czvf "/tmp/${ARCHIVE_NAME}" --exclude .git --exclude .idea --exclude env --exclude __pycache__ --exclude models .

# Copy the tar.gz archive to the remote server
_scp "/tmp/$ARCHIVE_NAME"

# Remove any existing directory with the same name on the remote server
# shellcheck disable=SC2029
_ssh "rm -rf ${PROJECT}"

# Extract the tar.gz archive on the remote server
# shellcheck disable=SC2029
_ssh "mkdir ${PROJECT} && tar --warning=no-unknown-keyword -xzvf ${ARCHIVE_NAME} -C ${PROJECT}"

# Remove the tar.gz archive from the remote server after extraction
# shellcheck disable=SC2029
_ssh "rm ${ARCHIVE_NAME}"

# Remove local tar.gz archive
rm "/tmp/${ARCHIVE_NAME}"

echo "Successfully copied ${PROJECT} to ${REMOTE_SERVER}!"
