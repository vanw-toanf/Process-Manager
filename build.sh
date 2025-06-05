#!/bin/bash

# Start
echo "🚀 Downloading the packages..."
apt-get update && apt-get install -y\
    libgl1 \
    libxkbcommon0 \
    libegl1-mesa \
    fontconfig \
    libglib2.0-0 \
    libdbus-1-3 \
    libxcb-cursor0 \
    libxcb-xinerama0 \
    libxcb-shape0 \
    libxcb-randr0 \
    libxcb-xfixes0 \
    libx11-xcb1 \
    libxcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    make

pip install -r src/requirements.txt

# Check setting
if [ $? -ne 0 ]; then
    echo "❌ Failed. Please check requirements.txt."
    exit 1
fi

# Notify success
echo "✅ Sucessed. The app is running..."
python src/main.py
