#!/bin/bash

echo "🧹 Cleaning build artifacts..."

# PyInstaller artifacts
rm -rf build irshelper/usr/local/bin/irshelper *.spec

# Python packaging artifacts
rm -rf *.egg-info
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

echo "✅ Clean complete."
