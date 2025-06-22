#!/bin/bash

# Exit on error
set -e

# Define variables
MAIN_SCRIPT="gui.py"
APP_NAME="xmlcsvtool"

echo "🔧 Cleaning previous build..."
rm -rf build dist *.spec

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Building executable..."
pyinstaller --noconfirm --onefile --windowed "$MAIN_SCRIPT" --name "$APP_NAME"

echo "✅ Build complete. Executable is in ./dist/$APP_NAME"
