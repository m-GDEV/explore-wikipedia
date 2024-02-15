#!/bin/bash

# Simple script to get wiki urls of one page, uses $1 as link

curl -s "$1" | htmlq a | grep -o 'href="/wiki/[^"]*"' | sed 's/href="\(.*\)"/\1/g' | ugrep '^/wiki/[\w_()/\-\.]*$' | sort | uniq

