#!/usr/bin/env bash
# Render build script — installs dependencies and seeds the database
set -e

pip install -r requirements.txt
python seed.py

echo "Build complete — database seeded!"
