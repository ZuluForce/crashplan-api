#!/bin/bash

usage() {
    echo "Manage the environment for the platform42 project"
    echo "	-u : update the requirements.txt file with your current packages"
    echo "	-i : install project requirements as specified in the requirements.txt file"
    echo "	-f : Specify a different requirements file to update or install from"
    echo "	-b : build the project for distribution"
    echo "	-h : print this help and exit"

    echo -e "\nOnly one of the action flags can be used at a time."
}


UPDATE_REQS=false
INSTALL_REQS=false

BUILD=false

REQS_FILE="requirements.txt"

while getopts ":uif:bh" opt; do
    case $opt in
        u)
        UPDATE_REQS=true
        ;;
        i)
        INSTALL_REQS=true
        ;;
        f)
        REQS_FILE="$OPTARG"
        ;;
        b)
        BUILD=true
        ;;
        h)
            usage
            exit 1
        ;;
        \?)
        echo "Unknown option: -$OPTARG" >&2
        exit 1
        ;;
        :)
        echo "Missing argument for flag -$OPTARG"
        exit 1
        ;;
    esac
done

# Switch to project root
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/../"

if $UPDATE_REQS; then
    echo "Updating $REQS_FILE file"
    pip freeze > "$REQS_FILE"
elif $INSTALL_REQS; then
    echo "Installing packages from $REQS_FILE"
    pip install -r "$REQS_FILE"
elif $BUILD; then
    echo "Building a distribution package"
    python setup.py sdist
else
    echo "No action specified"
    usage
    exit 1
fi

exit 0
