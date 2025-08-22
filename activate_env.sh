#!/bin/bash
# activate.sh

# Exit if venv does not exist
if [ ! -d "venv" ]; then
  echo "No venv directory found. Run: python3 -m venv venv"
  exit 1
fi

# Source the venv and drop into a new shell
source venv/bin/activate
exec "$SHELL"
