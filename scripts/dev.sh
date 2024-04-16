#!/bin/bash
set -eE -o functrace

failure() {
  local lineno=$1
  local msg=$2
  echo "Failed at $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

set -o pipefail

main(){
  pip3 install --upgrade virtualenv
  mkdir -pv .venv
  python3 -m virtualenv .venv

  # shellcheck disable=SC1091
  source .venv/bin/activate

  pip3 install -r requirements.txt
  pre-commit install
}

main "$@"
