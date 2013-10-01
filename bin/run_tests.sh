#!/bin/bash

TEST_DIR="`dirname $0`/../code42/tests"
echo "Test base directory = $TEST_DIR"

nosetests -w "$TEST_DIR" -c "$TEST_DIR/nose_setup.cfg" --processes=2

#--with-coverage --cover-erase --cover-html-dir=$TEST_DIR/../build/tests/coverage \
