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

main(){
  echo "## Setup: global project deps"

  cd "${WORKDIR}"

  mkdir -pv .venv

  if [[ "$(python3 --version)" == *"Python 3.12"* ]] ; then
    python3 -m venv .venv
  else
    pip3 install --upgrade virtualenv
    python3 -m virtualenv .venv
  fi

  # shellcheck disable=SC1091
  source .activate

  pip3 install -r requirements.txt
  pre-commit install
}

main "$@"
