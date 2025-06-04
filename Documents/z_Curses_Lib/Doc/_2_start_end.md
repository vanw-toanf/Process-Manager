# Bắt đầu và kết thúc một ứng dụng curses

## START CURSES

Trước khi làm gì khác, curses cần được khởi tạo. Điều này được thực hiện bằng cách gọi hàm `initscr()`, nó sẽ xác định loại terminal, gửi các mã thiết lập cần thiết đến terminal, và tạo ra các cấu trúc dữ liệu bên trong. Nếu thành công, `initscr()` trả về một đối tượng cửa sổ đại diện cho toàn bộ màn hình; đối tượng này thường được gọi là `stdscr`, giống tên biến trong C.

*"import curses*
*stdscr = curses.initscr()"*

---

Thông thường, ứng dụng curses sẽ **tắt việc tự động hiển thị phím nhấn trên màn hình**, để có thể đọc phím và chỉ hiển thị chúng trong một số trường hợp cụ thể. Để làm vậy, ta gọi hàm noecho():

*curses.noecho()*

---

Đôi khi Ứng dụng cũng thường cần **phản hồi ngay lập tức** với phím nhấn mà không yêu cầu nhấn phím Enter; đây gọi là chế độ cbreak, khác với chế độ nhập có bộ đệm thông thường.

*curses.cbreak()*

---

Các terminal thường trả về các phím đặc biệt như *phím mũi tên* hoặc *phím điều hướng (như Page Up, Home)* dưới *dạng chuỗi mã thoát nhiều byte*. Bạn có thể lập trình để xử lý chuỗi này, nhưng curses có thể tự xử lý, trả về các giá trị đặc biệt như *curses.KEY_LEFT*. Để curses làm việc này, bạn cần bật chế độ keypad:

stdscr.keypad(True)

---

## END CURSES

Kết thúc một ứng dụng curses dễ hơn nhiều so với khởi động. Bạn chỉ cần gọi:

*curses.nocbreak()*
*stdscr.keypad(False)*
*curses.echo()*

---

để trả terminal về chế độ bình thường. Sau đó gọi hàm endwin() để khôi phục terminal về chế độ gốc.

*curses.endwin()*

---

## SOME ERRORS

Một vấn đề phổ biến khi gỡ lỗi ứng dụng curses là terminal sẽ bị lỗi nếu ứng dụng **dừng mà không phục hồi lại trạng thái gốc của terminal**. Trong Python, điều này thường xảy ra khi có lỗi chưa xử lý gây ngoại lệ, khiến bạn không thể thấy các phím nhấn trên màn hình, và việc sử dụng shell trở nên khó khăn.

Trong Python, bạn có thể tránh rắc rối này và làm cho quá trình gỡ lỗi dễ dàng hơn bằng cách dùng hàm *curses.wrapper()* như sau:

from curses import wrapper

def main(stdscr):
    #stdscr is an object control screen
    # Xóa màn hình
    stdscr.clear()

    # Tạo lỗi ZeroDivisionError khi i == 10
    for i in range(0, 11):
        v = i - 10
        stdscr.addstr(i, 0, '10 chia cho {} là {}'.format(v, 10 / v))

    stdscr.refresh()
    stdscr.getkey()

wrapper(main) #with default is noecho(), cbreak(), keypad(True)

Hàm wrapper() nhận một đối tượng callable và thực hiện các khởi tạo cần thiết đã mô tả ở trên, cũng như khởi tạo màu nếu có hỗ trợ. Sau khi chạy callable bạn cung cấp, wrapper() sẽ phục hồi trạng thái gốc của terminal. Callable sẽ chạy trong một khối try…except để bắt ngoại lệ, phục hồi trạng thái terminal, và sau đó phát lại ngoại lệ. Vì vậy, terminal sẽ không ở trạng thái lỗi sau khi gặp ngoại lệ, và bạn có thể đọc thông báo lỗi và theo dõi lỗi một cách dễ dàng.