#!/bin/bash

# Start
echo "🚀 Downloading the packages..."
apt-get update && apt-get install -y make

pip install -r src/requirements.txt

# Check setting
if [ $? -ne 0 ]; then
    echo "❌ Failed. Please check requirements.txt."
    exit 1
fi

# Notify success
echo "✅ Sucessed. The app is running..."
python src/main.py
