Vẽ Đường Viền trong curses

Trong curses của Python, bạn có thể sử dụng các hàm sau để vẽ đường viền cho cửa sổ:
1. Hàm border()

- Tạo đường viền xung quanh cửa sổ với các ký tự mặc định hoặc tùy chọn.
    Cú pháp:

    python

    stdscr.border(ls, rs, ts, bs, tl, tr, bl, br)

        ls: Ký tự viền bên trái.
        rs: Ký tự viền bên phải.
        ts: Ký tự viền trên.
        bs: Ký tự viền dưới.
        tl: Góc trên trái.
        tr: Góc trên phải.
        bl: Góc dưới trái.
        br: Góc dưới phải.

2. Hàm box()

- Tạo đường viền với ký tự dọc và ký tự ngang.
    Cú pháp:

    python

    stdscr.box(vch, hch)

        vch: Ký tự viền dọc.
        hch: Ký tự viền ngang.

- Ví dụ Minh Họa

python

import curses

def main(stdscr):
    stdscr.clear()       # Xóa màn hình  
    stdscr.border()      # Vẽ đường viền  
    # stdscr.box('|', '-')  # Vẽ đường viền với ký tự tùy chọn  
    stdscr.refresh()     # Làm mới màn hình  
    stdscr.getch()       # Đợi phím nhấn  

curses.wrapper(main)

- Ghi chú

    Hàm border() sử dụng các ký tự mặc định nếu không có tham số nào được cung cấp.
    Hàm box() thích hợp cho việc sử dụng một ký tự cho cả hai cạnh.
