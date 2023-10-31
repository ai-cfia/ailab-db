#!/bin/bash
DIRNAME=$(dirname "$0")
. "$DIRNAME"/lib.sh

SEED_DIRECTORY_PATH=$PROJECT_DIR/seed-data

PYTHONPATH=$PROJECT_DIR python "$DIRNAME"/all-json-dictionary.py "$SEED_DIRECTORY_PATH"