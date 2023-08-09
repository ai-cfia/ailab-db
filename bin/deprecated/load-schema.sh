#!/bin/bash

psql -v ON_ERROR_STOP=1 --single-transaction -d inspection.canada.ca < sql/schema.sql
