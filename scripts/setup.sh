#!/bin/bash
set -eE -o functrace

failure() {
  local lineno=$1
  local msg=$2
  echo "Failed at $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

set -o pipefail

WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.."

setup_virtualenv(){
  mkdir -pv .venv

  if [[ "$(python3 --version)" == *"Python 3.12"* ]] ; then
    python3 -m venv .venv
  else
    pip3 install --upgrade virtualenv
    python3 -m virtualenv .venv
  fi
}

main(){
  echo "[INFO] Setup development environment"

  uv venv --python 3.12
  uv sync --all-extras
  uv run pre-commit install

  uv run pre-commit run --all-files
}

main "$@"
