#!/bin/bash

DIRNAME=`dirname $0`

echo "building louis-dataloader"
podman build --format docker \
    -t louis-dataloader \
    .