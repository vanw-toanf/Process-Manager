## Disks
### 1. `psutil.disk_partitions(all=False)`

Hàm `psutil.disk_partitions()` trả về danh sách các phân vùng đĩa được gắn kết (mounted) trên hệ thống dưới dạng một danh sách các `named tuple`. Hàm này tương tự như lệnh `df` trên hệ thống UNIX.

#### Các tham số:
- `False` (mặc định): Chỉ trả về các thiết bị vật lý (ổ cứng, USB, CD-ROM, v.v.).  
- `True`: Trả về tất cả các phân vùng, bao gồm cả những phân vùng giả lập, trùng lặp hoặc không thể truy cập.  
  *(Lưu ý: Trên một số hệ điều hành như BSD, tham số này có thể bị bỏ qua.)*

#### Các trường thông tin trả về:
- **device**: Đường dẫn tới thiết bị (ví dụ: `/dev/sda1`).  
  Trên Windows, giá trị này là ký tự ổ đĩa (ví dụ: `C:\\`).
- **mountpoint**: Đường dẫn nơi thiết bị được gắn kết (ví dụ: `/home`).  
  Trên Windows, giá trị này là ký tự ổ đĩa (ví dụ: `C:\\`).
- **fstype**: Loại hệ thống tệp của phân vùng (ví dụ: `ext3` trên UNIX, `NTFS` trên Windows).
- **opts**: Chuỗi các tùy chọn gắn kết của phân vùng, được phân cách bằng dấu phẩy (platform-dependent).  
  Ví dụ: `rw` (read-write), `ro` (read-only).

#### Ví dụ:
```python
import psutil
psutil.disk_partitions()
[sdiskpart(device='/dev/sda3', mountpoint='/', fstype='ext4', opts='rw,errors=remount-ro'),
 sdiskpart(device='/dev/sda7', mountpoint='/home', fstype='ext4', opts='rw')]

# Truy xuất thông tin chi tiết từng phân vùng
partitions = psutil.disk_partitions()
for partition in partitions:
...     print(f"Thiết bị: {partition.device}")
...     print(f"Điểm gắn kết: {partition.mountpoint}")
...     print(f"Hệ thống tệp: {partition.fstype}")
...     print(f"Tùy chọn: {partition.opts}")
...     print("-" * 20)
```
### 2. `psutil.disk_usage(path)`

Hàm `psutil.disk_usage()` trả về thông tin thống kê về việc sử dụng đĩa của phân vùng chứa đường dẫn được chỉ định (`path`). Kết quả được trả về dưới dạng một `named tuple`, bao gồm các trường thông tin sau:

#### Các trường thông tin:
- **total**: Tổng dung lượng của phân vùng (tính bằng byte).
- **used**: Dung lượng đã sử dụng (tính bằng byte).
- **free**: Dung lượng còn trống (tính bằng byte).
- **percent**: Tỷ lệ sử dụng của phân vùng (tính bằng %).

#### Tham số:
- **path**: Đường dẫn tới phân vùng cần kiểm tra. Nếu đường dẫn không tồn tại, hàm sẽ trả về lỗi `OSError`.

#### Lưu ý:
- Trên hệ thống **UNIX**, thường có 5% dung lượng đĩa được dự trữ cho người dùng root.  
  - Trường **total** và **used** biểu thị tổng dung lượng và dung lượng đã sử dụng (bao gồm cả phần dự trữ).  
  - Trường **free** chỉ biểu thị dung lượng khả dụng cho người dùng thường.  
  - Trường **percent** tính toán dựa trên dung lượng có thể sử dụng bởi người dùng thông thường, nên giá trị này thường lớn hơn 5% so với dự kiến.  
- Kết quả trả về tương ứng với lệnh `df` trên dòng lệnh UNIX.

#### Ví dụ:
```python
import psutil
psutil.disk_usage('/')
sdiskusage(total=21378641920, used=4809781248, free=15482871808, percent=22.5)

# Truy xuất thông tin và hiển thị theo định dạng dễ đọc
usage = psutil.disk_usage('/')
print(f"Tổng dung lượng: {usage.total / (1024 ** 3):.2f} GB")
print(f"Dung lượng đã sử dụng: {usage.used / (1024 ** 3):.2f} GB")
print(f"Dung lượng còn trống: {usage.free / (1024 ** 3):.2f} GB")
print(f"Tỷ lệ sử dụng: {usage.percent:.2f}%")
```
### 3. `psutil.disk_io_counters(perdisk=False, nowrap=True)`

Hàm `psutil.disk_io_counters()` trả về thông tin thống kê về hoạt động I/O của đĩa hệ thống. Thông tin này được trả về dưới dạng một `named tuple` bao gồm các trường sau:

#### Các trường thông tin:
- **read_count**: Số lần đọc dữ liệu.
- **write_count**: Số lần ghi dữ liệu.
- **read_bytes**: Tổng số byte đã đọc.
- **write_bytes**: Tổng số byte đã ghi.

#### Các trường dành riêng cho từng nền tảng:
- **read_time**: (Tất cả hệ điều hành trừ NetBSD và OpenBSD) Tổng thời gian đọc dữ liệu từ đĩa (tính bằng mili giây).
- **write_time**: (Tất cả hệ điều hành trừ NetBSD và OpenBSD) Tổng thời gian ghi dữ liệu vào đĩa (tính bằng mili giây).
- **busy_time**: (Linux, FreeBSD) Thời gian thực hiện các hoạt động I/O thực tế (tính bằng mili giây).
- **read_merged_count** (Linux): Số lần đọc được hợp nhất.
- **write_merged_count** (Linux): Số lần ghi được hợp nhất.

#### Tham số:
- **perdisk** (`bool`, mặc định `False`):  
  - Nếu `False`: Trả về thông tin tổng hợp cho tất cả các đĩa.
  - Nếu `True`: Trả về thông tin cho từng đĩa dưới dạng một dictionary, trong đó:
    - **Key**: Tên phân vùng.
    - **Value**: Các số liệu thống kê dưới dạng `named tuple`.
- **nowrap** (`bool`, mặc định `True`):  
  - Nếu `True`: Điều chỉnh số liệu khi giá trị từ kernel bị "quay vòng" (số liệu bắt đầu lại từ 0).  
  - Nếu `False`: Trả về giá trị gốc từ kernel, có thể bị giảm nếu hệ thống quá tải hoặc tồn tại lâu dài.  
  - **Lưu ý**: Nếu cần làm sạch bộ nhớ cache khi bật nowrap, sử dụng `disk_io_counters.cache_clear()`.

#### Lưu ý:
- **Windows**:  
  - Có thể cần chạy lệnh `diskperf -y` trong `cmd.exe` để kích hoạt bộ đếm IO.
- **Máy không có đĩa vật lý**:  
  - Hàm trả về `None` nếu `perdisk=False`, hoặc `{}` nếu `perdisk=True`.

#### Ví dụ:
```python
import psutil

# Thống kê tổng hợp cho tất cả các đĩa
disk_stats = psutil.disk_io_counters()
print(disk_stats)
# sdiskio(read_count=8141, write_count=2431, read_bytes=290203, write_bytes=537676, read_time=5868, write_time=94922)

# Thống kê chi tiết cho từng đĩa
perdisk_stats = psutil.disk_io_counters(perdisk=True)
for disk, stats in perdisk_stats.items():
    print(f"Disk {disk}: {stats}")
# Disk sda1: sdiskio(read_count=920, write_count=1, read_bytes=2933248, write_bytes=512, read_time=6016, write_time=4)
```