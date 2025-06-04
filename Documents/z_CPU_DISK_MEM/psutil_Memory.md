## Memory
### 1. `psutil.virtual_memory()`

Hàm `psutil.virtual_memory()` trả về thông tin về việc sử dụng bộ nhớ hệ thống dưới dạng `named tuple`, với các trường được tính bằng byte.

#### Các thông số chính:
- **total**: Tổng bộ nhớ vật lý (không bao gồm swap).
- **available**: Bộ nhớ có thể cung cấp ngay lập tức cho các tiến trình mà không cần sử dụng bộ nhớ swap. Thích hợp để theo dõi mức sử dụng bộ nhớ thực tế trên nhiều nền tảng.
- **percent**: Tỷ lệ bộ nhớ đã sử dụng, tính bằng công thức:  
 `(total - available)/ total * 100`

#### Các thông số khác:
- **used**: Bộ nhớ đã sử dụng, tính toán khác nhau tùy theo nền tảng, thường dùng cho mục đích tham khảo. **total - free** không nhất thiết bằng **used**.
- **free**: Bộ nhớ hoàn toàn không sử dụng (được làm sạch), sẵn sàng để dùng. Lưu ý, **free** không phản ánh bộ nhớ khả dụng thực tế (nên dùng **available**).
  
#### Chỉ trên UNIX:
- **active**: Bộ nhớ hiện đang sử dụng hoặc vừa được sử dụng gần đây, đang nằm trong RAM.
- **inactive**: Bộ nhớ được đánh dấu là không sử dụng.

#### Chỉ trên Linux và BSD:
- **buffers**: Bộ nhớ được sử dụng làm bộ đệm (cache) cho các siêu dữ liệu hệ thống tệp.
- **cached**: Bộ nhớ được sử dụng làm cache cho nhiều tác vụ.
- **shared**: Bộ nhớ có thể được truy cập đồng thời bởi nhiều tiến trình.
- **slab**: Bộ nhớ trong kernel được sử dụng làm cache cho các cấu trúc dữ liệu.

#### Chỉ trên BSD và macOS:
- **wired**: Bộ nhớ được đánh dấu là không thể di chuyển ra khỏi RAM và không bao giờ được chuyển sang đĩa.

#### Lưu ý:
- **used + available** không nhất thiết bằng **total**.
- Trên Windows, **available** và **free** là như nhau.

#### Ví dụ
```python
import psutil
mem = psutil.virtual_memory()
mem
svmem(total=10367352832, available=6472179712, percent=37.6, used=8186245120, free=2181107712, active=4748992512, inactive=2758115328, buffers=790724608, cached=3500347392, shared=787554304, slab=199348224)

# Kiểm tra nếu bộ nhớ khả dụng dưới 100MB
THRESHOLD = 100 * 1024 * 1024  # 100MB
if mem.available <= THRESHOLD:
...     print("warning")
```
### 2. `psutil.swap_memory()`

Hàm `psutil.swap_memory()` trả về thông tin về bộ nhớ **swap** của hệ thống dưới dạng `named tuple` với các trường được tính bằng byte.

#### Các thông số:
- **total**: Tổng dung lượng bộ nhớ swap.
- **used**: Dung lượng bộ nhớ swap đã được sử dụng.
- **free**: Dung lượng bộ nhớ swap còn trống.
- **percent**: Tỷ lệ bộ nhớ swap đã sử dụng, tính bằng công thức:  
`(total - available)/ total * 100`
- **sin**: Số byte hệ thống đã chuyển vào từ đĩa (tích lũy).  
  (Trên Windows luôn bằng 0.)
- **sout**: Số byte hệ thống đã chuyển ra đĩa (tích lũy).  
  (Trên Windows luôn bằng 0.)

#### Lưu ý:
- Bộ nhớ swap được sử dụng khi RAM hệ thống không đủ để xử lý các tiến trình.
- Trên Windows, **sin** và **sout** luôn là 0 do giới hạn của hệ điều hành.
- Để chuyển đổi dung lượng bộ nhớ từ byte sang định dạng dễ đọc, bạn có thể chia cho 1024 hoặc sử dụng các công cụ hỗ trợ.

#### Ví dụ
```python
import psutil
psutil.swap_memory()
sswap(total=2097147904, used=886620160, free=1210527744, percent=42.3, sin=1050411008, sout=1906720768)

# Chuyển đổi byte sang MB
swap = psutil.swap_memory()
total_swap_mb = swap.total / (1024 ** 2)
used_swap_mb = swap.used / (1024 ** 2)
print(f"Tổng bộ nhớ swap: {total_swap_mb} MB")
print(f"Bộ nhớ swap đã sử dụng: {used_swap_mb} MB")
```
