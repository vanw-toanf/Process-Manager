## CPU
### 1. `psutil.cpu_times(percpu=False)`
Hàm này trả về thời gian CPU hệ thống dưới dạng một `named tuple`. Mỗi thuộc tính của tuple biểu diễn thời gian (tính theo giây) mà CPU đã dành cho từng chế độ hoạt động cụ thể. Các thuộc tính này có thể thay đổi tùy vào hệ điều hành.
#### Các thuộc tính chung:
- **user**: Thời gian dành cho các tiến trình chạy ở chế độ user mode (chế độ người dùng); trên Linux, bao gồm cả thời gian `guest`.
- **system**: Thời gian dành cho các tiến trình chạy ở chế độ kernel mode (chế độ nhân hệ điều hành).
- **idle**: Thời gian CPU không thực hiện hoạt động nào.
#### Các thuộc tính đặc trưng cho Linux:
- **nice** (UNIX): Thời gian dành cho các tiến trình được ưu tiên (niced) chạy ở chế độ user mode; trên Linux, bao gồm cả `guest_nice`.
- **iowait** (Linux): Thời gian chờ đợi hoàn thành I/O; thời gian này không được tính vào thời gian `idle`.
- **irq** (Linux, BSD): Thời gian phục vụ ngắt phần cứng.
- **softirq** (Linux): Thời gian phục vụ ngắt phần mềm.
- **steal** (Linux 2.6.11+): Thời gian dành cho các hệ điều hành khác chạy trong môi trường ảo hóa.
- **guest** (Linux 2.6.24+): Thời gian chạy CPU ảo cho các hệ điều hành guest dưới sự điều khiển của kernel Linux.
- **guest_nice** (Linux 3.2.0+): Thời gian chạy CPU ảo được ưu tiên (niced) cho các hệ điều hành guest.
#### Các thuộc tính riêng cho Windows:
- **interrupt**: Thời gian phục vụ ngắt phần cứng (tương tự `irq` trên UNIX).
- **dpc**: Thời gian phục vụ DPC (Deferred Procedure Calls); DPC là các ngắt có độ ưu tiên thấp hơn ngắt chuẩn.
#### Tham số `percpu`
- Khi `percpu=True`, hàm sẽ trả về danh sách các `named tuple` cho từng CPU logic trên hệ thống. Phần tử đầu tiên trong danh sách là CPU đầu tiên, phần tử thứ hai là CPU thứ hai, và cứ tiếp tục như vậy. Thứ tự trong danh sách sẽ giữ nguyên trong các lần gọi hàm liên tiếp.
#### Ví dụ trên linux
```python
import psutil
psutil.cpu_times()
scputimes(user=17411.7, nice=77.99, system=3797.02, idle=51266.57, iowait=732.58, irq=0.01, softirq=142.43, steal=0.0, guest=0.0, guest_nice=0.0)
```
### 2. `psutil.cpu_percent(interval=None, percpu=False)`

Hàm `psutil.cpu_percent()` trả về mức độ sử dụng CPU hiện tại dưới dạng phần trăm.

- **interval > 0.0**: Khi `interval` lớn hơn 0, hàm sẽ so sánh thời gian CPU đã sử dụng trước và sau khoảng thời gian `interval` đó.
  
- **interval = 0.0 hoặc None**: Khi `interval` là 0.0 hoặc None, hàm sẽ so sánh thời gian CPU đã sử dụng kể từ lần gọi hàm trước hoặc kể từ khi thư viện được import, và sẽ trả về ngay lập tức.

- **percpu**: Khi `percpu=True`, hàm trả về danh sách các số thập phân đại diện cho mức độ sử dụng của từng CPU logic. Phần tử đầu tiên là CPU đầu tiên, phần tử thứ hai là CPU thứ hai, v.v. Thứ tự này được giữ cố định qua các lần gọi hàm.

#### Sử dụng đa luồng:
- Hàm này duy trì một bản đồ toàn cục (dạng từ điển), trong đó mỗi khóa là ID của luồng đang gọi (sử dụng `threading.get_ident`). Điều này cho phép gọi hàm từ các luồng khác nhau với các khoảng `interval` khác nhau, nhưng vẫn đảm bảo kết quả độc lập và có ý nghĩa.

#### Ví dụ:
```python
import psutil
# blocking
psutil.cpu_percent(interval=1)
2.0
# non-blocking (phần trăm sử dụng kể từ lần gọi cuối)
psutil.cpu_percent(interval=None)
2.9
# blocking, theo từng CPU
psutil.cpu_percent(interval=1, percpu=True)
[2.0, 1.0]
```
### 3. `psutil.cpu_times_percent(interval=None, percpu=False)`

Hàm `psutil.cpu_times_percent()` hoạt động tương tự như `cpu_percent()`, nhưng trả về phần trăm sử dụng cho từng loại thời gian CPU cụ thể, giống như dữ liệu từ `psutil.cpu_times(percpu=True)`. 

#### Tham số:
- **interval > 0.0**: Khi `interval` lớn hơn 0, hàm sẽ đợi khoảng thời gian `interval` rồi mới so sánh phần trăm sử dụng CPU giữa hai lần đo (blocking).
  
- **interval = 0.0 hoặc None**: Khi `interval` bằng 0.0 hoặc None, hàm sẽ so sánh phần trăm CPU sử dụng kể từ lần gọi trước hoặc từ lúc import thư viện và trả về ngay lập tức. Lưu ý rằng lần gọi đầu tiên sẽ trả về giá trị không có ý nghĩa và nên bỏ qua.
  
- **percpu**: Khi `percpu=True`, hàm trả về danh sách chứa phần trăm sử dụng CPU cho từng CPU logic. Mỗi phần tử trong danh sách đại diện cho một CPU, theo thứ tự lần lượt.

#### Phần trăm cho từng loại thời gian CPU:
Hàm này trả về `named tuple` với các trường tương tự `psutil.cpu_times()`, ví dụ:
- **user**: Phần trăm thời gian thực hiện các tiến trình ở chế độ người dùng.
- **system**: Phần trăm thời gian thực hiện các tiến trình ở chế độ nhân.
- **idle**: Phần trăm thời gian CPU không hoạt động.

Lưu ý: Trên Linux, phần trăm cho `guest` và `guest_nice` không tính vào phần trăm của `user` và `user_nice`.
### 4. `psutil.cpu_count(logical=True)`
Hàm `psutil.cpu_count()` trả về số lượng CPU logic (số lõi vật lý nhân với số luồng trên mỗi lõi, hay còn gọi là Hyper-Threading).

- **logical=True** (mặc định): Trả về số lượng CPU logic trong hệ thống. Nếu không xác định được, hàm trả về `None`. `logical CPUs` là tổng số lõi nhân với số luồng trên mỗi lõi. Ví dụ, một hệ thống có 2 lõi và mỗi lõi hỗ trợ 2 luồng sẽ có 4 CPU logic.

- **logical=False**: Trả về số lượng lõi vật lý (số CPU thực) trong hệ thống. Nếu không xác định được, hàm trả về `None`. Lưu ý, trên các hệ điều hành như OpenBSD và NetBSD, khi `logical=False`, hàm này luôn trả về `None`.

#### Ví dụ:
Trên một hệ thống với 2 lõi và mỗi lõi hỗ trợ 2 luồng:
```python
import psutil
psutil.cpu_count()
4        # Số CPU logic
psutil.cpu_count(logical=False)
2        # Số lõi vật lý
### psutil.cpu_stats()
```
### 5. `psutil.cpu_stats()`
Hàm `psutil.cpu_stats()` trả về các thông tin thống kê về CPU dưới dạng `named tuple`, bao gồm:

- **ctx_switches**: Số lần chuyển đổi ngữ cảnh (bao gồm chuyển đổi tự nguyện và không tự nguyện) kể từ khi hệ thống khởi động. Chuyển đổi ngữ cảnh xảy ra khi CPU chuyển quyền điều khiển từ một tiến trình sang tiến trình khác.
  
- **interrupts**: Số lần ngắt (interrupt) kể từ khi khởi động. Ngắt xảy ra khi các thiết bị phần cứng hoặc phần mềm yêu cầu CPU dừng thực thi một tác vụ để xử lý các tác vụ ưu tiên cao hơn.

- **soft_interrupts**: Số lần ngắt phần mềm kể từ khi khởi động. Giá trị này luôn là 0 trên Windows và SunOS.

- **syscalls**: Số lượng lệnh gọi hệ thống kể từ khi khởi động. Trên Linux, giá trị này luôn là 0.

#### Ví dụ
```python
import psutil
psutil.cpu_stats()
scpustats(ctx_switches=20455687, interrupts=6598984, soft_interrupts=2134212, syscalls=0)
```
### 6. `psutil.cpu_freq(percpu=False)`

Hàm `psutil.cpu_freq()` trả về tần số CPU hiện tại dưới dạng `named tuple`, với các trường:
- **current**: Tần số hiện tại của CPU (tính theo MHz).
- **min**: Tần số thấp nhất mà CPU có thể đạt được (MHz). Nếu không xác định được, giá trị là `0.0`.
- **max**: Tần số cao nhất mà CPU có thể đạt được (MHz). Nếu không xác định được, giá trị là `0.0`.

#### Tham số
- **percpu=False** (mặc định): Khi `percpu=False`, hàm trả về tần số hiện tại của hệ thống. Trên Linux, giá trị tần số là giá trị thời gian thực, còn trên các hệ điều hành khác, nó thường là giá trị cố định và không thay đổi.

- **percpu=True**: Khi `percpu=True` và hệ thống hỗ trợ việc lấy tần số của từng CPU riêng lẻ (Linux và FreeBSD), hàm trả về danh sách tần số cho mỗi CPU logic.
#### Ví dụ
```python
import psutil
psutil.cpu_freq()
scpufreq(current=931.42925, min=800.0, max=3500.0)
psutil.cpu_freq(percpu=True)
[scpufreq(current=2394.945, min=800.0, max=3500.0),
 scpufreq(current=2236.812, min=800.0, max=3500.0),
 scpufreq(current=1703.609, min=800.0, max=3500.0),
 scpufreq(current=1754.289, min=800.0, max=3500.0)]
 ```
### 7. `psutil.getloadavg()`

Hàm `psutil.getloadavg()` trả về mức tải trung bình của hệ thống trong 1 phút, 5 phút, và 15 phút gần nhất dưới dạng một `tuple`. 

- **Mức tải (load)**: Đại diện cho số lượng tiến trình đang ở trạng thái có thể chạy (runnable), bao gồm các tiến trình đang sử dụng CPU hoặc đang chờ tài nguyên (ví dụ: đợi I/O từ đĩa cứng).

#### Hoạt động trên các hệ điều hành:
- **UNIX**: Hàm dựa vào `os.getloadavg()` để thu thập thông tin.
- **Windows**: Mức tải được giả lập bằng cách sử dụng API Windows. Khi gọi lần đầu, trong 5 giây đầu tiên, hàm sẽ trả về một `tuple` vô nghĩa `(0.0, 0.0, 0.0)` vì cần thời gian để cập nhật.

#### Ý nghĩa của giá trị:
- Các giá trị trong `tuple` cần được so sánh với số lượng CPU logic để có ý nghĩa. Ví dụ:
  - Nếu hệ thống có 10 CPU logic và mức tải là `3.14`, điều này có nghĩa hệ thống đang sử dụng 31.4% tài nguyên CPU trung bình trong 1 phút qua.

#### Ví dụ
```python
import psutil
psutil.getloadavg()
(3.14, 3.89, 4.67)  # Mức tải trung bình trong 1 phút, 5 phút và 15 phút
psutil.cpu_count()
10                  # Hệ thống có 10 CPU logic
# Chuyển đổi sang phần trăm
[x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
[31.4, 38.9, 46.7]  # Phần trăm sử dụng CPU trung bình
```