#!/bin/bash

# Thông báo bắt đầu
echo "🚀 Đang cài đặt các thư viện cần thiết..."
pip install -r src/requirements.txt

# Kiểm tra cài đặt thành công không
if [ $? -ne 0 ]; then
    echo "❌ Cài đặt thư viện thất bại. Vui lòng kiểm tra lại requirement.txt."
    exit 1
fi

# Thông báo chạy project
echo "✅ Cài đặt xong. Đang chạy project..."
python src/main.py
