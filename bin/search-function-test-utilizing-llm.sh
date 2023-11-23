#!/bin/bash
DIRNAME=$(dirname "$0")
. "$DIRNAME"/lib.sh

PROMPT_PATH=$PROJECT_DIR/ailab/db/finesse/prompt

PYTHONPATH=$PROJECT_DIR python "$DIRNAME"/search-function-test-utilizing-llm.py "$PROMPT_PATH"