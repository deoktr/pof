#!/usr/bin/env bash

for file in ./out/*.py; do
    if [[ -f "$file" ]]; then
        python3 "$file"
    fi
done
