### Attributes and Color in curses

curses hỗ trợ nhiều kiểu hiển thị ký tự khác nhau thông qua các thuộc tính và màu  sắc, giúp tạo nên các ứng dụng văn bản nổi bật. 

#### Các thuộc tính thường gặp:
| **Attribute**       | **Mô tả**                 |
|---------------------|---------------------------|
| `A_BLINK`          | Văn bản nhấp nháy         |
| `A_BOLD`           | Văn bản đậm               |
| `A_DIM`            | Văn bản sáng một nửa      |
| `A_REVERSE`        | Video đảo ngược           |
| `A_STANDOUT`       | Kiểu nổi bật tốt nhất      |
| `A_UNDERLINE`      | Gạch chân văn bản         |

**Ví dụ**: Hiển thị dòng trạng thái video đảo ngược:
```python
stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
stdscr.refresh()

Sử dụng Màu sắc

    Khởi tạo màu: Gọi start_color() sau initscr().
    Kiểm tra hỗ trợ màu: Sử dụng has_colors().
    Cặp màu (color pair): curses tạo cặp màu gồm nền và chữ với init_pair(n, f, b) (n  là mã cặp, f là màu chữ, b là màu nền).

Ví dụ: Tạo màu đỏ trên nền trắng và áp dụng:

python

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
stdscr.addstr(0, 0, "RED ALERT!", curses.color_pair(1))
stdscr.refresh()

    Màu cơ bản: start_color() khởi tạo 8 màu: đen, đỏ, xanh lá, vàng, xanh dương,  tím, xanh cyan, và trắng. curses định nghĩa hằng số cho các màu này như curses.COLOR_RED, curses.COLOR_WHITE.

Tùy biến nâng cao

Một số terminal hỗ trợ tùy chỉnh màu RGB với can_change_color(), nhưng tính năng này  không phải lúc nào cũng được hỗ trợ.