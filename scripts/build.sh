#!/bin/bash

# Exit on error
set -e

# Define variables
MAIN_SCRIPT="src/irshelper/gui.py"
APP_NAME="irshelper"

echo "🔧 Cleaning previous build..."
rm -rf build dist *.spec

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Building executable..."
pyinstaller --noconfirm --onefile --windowed "$MAIN_SCRIPT" --name "$APP_NAME"

echo "✅ Build complete. Executable is in ./dist/$APP_NAME"

# Control file
#cat > myapp/DEBIAN/control <<EOF
#Package: myapp
#Version: 1.0.0
#Section: base
#Priority: optional
#Architecture: all
#Depends: python3
#Maintainer: Your Name <you@example.com>
#Description: MyApp - a tool that does amazing things
# A longer multiline description
#EOF

# Build the package
#dpkg-deb --build myapp

#echo "✅ Built myapp.deb"
