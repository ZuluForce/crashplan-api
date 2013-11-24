#!/bin/bash

SCRIPT_DIR=`dirname $0`

# ==== Python Bytecode Files ==== #
echo "Deleting Python bytecode files"
[[ "$SCRIPT_DIR" != "" ]] && \
  find "$SCRIPT_DIR/../" -type f -name *.pyc -print -exec rm '{}' \;
