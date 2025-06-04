## Nhập liệu trong `curses`

Thư viện `curses` cung cấp các hàm cơ bản để lấy đầu vào từ người dùng. Mặc dù Python  `curses` mở rộng một số chức năng, để có các widget đầu vào phức tạp hơn, bạn có thể tham khảo các thư viện khác như **Urwid**.

### Các phương thức nhập liệu

- **getch()**:
  - Chờ người dùng nhấn phím và làm mới màn hình.
  - Hiển thị ký tự nếu `echo()` đã được gọi trước đó.
  - Chấp nhận tham số tọa độ để di chuyển con trỏ.
  - **Trả về**: một **số nguyên** cho mã ASCII (0-255) hoặc các phím đặc biệt (>255).

- **getkey()**:
  - Tương tự `getch()` nhưng trả về **chuỗi ký tự** (e.g., "KEY_UP", "^G").

- **Nhập liệu không chặn**:
  - Sử dụng `nodelay(True)` để phương thức nhập không chờ đầu vào.
  - **Trả về**: `getch()` trả `curses.ERR` (-1) nếu không có đầu vào.
  - `halfdelay()` có thể đặt thời gian chờ cho `getch()`, nếu không có đầu vào trong khoảng thời gian này, sẽ có ngoại lệ.

### Ví dụ xử lý phím nhấn

Ví dụ mã lặp để xử lý các phím nhấn:
```python
while True:
    c = stdscr.getch()
    if c == ord('p'):
        PrintDocument()  # Xử lý phím 'p'
    elif c == ord('q'):
        break  # Thoát vòng lặp nếu nhấn 'q'
    elif c == curses.KEY_HOME:
        x = y = 0  # Đặt lại vị trí con trỏ

Các tiện ích ASCII

    Module curses.ascii cung cấp:
        Kiểm tra ký tự: Các hàm để kiểm tra mã ASCII theo kiểu số nguyên hoặc chuỗi 1 ký tự.
        Chuyển đổi ký tự điều khiển: curses.ascii.ctrl() chuyển đổi ký tự sang dạng điều khiển.

Nhập chuỗi ký tự

    getstr():
        Nhận toàn bộ chuỗi nhập (chỉ có thể chỉnh sửa bằng backspace và Enter).
        Ví dụ:

        python

        curses.echo()
        s = stdscr.getstr(0, 0, 15)  # Nhận chuỗi tối đa 15 ký tự

Widget Text Box (curses.textpad)

    Dùng để tạo ô nhập văn bản có phím tắt kiểu Emacs:

    python

import curses
from curses.textpad import Textbox, rectangle

def main(stdscr):
    stdscr.addstr(0, 0, "Nhập tin nhắn: (nhấn Ctrl-G để gửi)")
    editwin = curses.newwin(5, 30, 2, 1)
    rectangle(stdscr, 1, 0, 1+5+1, 1+30+1)
    stdscr.refresh()

    box = Textbox(editwin)
    box.edit()  # Cho phép chỉnh sửa đến khi nhấn Ctrl-G
    message = box.gather()  # Lấy chuỗi văn bản
