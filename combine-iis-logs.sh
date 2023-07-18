#!/bin/sh
# https://www.itnota.com/import-iis-log-postgresql/
if [ ! -d "$1" -o -z "$2" ];
    echo "Usage: $0 directory_with_logs combined_output_log_name"
    exit 1
fi

cat $1/u_*.log  | grep -v ^# |  egrep "GET [^\ ]*/(fra|eng)/" | sed 's:\\:\\\\:g' | > $2