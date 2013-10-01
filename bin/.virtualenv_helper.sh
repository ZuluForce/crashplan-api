#!/bin/bash

# VENV = 0 (if no virtualenv) VENV=1 (if in virtualenv)
[[ "$VIRTUAL_ENV" != "" ]]; export VENV=$?


function get_site_package_path() {
  dirs=`find $VIRTUAL_ENV -name site-packages`

  if [[ "${#dirs[@]}" -eq 0 ]]; then
    echo "No site package found for virtualenv" 1>&2
    return 1
  fi

  echo "${dirs[0]}"
  return 0
}

function get_venv_name() {
  echo "${VIRTUAL_ENV##*/}"
}

