#!/bin/bash

#
# Add required paths to run project code from
# the cli.
#
# Requirements:
# * virtualenvwrapper
# * virtualenv setup using the above
#

. .virtualenv_helper.sh

add_to_pth() {
  local pth_file=$1
  local new_path=$2

  echo "------"

  if [ ! -e "$pth_file" ]; then
    echo "PTH file $pth_file doesn't exist. Creating now..."
    touch "$pth_file"
  fi

  check_present=$(grep -c $new_path $pth_file)

  if [[ $? -eq 2 ]]; then
    echo "Failed to check if path is already set"
    return 1
  elif [[ "$check_present" -gt 0 ]]; then
    echo "PTH file already contains path $new_path  Skipping..."
    return 0
  else
    echo "Adding path $new_path"
    echo "$new_path" >> "$pth_file"
  fi

  return 0
}

if (($VENV)) ; then
  echo "No virtualenv detected. Please enter one before running this."
  exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_MAIN=`readlink -e $SCRIPT_DIR/../`
#TEST_MAIN=`readlink -e $SCRIPT_DIR/../test`

{
  SITE_DIR=`get_site_package_path`
  PTH_FILE="$SITE_DIR/_`get_venv_name`_paths.pth"
} || { echo "Failed to find location for pth file."; exit; }

echo "Source: $SRC_MAIN"
echo "Tests: $TEST_MAIN"

{
  add_to_pth "$PTH_FILE" "$SRC_MAIN"
  #add_to_pth "$PTH_FILE" "$TEST_MAIN"
} || { echo "Failed to add paths. Are you using virtualenvwrapper?"; }

echo ""; echo "Finished adding project paths to virtualenv"
