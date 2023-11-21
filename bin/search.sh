#!/bin/bash
DIRNAME=$(dirname "$0")
. "$DIRNAME"/lib.sh

PYTHONPATH=$PROJECT_DIR python "$DIRNAME"/search.py "$@"
