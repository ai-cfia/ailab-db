#!/bin/bash
DIRNAME=$(dirname "$0")
. "$DIRNAME"/lib.sh

SEED_DATA_PATH=$PROJECT_DIR/seed-data
PROMPT_PATH=$PROJECT_DIR/nachet-data/prompt

PYTHONPATH=$PROJECT_DIR python "$DIRNAME"/seed-identification-api-for-nachet-frontend.py "$SEED_DATA_PATH" "$PROMPT_PATH"