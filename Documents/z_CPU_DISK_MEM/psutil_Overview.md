# **Thư viện python: `psutil`**
## Giới thiệu
### Tổng quan
#### `psutil` (Python system and process utilities) là một thư viện Python mạnh mẽ cho phép thu thập thông tin chi tiết về các tài nguyên hệ thống và quản lý các tiến trình. Nó cung cấp các hàm API để lấy thông tin về CPU, bộ nhớ, ổ đĩa, mạng và các tiến trình, giúp dễ dàng giám sát, quản lý và phân tích tình trạng hệ thống.
### Mục đích của `psutil`
#### `psutil` được sử dụng chủ yếu cho các tác vụ sau:
- **Theo dõi hệ thống**: Lấy thông tin chi tiết về tài nguyên hệ thống (CPU, RAM, Disk, Network).
- **Quản lý tiến trình**: Theo dõi và kiểm soát các tiến trình đang chạy, bao gồm khởi động, dừng hoặc giám sát chúng.
- **Phát triển các công cụ giám sát**: Hữu ích trong các ứng dụng giám sát hiệu suất hệ thống, đặc biệt là trong DevOps hoặc lập trình hệ thống.
## Cài đặt
Cài đặt `psutil` qua pip:
```
pip install psutill
```
## Một số tính năng chính của `psutil`
- **CPU**: Đo thời gian hoạt động của CPU, phần trăm sử dụng, số lượng lõi CPU, tốc độ xung nhịp, v.v.
- **Memory**: Cung cấp thông tin về bộ nhớ vật lý và bộ nhớ ảo (RAM), dung lượng đã sử dụng, khả dụng, bộ nhớ swap.
- **Disk**: Thông tin về các ổ đĩa, dung lượng, số lượng đọc/ghi, và tốc độ truy cập.
- **Network**: Theo dõi lưu lượng mạng, bao gồm các gói gửi/nhận, địa chỉ IP và các giao diện mạng.
- **Process**: Lấy thông tin chi tiết về các tiến trình, bao gồm ID, tên, CPU và bộ nhớ sử dụng, trạng thái tiến trình, thời gian bắt đầu, v.v.
## Cấu trúc thư viện
#### `psutil` cung cấp nhiều module và phương thức để tương tác với tài nguyên hệ thống. Các module chính bao gồm:
- **Process**: Tương tác với các tiến trình hệ thống
- **CPU**: Thu thập thông tin và số liệu liên quan đến CPU
- **Memory**: Truy cập thông tin về việc sử dụng bộ nhớ hệ thống
- **Disk**: Lấy thông tin về các phân vùng ổ đĩa và tình trạng sử dụng
- **Network**: Giám sát I/O mạng và thông tin kết nối
- **Sensors**: Thu thập dữ liệu từ cảm biến nhiệt độ và pin (nếu có)