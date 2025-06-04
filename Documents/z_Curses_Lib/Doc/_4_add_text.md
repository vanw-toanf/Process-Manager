### Displaying Text in curses

Curses có thể trông như một mê cung các hàm có chức năng hơi khác nhau, đặc biệt nếu bạn đến từ nền tảng lập trình C. Ví dụ:

- **`addstr()`**: hiển thị một chuỗi tại vị trí con trỏ hiện tại trong cửa sổ `stdscr`.
- **`mvaddstr()`**: di chuyển đến tọa độ `y,x` rồi hiển thị chuỗi.
- **`waddstr()`**: giống `addstr()`, nhưng có thể chỉ định cửa sổ thay vì dùng `stdscr` mặc định.
- **`mvwaddstr()`**: cho phép chỉ định cả cửa sổ và tọa độ.

May mắn là giao diện Python của curses giúp đơn giản hóa thao tác. `stdscr` cũng là một đối tượng cửa sổ và các hàm như `addstr()` có thể chấp nhận nhiều dạng đối số. Các dạng thường gặp là:

| Dạng                             | Mô tả                                                                           |
|----------------------------------|---------------------------------------------------------------------------------|
| `str` hoặc `ch`                  | Hiển thị chuỗi `str` hoặc ký tự `ch` tại vị trí hiện tại                        |
| `str` hoặc `ch`, `attr`          | Hiển thị `str` hoặc `ch` với thuộc tính `attr` tại vị trí hiện tại              |
| `y, x, str` hoặc `ch`            | Di chuyển đến vị trí `y,x` trong cửa sổ, rồi hiển thị `str` hoặc `ch`           |
| `y, x, str` hoặc `ch`, `attr`    | Di chuyển đến vị trí `y,x` trong cửa sổ, rồi hiển thị `str` hoặc `ch` với `attr` |

#### Attributes

- Thuộc tính (**attributes**) giúp hiển thị văn bản theo các kiểu nổi bật như **in đậm**, **gạch chân**, **mã đảo ngược**, hoặc **màu sắc**. Chúng sẽ được giải thích kỹ hơn ở phần tiếp theo.

#### addstr() và addch()

- **`addstr()`**: nhận chuỗi Python hoặc bytestring và hiển thị chúng trên màn hình. Nếu là bytestring, nội dung sẽ được gửi trực tiếp đến terminal, còn chuỗi sẽ được mã hóa thành bytes dựa trên thuộc tính mã hóa của cửa sổ.
- **`addch()`**: nhận một ký tự, có thể là chuỗi độ dài 1, bytestring độ dài 1, hoặc số nguyên. Các ký tự đặc biệt như **`ACS_PLMINUS`** (dấu +/-) hoặc **`ACS_ULCORNER`** (góc trên-trái của một hộp) được biểu diễn dưới dạng hằng số số nguyên lớn hơn 255.

#### Vị trí Con trỏ

- Cửa sổ lưu vị trí con trỏ sau mỗi thao tác. Nếu không chỉ định tọa độ `y,x`, nội dung sẽ được hiển thị tại vị trí con trỏ hiện tại. Con trỏ có thể di chuyển bằng phương thức **`move(y, x)`**.
- Nếu không cần con trỏ nhấp nháy, có thể gọi **`curs_set(False)`** để làm nó ẩn đi. Để tương thích với các phiên bản curses cũ hơn, hàm **`leaveok(bool)`** cũng có thể được dùng để ẩn con trỏ khi `bool` là `True`.
