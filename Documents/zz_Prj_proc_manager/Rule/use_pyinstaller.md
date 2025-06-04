# Biên Dịch File Python Thành Chương Trình Thực Thi Trên Linux

## 1. Cài đặt PyInstaller
Mở terminal và chạy lệnh sau để cài đặt PyInstaller:

```bash
pip install pyinstaller
```

---

## 2. Chuyển File Python Thành Chương Trình Thực Thi
Giả sử file Python của bạn là `main.py`, làm theo các bước sau:

### a) Tạo File Thực Thi Đơn Giản
```bash
pyinstaller --onefile main.py
```

- Tùy chọn `--onefile` tạo ra một file thực thi duy nhất.
- Sau khi hoàn tất, chương trình thực thi sẽ nằm trong thư mục `dist/main`.

### b) Đặt Tên Cụ Thể Cho File Thực Thi
```bash
pyinstaller --onefile --name my_program main.py
```
File thực thi sẽ có tên là `my_program`.

### c) Thêm Icon (Tuỳ Chọn)
Nếu muốn thêm icon cho chương trình, sử dụng tùy chọn `--icon`:
```bash
pyinstaller --onefile --icon=my_icon.ico main.py
```
Lưu ý: Icon phải ở định dạng `.ico`.

---

## 3. Chạy File Thực Thi
Chuyển đến thư mục `dist` nơi file thực thi được tạo ra:

```bash
cd dist
./main
```

---

## 4. Những Lưu ý Quan Trọng

### a) Phiên Bản Python
- Đảm bảo bạn sử dụng phiên bản Python phù hợp với môi trường đích.
- Ví dụ: Nếu môi trường đích sử dụng Python 3.8, bạn nên dùng cùng phiên bản để tránh lỗi tương thích.

### b) Thư Viện Phụ Thuộc
- PyInstaller sẽ tự động đóng gói các thư viện mà file Python của bạn sử dụng.

### c) Kích Thước File
- File thực thi có thể lớn hơn do bao gồm cả trình thông dịch Python.
