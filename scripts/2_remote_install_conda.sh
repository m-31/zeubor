#!/bin/bash

set -euo pipefail

cd "$HOME" || exit 1
wget -O Miniconda3-latest-Linux-x86_64.sh "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
rm -rf "$HOME/miniconda3"
bash Miniconda3-latest-Linux-x86_64.sh -b -u -p "$HOME/miniconda3"
