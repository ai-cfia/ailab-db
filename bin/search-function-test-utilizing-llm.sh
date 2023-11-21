#!/bin/bash
DIRNAME=$(dirname "$0")
. "$DIRNAME"/lib.sh

PYTHONPATH=$PROJECT_DIR python "$DIRNAME"/search-function-test-utilizing-llm.py