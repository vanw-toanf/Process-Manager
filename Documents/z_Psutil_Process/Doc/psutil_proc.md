# Thư viện Python: `psutil` cho Quản lý Tiến trình

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Các tính năng chính](#các-tính-năng-chính)
- [Cấu trúc thư viện](#cấu-trúc-thư-viện)
<!-- - [Hướng dẫn sử dụng cơ bản](#hướng-dẫn-sử-dụng-cơ-bản) -->
- [Danh sách các hàm](#danh-sách-các-hàm)
- [Xử lý ngoại lệ](#exceptions)
- [Process Class](#process-class)
- [Tham khảo thêm](#tham-khảo-thêm)
- [Tài liệu chính thức](#tài-liệu-chính-thức)

---

## Giới thiệu
### Tổng quan
`psutil` (Python System and Process Utilities) là một thư viện đa nền tảng giúp lấy thông tin về việc sử dụng tài nguyên hệ thống (CPU, bộ nhớ, ổ đĩa, mạng, cảm biến) và các tiến trình. Thư viện rất hữu ích cho việc giám sát hệ thống, phân tích hiệu năng, và quản lý tài nguyên của tiến trình.

### Lợi ích của `psutil`
- Quản lý và giám sát tài nguyên hệ thống hiệu quả
- Lấy thông tin chi tiết về tiến trình và thực hiện các thao tác như dừng hoặc tạm ngừng tiến trình
- Phù hợp để xây dựng công cụ giám sát hệ thống và tự động hóa

## Cài đặt
Cài đặt `psutil` qua pip:

```bash
pip install psutil
```
## Các tính năng chính

- Quản lý Tiến trình: Bắt đầu, dừng và giám sát tiến trình hệ thống
- Thông tin Hệ thống: Truy cập CPU, bộ nhớ, ổ đĩa và sử dụng mạng
- Dữ liệu Cảm biến: Lấy dữ liệu nhiệt độ và pin (nếu có)

## Cấu trúc thư viện

`psutil` cung cấp nhiều module và phương thức để tương tác với tài nguyên hệ thống. Các mudole chính bao gồm:
- Process: Tương tác với các tiến trình hệ thống
- CPU: Thu thập thông tin và số liệu liên quan đến CPU
- Memory: Truy cập thông tin về việc sử dụng bộ nhớ hệ thống
- Disk: Lấy thông tin về các phân vùng ổ đĩa và tình trạng sử dụng
- Network: Giám sát I/O mạng và thông tin kết nối
- Sensors: Thu thập dữ liệu từ cảm biến nhiệt độ và pin (nếu có)

## Danh sách các hàm

1. `psutil.pids()`: Trả về danh sách đã sắp xếp các PID đang chạy. Để lặp lại tất cả các tiến trình và tránh race conditions, nên ưu tiên process_iter().
2. `psutil.process_iter(attrs=None, ad_value=None)`:
- Hàm này trả về một iterator, cho phép lặp qua từng tiến trình một cách hiệu quả.
- Tùy chỉnh thông tin cần lấy về của mỗi tiến trình thông qua tham số `attrs`
- Tham số `ad_value` giúp xử lý trường hợp không thể truy cập được thông tin của một tiến trình nào đó.
- Thứ tự sắp xếp các process sẽ trả về PID của chúng.
``` python
for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
    print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU%: {proc.info['cpu_percent']}")
psutil.process_iter.cache_clear() //xoá bộ nhớ đệm nội bộ
```
3. `psutil.wait_procs(procs, timeout=None, callback=None)`
- Chờ danh sách các phiên bản tiến trình kết thúc. Nó cung cấp một cách thuận tiện để giám sát và quản lý nhiều tiến trình cùng một lúc.
    - Gửi SIGTERM tới danh sách các tiến trình
    - Cho các process chút thời gian để chấm dứt
    - Gửi SIGKILL cho những process vẫn còn sống
- **Trả về**: 
    - gone: Danh sách các phiên bản tiến trình đã kết thúc.
    - alive: Danh sách các phiên bản tiến trình vẫn đang chạy.
```python
def on_terminate(proc):
    print(f"Process {proc.pid} terminated with exit code {proc.returncode}")
# Create a list of processes to wait for
procs = [psutil.Process(pid) for pid in [123, 456, 789]]
# Wait for the processes to terminate with a 10-second timeout
gone, alive = psutil.wait_procs(procs, timeout=10, callback=on_terminate)
print(f"Terminated processes: {gone}")
print(f"Still running processes: {alive}")
for p in alive: // kill các process alive sau khi hết timeout
    p.kill()
```
## Exceptions

1. **`class psutil.Error`**: Lớp ngoại lệ cơ bản, tất cả các trường hợp ngoại lệ khác đều kế thừa từ trường hợp này.
    - quyền hạn không đủ: Khi chương trình của bạn không có quyền truy cập vào thông tin về các tiến trình khác hoặc không thể thực hiện các thao tác trên chúng.
    - Tiến trình không tồn tại: Khi bạn cố gắng truy cập vào một tiến trình đã bị kết thúc hoặc không tồn tại.
    - Lỗi hệ thống: Khi có lỗi xảy ra ở cấp độ hệ điều hành, ví dụ như lỗi I/O, lỗi bộ nhớ, v.v.
    - Tham số không hợp lệ: Khi bạn truyền vào các tham số không đúng hoặc không hợp lệ cho các hàm của psutil.

**Lí do sử dụng**: giúp chương trình không bị dừng đột ngột, xử lý lỗi linh hoạt hơn như log lỗi, gửi thông báo, thực hiện các biện pháp khôi phục

**Ví dụ**
```python
try:
    # Lấy thông tin của một tiến trình không tồn tại
    p = psutil.Process(999999)
    print(p.name())
except psutil.Error as e:
    print(f"Lỗi xảy ra: {e}") 
```
2. **`class psutil.NoSuchProcess(pid, name=None, msg=None)`**: được đưa ra khi không thể tìm thấy một tiến trình có ID tiến trình (PID) được chỉ định hoặc tiến trình đó không còn tồn tại(terminated). Đây là một lớp con của ngoại lệ psutil.Error tổng quát hơn.

**Lí do sử dụng**
- Xử lý lỗi: Điều quan trọng là phải xử lý ngoại lệ này để ngăn chương trình của bị crashing (*sập đột ngột*).
- Thông tin lỗi cụ thể: Đối tượng ngoại lệ cung cấp thông tin về tiến trình bị thiếu, chẳng hạn như PID và tên của nó (nếu có).

**Ví dụ**
```python
try:
    p = psutil.Process(12345)  # Assuming process with PID 12345 doesn't exist
    print(p.name())
except psutil.NoSuchProcess as e:
    print(f"Process with PID 12345 not found: {e}")
```

3. **`class psutil.ZombieProcess(pid, name=None, ppid=None, msg=None)`**: đưa ra khi một tiến trình ở trạng thái zombie. Một tiến trình zombie là một tiến trình đã kết thúc nhưng mục nhập của nó trong bảng tiến trình vẫn tồn tại.
    - Đưa ra khi cố gắng truy cập thông tin về tiến trình zombie bằng psutil. Có thể xảy ra trong trường hợp một tiến trình con đã kết thúc nhưng tiến trình cha của nó vẫn chưa gọi **wait()** để thu thập nó.

**Lí do sử dụng**
- Tiến trình Zombie: Chúng tiêu tốn tài nguyên hệ thống tối thiểu, nhưng chúng có thể làm lộn xộn bảng tiến trình.
- Trách nhiệm của tiến trình cha: Trách nhiệm của tiến trình cha là thu thập các tiến trình con của nó bằng cách sử dụng lệnh gọi hệ thống **wait()**.

**Giải pháp**
- Sự khác biệt về hệ điều hành: Hoạt động của các tiến trình zombie có thể khác nhau một chút giữa các hệ điều hành khác nhau.

- Công cụ giám sát hệ thống: Các công cụ như **top** hoặc **htop** có thể giúp xác định và giám sát các tiến trình của zombie.

- Thực tiễn tốt nhất: Đảm bảo rằng tiến trình của bạn xử lý đúng tiến trình con và gọi **wait()** để thu thập chúng.

**Ví dụ**
```python
try:
    p = psutil.Process(12345)  # Assuming process 12345 is a zombie process
    print(p.name())
except psutil.ZombieProcess as e:
    print(f"Process with PID 12345 is a zombie process: {e}")
```


4. **`class psutil.AccessDenied(pid=None, name=None, msg=None)`**: đưa ra khi người dùng thiếu đủ quyền để truy cập thông tin về một tiến trình cụ thể hoặc thực hiện các thao tác trên đó.
    - quyền không đủ: Khi người dùng chạy tập lệnh Python không có các đặc quyền cần thiết để truy cập thông tin tiến trình.
    - Hạn chế của Hệ điều hành: Một số hệ điều hành có thể áp đặt các hạn chế đối với việc truy cập thông tin tiến trình, đặc biệt là đối với các tiến trình hệ thống.

**Giải pháp**
- Chạy bằng quyền root: Trên các hệ thống giống Unix, việc chạy tập lệnh bằng quyền root thường có thể cung cấp các quyền cần thiết. Tuy nhiên, việc này cần được thực hiện một cách thận trọng và chỉ khi thực sự cần thiết.

- Sử dụng sudo: Trên các hệ thống giống Unix, bạn có thể sử dụng sudo để tạm thời nâng cao đặc quyền cho một lệnh cụ thể.

- Phương pháp tiếp cận thay thế: Trong một số trường hợp, bạn có thể nhận được thông tin hạn chế về các tiến trình mà không có quyền truy cập đầy đủ.

**Ví dụ**
```python
try:
    p = psutil.Process(1)  # Trying to access the init process (usually requires root privileges)
    print(p.name())
except psutil.AccessDenied as e:
    print(f"Access denied to process with PID 1: {e}")
```
5. **`class psutil.TimeoutExpired(seconds, pid=None, name=None, msg=None)`**: đưa ra khi thời gian chờ trong khi chờ tiến trình kết thúc nhưng tiến trình vẫn alive hoặc thực hiện một hành động. 

**Giải pháp**
- Điều chỉnh thời gian chờ: Giá trị thời gian chờ thích hợp tùy thuộc vào trường hợp sử dụng cụ thể và thời lượng dự kiến ​​của tiến trình.

- Hoạt động không chặn: Hãy cân nhắc sử dụng các hoạt động không chặn hoặc kỹ thuật lập trình không đồng bộ để tránh chặn tập lệnh của bạn trong thời gian dài.

- Thông báo lỗi: Thông báo ngoại lệ có thể cung cấp thông tin về tiến trình đã hết thời gian chờ và lý do hết thời gian chờ.

**Ví dụ**
```python
try:
    p = psutil.Process(12345)
    p.wait(timeout=5)  # Wait for 5 seconds for the process to terminate
except psutil.TimeoutExpired as e:
    print(f"Process {p.pid} did not terminate within 5 seconds: {e}")
```
## Process Class

**`oneshot()`** : 
- Trình quản lý bối cảnh **(context manager)** tiện ích giúp tăng tốc đáng kể việc truy xuất thông tin nhiều tiến trình cùng một lúc
- Thông tin tiến trình khác nhau bên trong (ví dụ: *`name(), ppid(), uids(), create_time(), ...`)* có thể được tìm nạp bằng cách sử dụng cùng một tiến trình, nhưng chỉ một giá trị được trả về và các giá trị khác sẽ bị loại bỏ.
- Tiến trình nội bộ được thực thi 1 lần, giá trị quan tâm sẽ được trả về và các giá trị khác sẽ được lưu vào bộ nhớ cached. Bộ đệm sẽ bị xóa khi thoát khỏi khối quản lý bối cảnh.

**Lưu ý** : Để tìm nạp nhiều thông tin về tiến trình cùng một lúc một cách hiệu quả, hãy đảm bảo sử dụng trình quản lý bối cảnh `oneshot()` hoặc phương thức tiện ích `as_dict()`.

**Ví dụ**
```python
p = psutil.Process()
with p.oneshot():
    p.name()  # execute internal routine once collecting multiple info
    p.cpu_times()  # return cached value
    p.cpu_percent()  # return cached value
    p.create_time()  # return cached value
    p.ppid()  # return cached value
    p.status()  # return cached value
```
<hr style="border: px solid;">

**`exe()`**: trả về đường dẫn thực thi của một tiến trình. Xác định chương trình hoặc tập lệnh cụ thể mà một tiến trình đang chạy.
- Khả năng tương thích đa nền tảng: Phương pháp này hoạt động trên các hệ điều hành khác nhau, cung cấp một cách nhất quán để truy xuất đường dẫn thực thi.path.
- Công cụ có giá trị để giám sát hệ thống, phân tích tiến trình và điều tra bảo mật.

**Ví dụ**

```python
p = psutil.Process(psutil.Process().pid)

# Get the executable path
exe_path = p.exe()

print(exe_path)
```

<hr style="border: px solid;">

**`cmdline()`**: Giá trị trả về là danh sách các chuỗi, trong đó mỗi chuỗi đại diện cho một đối số dòng lệnh.

**Ví dụ**

```python
# Get the current Python process
p = psutil.Process(psutil.Process().pid)

# Get the command-line arguments
cmdline = p.cmdline()

print(cmdline)
# ['python3', 'Code/main.py']
```

<hr style="border: px solid;">

**`environ()`**: trả về một từ điển chứa các biến môi trường của một tiến trình. Biến môi trường là cặp key-value cung cấp thông tin về môi trường thực thi của tiến trình.

**Đặc điểm**:
- Các biến môi trường cụ thể có sẵn có thể khác nhau giữa các hệ điều hành khác nhau.
- Các biến này có thể ảnh hưởng đến hành vi của một tiến trình, chẳng hạn như thư mục làm việc, đường dẫn đến tệp thực thi và các cài đặt cấu hình khác.
- Truy cập và sửa đổi các biến môi trường, vì nó có thể gây ra những hậu quả không lường trước được.

**Ví dụ**
```python
# Get the current Python process
p = psutil.Process(psutil.Process().pid)

# Get the environment variables
env_vars = p.environ()

print(env_vars)
```

<hr style="border: px solid;">

**`create_time()`**: trả về thời gian tạo của một tiến trình. Nó cung cấp dấu thời gian khi tiến trình được bắt đầu, được biểu thị dưới dạng số dấu phẩy động biểu thị số giây kể từ kỷ nguyên Unix (ngày 1 tháng 1 năm 1970, 00:00:00 UTC).

**Ví dụ**

```python
# Get the current Python process
p = psutil.Process(psutil.Process().pid)

# Get the creation time
create_time = p.create_time()

# Convert the creation time to a human-readable format
create_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(create_time))

print(f"Process created at: {create_time_str}")
```

<hr style="border: px solid;">

**`as_dict(attrs=None, ad_value=None)`**: Cung cấp một cách thuận tiện để truy xuất nhiều thuộc tính của một tiến trình dưới dạng từ điển. 

**Tham số**:
- attrs: Danh sách tên thuộc tính tùy chọn để đưa vào từ điển. Nếu không được chỉ định, tất cả các thuộc tính có sẵn sẽ được bao gồm.
- ad_value: Giá trị mặc định để sử dụng cho các thuộc tính không thể truy xuất do hạn chế truy cập hoặc các lỗi khác.

**Ví dụ**

```python
# Get the current Python process
p = psutil.Process(psutil.Process().pid)

# Get a dictionary of process information, including PID, name, and CPU usage
info = p.as_dict(attrs=['pid', 'name', 'cpu_percent'])

print(info)
```

<hr style="border: px solid;">

**`parent()`**: trả về một đối tượng đại diện cho tiến trình cha trực tiếp của tiến trình hiện tại.
```python
# Get the parent process
parent_process = p.parent()

if parent_process:
    print(f"Parent process PID: {parent_process.pid}")
    print(f"Parent process name: {parent_process.name()}")
else:
    print("This process is a top-level process.")
```

<hr style="border: px solid;">

**`parents()`**: trả về một danh sách các đối tượng đại diện cho tất cả các tiến trình tổ tiên của tiến trình hiện tại, bắt đầu từ tiến trình cha trực tiếp và đi lên theo hệ thống phân cấp tiến trình.

**Ví dụ**

```python
# Get the current Python process
p = psutil.Process(psutil.Process().pid)

# Get all ancestor processes
ancestor_processes = p.parents()

for ancestor in ancestor_processes:
    print(f"Ancestor process PID: {ancestor.pid}")
    print(f"Ancestor process name: {ancestor.name()}")
```
<hr style="border: px solid;">

**`status`**: Trạng thái tiến trình hiện tại dưới dạng một chuỗi. Chuỗi trả về là một trong các hằng số psutil.STATUS_*.

<hr style="border: px solid;">

**`cwd()`**: trả về thư mục làm việc hiện tại của một tiến trình. Đây là thư mục mà tiến trình được khởi chạy hoặc thư mục mà tiến trình sau đó đã thay đổi thành.

<hr style="border: px solid;">

**`username`**: Tên của người dùng sở hữu tiến trình. Trên UNIX, điều này được tính bằng cách sử dụng uid tiến trình thực.

<hr style="border: px solid;">

**`uids()`**: trả về một namedtuple chứa ID người dùng (UID) thực, hiệu quả và đã lưu của một tiến trình. Các UID này rất quan trọng để hiểu các quyền và bối cảnh bảo mật của tiến trình.

**Ví dụ**

```python
# Get the current Python process
p = psutil.Process(psutil.Process().pid)

# Get the user IDs
uids = p.uids()

print(f"Real UID: {uids.real}")
print(f"Effective UID: {uids.effective}")
print(f"Saved UID: {uids.saved}")
# Real UID: 1000
# Effective UID: 1000
# Saved UID: 1000
```
<hr style="border: px solid;">

**`gids()`**: Id người dùng thực, hiệu quả và được lưu của tiến trình này dưới dạng một bộ dữ liệu namedtuple.

- `Namedtuple`: Đây là một kiểu dữ liệu đặc biệt trong Python, cho phép tạo các cấu trúc dữ liệu giống như tuple nhưng có tên cho từng phần tử.
- `GID: Group` ID là một số nguyên duy nhất xác định một nhóm người dùng trong hệ thống Unix-like.
- `Real GID: `GID thực tế của người dùng khởi chạy tiến trình.
- `Effective `GID: GID hiệu dụng mà tiến trình đang sử dụng để thực hiện các hoạt động. Nó có thể khác với GID thực tế nếu tiến trình đã thay đổi quyền hạn của mình.
- `Saved GID:` GID được lưu trữ để phục hồi sau khi tiến trình thay đổi quyền hạn của mình.

**Ví dụ**

```python

gids = p.gids()

print(f"Real GID: {gids.real}")
print(f"Effective GID: {gids.effective}")
print(f"Saved GID: {gids.saved}")
# Real GID: 1000
# Effective GID: 1000
# Saved GID: 1000
```
<hr style="border: px solid;">

**`terminal()`**: trả về thiết bị đầu cuối được liên kết với một tiến trình. Thông tin này có thể hữu ích để hiểu cách một tiến trình tương tác với thiết bị đầu cuối và cho mục đích gỡ lỗi.

**Ví dụ**

```python
# Get the current Python process
p = psutil.Process(psutil.Process().pid)

# Get the terminal device
terminal = p.terminal()

if terminal:
    print(f"Process is associated with terminal: {terminal}")
else:
    print("Process is not associated with a terminal.")
# Process is associated with terminal: /dev/pts/7
```
<hr style="border: px solid;">

**`nice(value=None)`**: Nhận hoặc thiết lập mức độ ưu tiên của tiến trình (ưu tiên). Trên UNIX, đây là con số thường đi từ -20 đến 20. Giá trị Nice càng cao thì mức độ ưu tiên của tiến trình càng thấp.

**Lí do sử dụng**:
- Cân bằng việc sử dụng tài nguyên giữa các tiến trình khác nhau.
- Tự nguyện giảm mức độ ưu tiên của tiến trình, để quan tâm đến những người dùng khác, đặc biệt là trên các hệ thống dùng chung.

**Ví dụ**

```python
p.nice(10)  # set
p.nice()  # get
```
<hr style="border: px solid;">

**`ionice(ioclass=None, value=None)`**: Nhận hoặc thiết lập mức độ độc đáo I/O của tiến trình (ưu tiên)


**Tham số**
- class: Xác định lớp ưu tiên (Idle, Best-effort, Real-time).
- value: Giá trị phụ thuộc vào lớp ưu tiên, thường được sử dụng để tinh chỉnh mức độ ưu tiên trong cùng một lớp.

**Cấp độ ưu tiên I/O**
- `Idle`: Ưu tiên thấp nhất, thích hợp cho các tiến trình nền hoặc các tiến trình không quan trọng đến hiệu suất.
- `Best-effort`: Ưu tiên trung bình, đây là mức ưu tiên mặc định cho hầu hết các tiến trình.
- `Real-time`: Ưu tiên cao nhất, dành cho các tiến trình đòi hỏi thời gian đáp ứng thực sự nhanh, chẳng hạn như các tiến trình âm thanh hoặc video.

**Các lớp và giá trị I/O:**

- `IOPRIO_CLASS_RT`: (cao) tiến trình luôn có quyền truy cập đầu tiên vào đĩa. Sử dụng nó cẩn thận vì nó có thể làm chết đói toàn bộ hệ thống. Mức độ ưu tiên bổ sung có thể được chỉ định và nằm trong khoảng từ 0 (cao nhất) đến 7 (thấp nhất).

- `IOPRIO_CLASS_BE`: (bình thường) mặc định cho mọi tiến trình chưa đặt mức ưu tiên I/O cụ thể. Mức độ ưu tiên bổ sung dao động từ 0 (cao nhất) đến 7 (thấp nhất).

- `IOPRIO_CLASS_IDLE`: (thấp) nhận thời gian I/O khi không có ai khác cần đĩa. Không có giá trị bổ sung được chấp nhận.

- `IOPRIO_CLASS_NONE`: được trả về khi không có mức độ ưu tiên nào được đặt trước đó.

**Ví dụ**

```python
def set_process_ionice(pid, ioclass, value):
    """Sets the I/O nice level of a process.

    Args:
        pid: The process ID.
        ioclass: The I/O class (one of IONICE_CLASS_IDLE, IONICE_CLASS_BESTEFFORT, IONICE_CLASS_REALTIME).
        value: The I/O class value (0-7).
    """

    p = psutil.Process(pid)
    p.ionice(ioclass, value)

# Example usage:
pid = 1234  # Replace with the desired PID
set_process_ionice(pid, psutil.IOPRIO_CLASS_IDLE, 0)

```
<hr style="border: px solid;">

**`rlimit(resource, limits=None)`**: Nhận hoặc đặt giới hạn tài nguyên cho tiến trình hiện tại. Các giới hạn này kiểm soát các khía cạnh khác nhau của việc sử dụng tài nguyên của tiến trình, chẳng hạn như thời gian CPU, bộ nhớ, bộ mô tả tệp, v.v.

**Đặc trưng**:
- Giới hạn tài nguyên: Đây là những hạn chế được áp đặt lên một tiến trình để ngăn chặn nó tiêu thụ tiến nhiều tài nguyên hệ thống.

- Giới hạn mềm: Giới hạn hiện tại mà tiến trình được thực thi.

- Giới hạn cứng: Giới hạn tối đa có thể được đặt cho tài nguyên.

**Tham số**:

- `resource.RLIMIT_CPU`: Giới hạn thời gian của CPU

- `resource.RLIMIT_FSIZE`: Giới hạn kích thước tệp

- `resource.RLIMIT_DATA`: Giới hạn kích thước phân đoạn dữ liệu

- `resource.RLIMIT_STACK`: Giới hạn kích thước ngăn xếp

- `resource.RLIMIT_CORE`: Giới hạn kích thước tệp lõi

- `resource.RLIMIT_NOFILE`: Giới hạn số lượng file đang mở

- `resource.RLIMIT_AS`: Giới hạn không gian địa chỉ

- `resource.RLIMIT_NPROC`: Giới hạn số lượng tiến trình

- `resource.RLIMIT_MEMLOCK`: Giới hạn bộ nhớ bị khóa
**Ví dụ**

```python
# Get the current soft and hard limits for CPU time
limits = resource.getrlimit(resource.RLIMIT_CPU)
print("Current CPU time limits:", limits)

# Set a soft limit of 10 seconds and a hard limit of 20 seconds
resource.setrlimit(resource.RLIMIT_CPU, (10, 20))

# Get the new limits
new_limits = resource.getrlimit(resource.RLIMIT_CPU)
print("New CPU time limits:", new_limits)
```
<hr style="border: px solid;">

**`io_counters()`**: Trả về số liệu thống kê I/O của tiến trình dưới dạng một bộ dữ liệu được namedtuple 

- `read_count`: số lượng thao tác đọc được thực hiện (tích lũy). Điều này được cho là để đếm số lượng các cuộc gọi tổng hợp liên quan đến việc đọc như read() và pread() trên UNIX.

- `write_count`: số thao tác ghi được thực hiện (tích lũy). Điều này được cho là để đếm số lượng các cuộc gọi tổng hợp liên quan đến việc ghi như write() và pwrite() trên UNIX.

- `read_bytes`: số byte đã đọc (tích lũy). Luôn -1 trên BSD.

- `write_bytes`: số byte được ghi (tích lũy). Luôn -1 trên BSD.

**Đặc biệt với Linux**:
- `read_chars`: số byte mà tiến trình này chuyển tới các tòa nhà cao tầng read() và pread() (tích lũy). Khác với read_bytes, nó không quan tâm liệu I/O đĩa vật lý thực tế có xảy ra hay không.

- `write_chars`: số byte mà tiến trình này chuyển tới các tòa nhà chọc trời write() và pwrite() (tích lũy). Khác với write_bytes, nó không quan tâm liệu I/O đĩa vật lý thực tế có xảy ra hay không.

**Ví dụ**

```python
p.io_counters()
pio(read_count=454556, write_count=3456, read_bytes=110592, write_bytes=0, read_chars=769931, write_chars=203)
```
<hr style="border: px solid;">

**`num_ctx_switches()`**: Số lần chuyển ngữ cảnh tự nguyện và không tự nguyện được thực hiện bởi tiến trình này (tích lũy).

- Voluntary Context Switches: Điều này xảy ra khi một tiến trình tự nguyện nhường CPU, thường là do phải chờ các thao tác I/O hoặc các sự kiện khác.

- Involuntary Context Switches: Xảy ra khi hệ điều hành ưu tiên một tiến trình để cho một tiến trình khác có cơ hội chạy, thường là do cắt thời gian hoặc các tiến trình có mức độ ưu tiên cao hơn.

**Ví dụ**

```python
# Get the number of context switches
ctx_switches = p.num_ctx_switches()

print(f"Voluntary context switches: {ctx_switches.voluntary}")
print(f"Involuntary context switches: {ctx_switches.involuntary}")
# Voluntary context switches: 92
# Involuntary context switches: 0
```
<hr style="border: px solid;">

**`num_fds()`**: Số lượng bộ mô tả tệp hiện được mở bởi tiến trình này (không tích lũy).

**Lí do sử dụng**: 
- Phát hiện rò rỉ tài nguyên: Nếu một tiến trình giữ tiến nhiều mô tả tệp mở, nó có thể gây ra rò rỉ tài nguyên và ảnh hưởng đến hiệu suất của hệ thống.
- Quản lý tài nguyên: Việc biết số lượng mô tả tệp của các tiến trình giúp quản lý hiệu quả các tài nguyên hệ thống.
- Phân tích hiệu suất: Số lượng mô tả tệp có thể cung cấp thông tin về cách một tiến trình tương tác với hệ thống tệp và các thiết bị I/O.

**Ví dụ**

```python
num_fds = p.num_fds()

print(f"Number of file descriptions: {num_fds}")
# 6
```
<hr style="border: px solid;">

**`num_handles()`**: Số lượng thẻ điều khiển hiện đang được tiến trình này sử dụng (không tích lũy).

**Đặc điểm**: Tham chiếu đến nhiều đối tượng khác nhau

- Mô tả tệp: Đã được giải thích ở câu trả lời trước.
- Các đối tượng kernel: Như mutex, semaphore, event, timer,...

**Ví dụ**

```python
num_handles = p.num_handles()

print(f"Số lượng handle của tiến trình: {num_handles}")
```
<hr style="border: px solid;">

**`num_threads`**: Số lượng luồng hiện đang được tiến trình này sử dụng (không tích lũy).

**Ví dụ**

```python
num_threads = process.num_threads()
print(f"Counts : {num_threads}")
```
<hr style="border: px solid;">

**`threads()`**: Trả về các luồng được mở bởi tiến trình dưới dạng danh sách các bộ dữ liệu được đặt tên

**Giá trị trả về**
- `id`: Mã định danh duy nhất của thread.

- `user_time`: Lượng thời gian CPU được sử dụng bởi luồng ở chế độ người dùng.

- `system_time`: Lượng thời gian CPU được sử dụng bởi luồng ở chế độ kernel.

- `current_activity`: Hoạt động hiện tại của luồng, chẳng hạn như chạy, ngủ hoặc chờ.

**Ví dụ**

```python
threads = p.threads()
for thread in threads:
    print(f"Thread ID: {thread.id}")
    print(f"User time: {thread.user_time}")
    # print(f"System time: {thread.system_time}")
# Thread ID: 95472
# User time: 0.02
# System time: 0.0
```
<hr style="border: px solid;">

**`cpu_times()`**: cung cấp thông tin chi tiết về thời gian CPU được sử dụng bởi một tiến trình. Nó trả về một namedtuple chứa các trường sau:

- `user`: Lượng thời gian CPU dành để thực thi mã người dùng.
- `system`: Lượng thời gian CPU dành để thực thi mã hạt nhân thay mặt cho tiến trình.
- `children_user`: Lượng thời gian CPU dành cho các tiến trình con ở chế độ người dùng. 
- `children_system`: Lượng thời gian CPU dành cho các tiến trình con ở chế độ kernel.
**Ví dụ**

```python
cpu_times = p.cpu_times()
print(cpu_times)
sum(p.cpu_times()[:2]) # tích lũy, không bao gồm children và iowait 

# pcputimes(user=0.01, system=0.0, children_user=0.0, children_system=0.0, iowait=0.0)
```
<hr style="border: px solid;">

**`cpu_percent(interval=None)`**: tính toán việc sử dụng CPU của một tiến trình cụ thể. Nó trả về một số float biểu thị việc sử dụng CPU dưới dạng phần trăm.

- `interval=None`: Chế độ này tính toán mức sử dụng CPU kể từ lệnh gọi cuối cùng tới cpu_percent(). Nó rất hữu ích để có được ảnh chụp nhanh về mức sử dụng CPU hiện tại. Tuy nhiên, lệnh gọi đầu tiên có interval=None sẽ luôn trả về 0,0 vì không có phép đo nào trước đó để so sánh.

- `interval=X`: Chế độ này tính toán mức sử dụng CPU trong khoảng thời gian X được chỉ định tính bằng giây. Nó cung cấp phép đo chính xác và nhất quán hơn về mức sử dụng CPU theo thời gian.

**Đặc trưng**
- `Độ chính xác`: Để đo chính xác, bạn nên sử dụng giá trị khoảng khác 0.

- `Nhiều cuộc gọi`: Để nhận được các cập nhật sử dụng CPU liên tục, bạn có thể gọi cpu_percent() liên tục với cùng một giá trị khoảng thời gian.

- `Bối cảnh tiến trình`: Phương thức cpu_percent() tính toán mức sử dụng CPU của tiến trình cụ thể, chứ không phải mức sử dụng CPU của toàn hệ thống.

**Chú ý**:

- Giá trị trả về có thể > 100,0 trong trường hợp một tiến trình chạy nhiều luồng trên các lõi CPU khác nhau.

**Ví dụ**

```python
cpu_percent = p.cpu_percent(interval=1)

print(f"CPU usage: {cpu_percent}%")
```
<hr style="border: px solid;">

**`cpu_affinity(cpus=None)`**: đề cập đến khả năng gán/liên kết một tiến trình hoặc luồng cho một lõi CPU hoặc bộ lõi cụ thể trên hệ thống đa lõi hoặc đa bộ xử lý.

**Ví dụ**

```python
p.cpu_affinity()
[0, 1, 2, 3]
# set; from now on, process will run on CPU #0 and #1 only
p.cpu_affinity([0, 1])
p.cpu_affinity()
[0, 1]
# reset affinity against all eligible CPUs
p.cpu_affinity([])
```
<hr style="border: px solid;">

**`cpu_num()`**: trả về CPU mà tiến trình này hiện đang chạy.
**`cpu_count()`**: trả về số lượng CPU vật lý

- `CPU logic`: Bao gồm cả các luồng (threads) trên mỗi core.
- `CPU vật lý`: Là số lượng core vật lý của CPU.
- `Hyper-threading`: Công nghệ Hyper-threading của Intel làm cho mỗi core vật lý xuất hiện như nhiều core logic.
- `Hệ thống đa socket`: Nếu hệ thống có nhiều socket, mỗi socket có thể chứa nhiều CPU.

**Ví dụ**

```python
# Sử dụng psutil
cpu_num = p.cpu_num() # CPU hiện tại tiến trình đang chạy

num_cpus = psutil.cpu_count(logical=True)  # Số lượng CPU logic

num_cpus = psutil.cpu_count(logical=False)  # Số lượng CPU vật lý

```
<hr style="border: px solid;">

**`memory_info()`**: chức năng hoặc phương pháp được sử dụng để truy xuất thông tin về việc sử dụng bộ nhớ của một tiến trình

**Thông số trả về**: 
- `rss(resident sent size)`: “Kích thước cài đặt thường trú”, đây là bộ nhớ vật lý không thể hoán đổi mà một tiến trình đã sử dụng. Trên UNIX nó khớp với cột RES của “top“

- `vms(virtual memory size)`: “Kích thước bộ nhớ ảo”, đây là tổng dung lượng bộ nhớ ảo được tiến trình sử dụng. Trên UNIX nó khớp với cột VIRT của “top“.
- `shared`: bộ nhớ (Linux) có thể được chia sẻ với các tiến trình khác. Điều này khớp với cột SHR của “top“

- `text (Linux, BSD)`: TRS (text resident set) dung lượng bộ nhớ dành cho mã thực thi. Điều này khớp với cột CODE của “top“.

- `data(Linux, BSD)`:  lượng bộ nhớ dành cho dữ liệu (data segment) và heap, tức là nơi chứa các biến toàn cục, biến động (allocated memory) và dữ liệu do tiến trình tạo ra. Nó khớp với cột DATA của “top“.

- `lib (Linux)`:  lượng bộ nhớ được ánh xạ bởi các thư viện dùng chung (shared libraries). Tuy nhiên, giá trị này thường được báo cáo là 0 trên nhiều hệ điều hành hiện đại, vì bộ nhớ này thường được tính vào shared.

- `dirty (Linux)`: lượng bộ nhớ được sửa đổi trong tiến trình nhưng chưa được ghi trở lại vào ổ cứng. Bộ nhớ này được gọi là "dirty" (bẩn) vì nó cần được đồng bộ hóa với lưu trữ lâu dài trước khi giải phóng.

**Ví dụ**

```python
import psutil
p = psutil.Process()
p.memory_info()

# pmem(rss=11714560, vms=17358848, shared=6025216, text=2822144, lib=0, data=7196672, dirty=0)
```
<hr style="border: px solid;">

**`memory_full_info()`**: giống memory_info , chỉ có thêm vài thông số trả về

- uss(Unique Set Size): “Kích thước cài đặt duy nhất”, bộ nhớ dành riêng cho một tiến trình và sẽ được giải phóng nếu tiến trình đó bị chấm dứt ngay bây giờ.

- pss(Proportional Set Size): “Kích thước cài đặt theo tỷ lệ”, là dung lượng bộ nhớ được chia sẻ với các tiến trình khác, được tính theo cách dung lượng được chia đều cho các tiến trình chia sẻ nó. tức là nếu một tiến trình có tất cả 10 MB cho chính nó và 10 MB được chia sẻ với một tiến trình khác thì PSS của nó sẽ là 15 MB.

- swap (Linux): dung lượng bộ nhớ đã được hoán đổi vào đĩa.

```python
print(p.memory_full_info())
# pfullmem(rss=12025856, vms=17358848, shared=6336512, text=2822144, lib=0, data=7196672, dirty=0, uss=5861376, pss=7316480, swap=0)
```
<hr style="border: px solid;">

**`memory_percent(memtype='rss')`**: So sánh bộ nhớ tiến trình với tổng bộ nhớ hệ thống vật lý và tính toán mức sử dụng bộ nhớ tiến trình theo phần trăm.

**Ví dụ**

```python
p.memory_percent(memtype="rss")
# 0.14495697226152243
```
<hr style="border: px solid;">

**`memory_maps(grouped=True)`**: Nó trả về một danh sách các bộ dữ liệu được đặt tên, mỗi bộ đại diện cho một vùng bộ nhớ được ánh xạ bởi các tiến trình
- Khi được `grouped = True`, phương thức sẽ nhóm các vùng bộ nhớ theo đường dẫn tệp của chúng. Xem tổng mức sử dụng bộ nhớ cho từng tệp hoặc thư viện.

**Return**
- `path, rss, pss`: tương tự với memory_info()
- `Shared_clean`: Bộ nhớ sạch được chia sẻ.

- `Shared_dirty`: Bộ nhớ bẩn được chia sẻ.

- `Private_clean`: Bộ nhớ sạch riêng tư.

- `Private_dirty`: Bộ nhớ bẩn riêng tư.

- `refenced`: Bộ nhớ đã được truy cập gần đây.

- `Private`: Bộ nhớ Private, không được hỗ trợ bởi tệp.

- `Trao đổi(Swap)`: Bộ nhớ đã được hoán đổi vào đĩa.

**Ví dụ**

```python
memory_maps = p.memory_maps(grouped=True)

for memory_map in memory_maps:
    print(f"Path: {memory_map.path}")
    print(f"RSS: {memory_map.rss / 1024 / 1024:.2f} MB")
    print(f"Size: {memory_map.size / 1024 / 1024:.2f} MB")
```
<hr style="border: px solid;">

**`open_files()`**: Trả về các tệp thông thường được mở theo tiến trình dưới dạng danh sách các bộ dữ liệu được đặt tên
- path: tên file tuyệt đối.

- fd: số mô tả tập tin
- vị trí (Linux): vị trí tệp (offset).

- mode (Linux): một chuỗi cho biết cách mở tệp, tương tự như đối số chế độ dựng sẵn mở. Các giá trị có thể là 'r', 'w', 'a', 'r+' và 'a+'. Không có sự phân biệt giữa các tệp được mở ở chế độ nhị phân hoặc văn bản ("b" hoặc "t").

- flags (Linux): các cờ được chuyển đến lệnh gọi os.open C cơ bản khi tệp được mở (ví dụ: os.O_RDONLY, os.O_TRUNC, v.v.).

**Ví dụ**

```python
f = open('file.ext', 'w')
p = psutil.Process()
p.open_files()
[popenfile(path='/home/giampaolo/svn/psutil/file.ext', fd=3, position=0, mode='w', flags=32769)]
```
<hr style="border: px solid;">

**`net_connections(kind='inet')`**: Trả về các kết nối socket được mở theo quy trình dưới dạng danh sách các bộ dữ liệu được đặt tên

**Tham số** :
- `inet`: Các kết nối Internet (TCP hoặc UDP).
- `inet4`: Các kết nối IPv4.
- `inet6`': Các kết nối IPv6.
- `unix`: Các kết nối socket Unix.

**Giá trị trả về**:

- `fd`: Mô tả số (file descriptor) của socket.
- `family`: Gia đình địa chỉ (AF_INET, AF_INET6 hoặc AF_UNIX).
- `type`: Loại socket (SOCK_STREAM, SOCK_DGRAM, SOCK_RAW).
- `laddr`(local): Địa chỉ địa phương (ip, port).
- `raddr`(remote): Địa chỉ từ xa (ip, port).
- `status`: Trạng thái của kết nối (ESTABLISHED, LISTEN, CLOSE_WAIT, ...).
- `pid`: PID của tiến trình sở hữu kết nối

**Ví dụ**

```python
p.net_connections()
```
<hr style="border: px solid;">

**`is_running()`**: Trả về xem quy trình hiện tại có đang chạy trong danh sách quy trình hiện tại không. 
- tự động xóa quy trình khỏi bộ đệm trong của process_iter() nếu PID đã được quy trình khác sử dụng lại.
- trả về True nếu tiến trình là zombie (p.status() == psutil.STATUS_ZOMBIE).


<hr style="border: px solid;">

**`send_signal(signal)`**: gửi tín hiệu cụ thể tới các tiến trình

- Chấm dứt quá trình: Gửi tín hiệu `SIGTERM` hoặc `SIGKILL`.

- Tạm dừng hoặc tiếp tục quá trình: Gửi tín hiệu `SIGSTOP` hoặc `SIGCONT`.

- Tùy chỉnh hành vi của quy trình: Gửi các tín hiệu khác để kích hoạt các hành động cụ thể trong quy trình.

**Ví dụ**

```python
p = psutil.Process(pid)
p.send_signal(signal.SIGTERM)
```
<hr style="border: px solid;">

**`wait(timeout=None)`**: Đợi quá trình PID kết thúc
- Giá trị trả về được lưu trữ trong bộ nhớ đệm. Để chờ nhiều tiến trình, hãy sử dụng `psutil.wait_procs()`.

**Ví dụ**

```python
p = psutil.Process(9891)
p.terminate()
p.wait()
# <Negsignal.SIGTERM: -15>
```
<hr style="border: px solid;">


**`classpsutil.Popen(*args, **kwargs)`**:  tạo và quản lý các quy trình con

- `args`: Một chuỗi các đối số của chương trình. Đối số đầu tiên là chương trình sẽ được thực thi

**kwargs**:

- `stdin`: Bộ mô tả tệp đầu vào tiêu chuẩn.

- `stdout`: Bộ mô tả tệp đầu ra tiêu chuẩn.

- `stderr`: Bộ mô tả tệp lỗi tiêu chuẩn.

- `cwd`: Thư mục làm việc hiện tại của subprocess.

- `env`: Biến môi trường cho tiến trình con.

- `shell`: Nếu đúng thì lệnh sẽ được shell thực thi.

- `Creationflags`: Trên Windows, các cờ tạo bổ sung cho tiến trình.

- start_new_session`: Có bắt đầu một nhóm và phiên quy trình mới hay không.

**Ví dụ**

```python
p = psutil.Popen(['ls', '-la'])

# Wait for the subprocess to finish
p.wait()

# Print the return code
print(p.returncode)
# total 16
# drwxr-xr-x 4 vuong vuong 4096 Nov 11 23:31 .
# drwxr-xr-x 5 vuong vuong 4096 Nov 11 23:31 ..
# drwxr-xr-x 2 vuong vuong 4096 Nov 11 23:31 Code
# drwxr-xr-x 2 vuong vuong 4096 Nov 11 23:31 Doc
# 0
```
<!-- <hr style="border: px solid;">

**``**:

**Ví dụ**

```python

```
<hr style="border: px solid;">

**``**:

**Ví dụ**

```python

```
<hr style="border: px solid;"> -->


<!-- -----------------------Template---------------------------------------------- -->
<!-- .**``**:

- **Lí do sử dụng**
**Ví dụ**
```python

``` -->
<!-- -------------------------------------------------------------------------------->






## Tham khảo thêm
- [Kho mã nguồn psutil trên GitHub](https://github.com/giampaolo/psutil)
- [Hướng dẫn Python `psutil` trên Real Python](https://realpython.com/python-psutil)
- [Chi tiết các hàm trong psutil process ](https://psutil.readthedocs.io/en/latest/#processes)
- [Real process memory and environ in python (Giampaolo)](https://gmpy.dev/blog/2016/real-process-memory-and-environ-in-python)

## Tài liệu chính thức
Để có thêm thông tin chi tiết, tham khảo tài liệu chính thức:
- [Tài liệu `psutil`](https://psutil.readthedocs.io/)