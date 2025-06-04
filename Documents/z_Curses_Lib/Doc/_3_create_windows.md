# Windows và Pads trong curses

## 1. Windows
- **Windows**: Đối tượng window trong curses đại diện cho vùng chữ nhật trên màn hình, hỗ trợ các phương thức hiển thị, xóa văn bản, nhập chuỗi.
- **stdscr**: Đối tượng window bao phủ toàn bộ màn hình, được tạo bởi hàm `initscr()`.
- **Tạo window mới**: Sử dụng `newwin(height, width, begin_y, begin_x)` để tạo một window mới với kích thước và vị trí cụ thể.

    begin_x = 20; begin_y = 7  
    height = 5; width = 40  
    win = curses.newwin(height, width, begin_y, begin_x)  

Kích thước màn hình: Sử dụng curses.LINES và curses.COLS để lấy kích thước y và x của màn hình.

---

## 2. Refresh màn hình

- **refresh()**: Phải gọi refresh() để cập nhật màn hình với các thay đổi mới; curses tối ưu hóa việc hiển thị khi gọi phương thức này.
- Đặc biệt khi có nhiều cửa sổ cần update, để tránh hiện tượng nhấp nháy ta không refresh ngay mà dùng 1 cơ chế là cập nhật ẩn và update cùng lúc:  
    **noutrefresh()**: Cập nhật cấu trúc dữ liệu ẩn với trạng thái mong muốn của màn hình.  
    **doupdate()**: Cập nhật màn hình thực tế với trạng thái đã được lưu trong cấu trúc dữ liệu.  

---

## 3. Pads

- Pads: Loại window đặc biệt, có thể lớn hơn màn hình; chỉ hiển thị một phần của pad tại một thời điểm.

- Tạo pad: Sử dụng curses.newpad(height, width).

    pad = curses.newpad(100, 100)  
    for y in range(0, 99):  
        for x in range(0, 99):  
            pad.addch(y, x, ord('a') + (x*x + y*y) % 26)  

    pad.refresh(0, 0, 5, 5, 20, 75)  

refresh() trên pad: Cần chỉ định tọa độ của phần pad hiển thị trên màn hình.

Sử dụng hiệu quả với nhiều windows/pads: Gọi noutrefresh() cho các windows/pads cần cập nhật, sau đó gọi doupdate() để tránh nhấp nháy.