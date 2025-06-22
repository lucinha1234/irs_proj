#!/bin/bash

echo "🧪 Running unit tests..."
PYTHONPATH="$PYTHONPATH:$(pwd)/../src" pytest -v
