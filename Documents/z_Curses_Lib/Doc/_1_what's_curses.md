# Curses là gì?

Thư viện curses cung cấp các chức năng vẽ màn hình và xử lý bàn phím độc lập với loại terminal, sử dụng cho các terminal dạng văn bản như VT100, **console của Linux**, và terminal mô phỏng của nhiều chương trình. Những terminal này hỗ trợ các mã điều khiển để thực hiện các thao tác như di chuyển con trỏ, cuộn màn hình, và xóa các khu vực. Mỗi loại terminal có mã điều khiển khác nhau và thường có các chi tiết riêng.

---

Curses cung cấp các chức năng cơ bản, cho phép lập trình viên làm việc với màn hình gồm nhiều cửa sổ văn bản không chồng lấn nhau. Nội dung trong một cửa sổ có thể thay đổi theo nhiều cách—thêm chữ, xóa chữ, thay đổi hiển thị—và curses sẽ tự tính toán mã điều khiển cần gửi đến terminal để tạo ra đầu ra chính xác. Tuy nhiên, curses **không cung cấp** các yếu tố giao diện người dùng như **nút, hộp chọn hay hộp thoại**; nếu cần, bạn có thể dùng thư viện giao diện như Urwid.

---

Thư viện curses ban đầu được viết cho Unix BSD, và các phiên bản sau của Unix System V từ AT&T đã bổ sung nhiều cải tiến. BSD curses đã ngừng phát triển và được thay thế bởi ncurses, một bản mã nguồn mở của curses từ AT&T. Nếu bạn sử dụng Unix mã nguồn mở như Linux hay FreeBSD, hệ thống của bạn gần như chắc chắn sử dụng ncurses. Các phiên bản Unix thương mại hiện nay dựa trên System V, nên các chức năng này thường có sẵn. Những phiên bản curses cũ trên một số Unix có thể không hỗ trợ đầy đủ tính năng.

Python trên Windows không bao gồm curses, nhưng có phiên bản UniCurses dành cho Windows.