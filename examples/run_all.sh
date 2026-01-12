#!/usr/bin/env bash

for file in ./out/*.py; do
    if [[ -f "$file" ]]; then
        echo "Running $file"
        echo "=========================="
        python3 "$file"
        echo "=========================="
        echo ""
    fi
done
