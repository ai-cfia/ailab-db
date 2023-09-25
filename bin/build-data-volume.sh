#!/bin/bash

DIRNAME=`dirname $0`

if [ -z "$1" ]; then
    echo "usage: $0 LOUIS_SCHEMA"
    exit 1
fi
if [ ! -d "$DIRNAME/dumps/$1" ]; then
    echo "No such schema $1"
    exit 1
fi

LOUIS_SCHEMA=$1

VOLUME_NAME=louis-data-$LOUIS_SCHEMA
echo "building louis-data label LOUIS_SCHEMA=$LOUIS_SCHEMA"
podman volume create \
    --label LOUIS_SCHEMA=$LOUIS_SCHEMA \
     $VOLUME_NAME

ARCHIVE=$DIRNAME/dumps/$LOUIS_SCHEMA.tgz
if [ ! -f "$ARCHIVE" ]; then
    tar cvfz $ARCHIVE --directory $DIRNAME/dumps/$LOUIS_SCHEMA .
fi

gunzip -c $ARCHIVE | podman volume import $VOLUME_NAME -

