#!/bin/bash
DIRNAME=$(dirname "$0")
. "$DIRNAME"/lib.sh

INDIVIDUAL_SCORING_SCRIPT="$DIRNAME"/get-individual-scoring-finesse.py
PYTHONPATH=$PROJECT_DIR python "$INDIVIDUAL_SCORING_SCRIPT"
