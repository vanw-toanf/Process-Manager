#!/bin/bash

# Thông báo bắt đầu
echo "🚀 Downloading the packages..."
pip install -r src/requirements.txt

# Kiểm tra cài đặt thành công không
if [ $? -ne 0 ]; then
    echo "❌ Failed. Please check requirements.txt."
    exit 1
fi

# Thông báo chạy project
echo "✅ Sucessed. The app is running..."
python src/main.py
