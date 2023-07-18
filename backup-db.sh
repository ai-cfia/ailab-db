#!/bin/bash
TODAY=`date +%Y-%m-%d`
NAME=dumps/inspection.canada.ca.$TODAY.pg_dump
if [ ! -f "$NAME" ]; then
    pg_dump --no-owner --no-privileges -d inspection.canada.ca > $NAME
else
    echo "File $NAME already exists"
fi

if [ ! -f "$NAME.zip" ]; then
    zip $NAME.zip $NAME
else
    echo "File $NAME.zip already exists"
fi

