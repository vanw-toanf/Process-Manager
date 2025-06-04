# Threading trong Python

## 1. Giới thiệu về Threading
Threading cho phép thực thi đồng thời các tác vụ trong Python. Mặc dù **Global Interpreter Lock (GIL)** của Python ngăn chặn việc thực thi song song thực sự của các thread trong các tác vụ CPU-bound (tính toán nặng), nhưng nó vẫn rất hữu ích cho các tác vụ I/O-bound và cần xử lý đồng thời.

## 2. Tạo và khởi chạy Thread
Python cung cấp module `threading` để tạo và quản lý các thread.

### Ví dụ: Tạo Thread
```python  
import threading

def worker_function(name):
    print(f"Thread {name} đang chạy")

# Tạo thread
thread1 = threading.Thread(target=worker_function, args=("A",))
thread2 = threading.Thread(target=worker_function, args=("B",))

# Khởi chạy thread
thread1.start()
thread2.start()

# Chờ cho các thread hoàn thành
thread1.join()
thread2.join()

print("Tất cả các thread đã hoàn thành")
```

## 3. An toàn và Đồng bộ Thread

Khi nhiều thread cùng truy cập vào dữ liệu chung, bạn cần đảm bảo tính an toàn của thread thông qua các cơ chế đồng bộ như Lock.  
Đi kèm với lock là sử dụng 'with' để tạo cơ chế gọi context manager thông qua tự động gọi
các hàm **__enter__** và **__exit__**  
### 3.1. Sử dụng Lock

Lock đảm bảo chỉ một thread có thể truy cập vào phần mã quan trọng tại một thời điểm.
Ví dụ: Sử dụng Lock  
```python  
lock = threading.Lock()
shared_resource = 0

def increment_resource():
    global shared_resource
    with lock:  # Tự động khóa và giải phóng lock
        for _ in range(1000):
            shared_resource += 1

threads = [threading.Thread(target=increment_resource) for _ in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Giá trị cuối cùng của tài nguyên chung: {shared_resource}")
```

### 3.2. Sử dụng RLock

RLock (Reentrant Lock) cho phép cùng một thread có thể acquire (khóa) một lock nhiều lần mà không gây ra deadlock.
Ví dụ: Sử dụng RLock  
```python  
rlock = threading.RLock()

def recursive_task(n):
    with rlock:
        if n > 0:
            print(f"Công việc cấp độ {n}")
            recursive_task(n - 1)

recursive_task(3)
```

## 4. Thread Daemon

Daemon threads chạy nền và tự động kết thúc khi chương trình chính thoát.
Ví dụ: Daemon Thread
```python  
import time

def background_task():
    while True:
        print("Công việc nền đang chạy")
        time.sleep(1)

thread = threading.Thread(target=background_task, daemon=True)
thread.start()

time.sleep(5)
print("Chương trình chính thoát, daemon thread sẽ kết thúc")
```

### 5. Giao tiếp giữa các Thread

Các thread có thể giao tiếp và chia sẻ dữ liệu thông qua các biến chung hoặc các hàng đợi (queue) thread-safe.
Ví dụ: Sử dụng Queue
```python
#Module queue cung cấp cách an toàn để chia sẻ dữ liệu giữa các thread.

from queue import Queue

def producer(queue):
    for i in range(5):
        queue.put(i)
        print(f"Đã sản xuất: {i}")

def consumer(queue):
    while not queue.empty():
        item = queue.get()
        print(f"Đã tiêu thụ: {item}")

q = Queue()
producer_thread = threading.Thread(target=producer, args=(q,))
consumer_thread = threading.Thread(target=consumer, args=(q,))

producer_thread.start()
producer_thread.join()

consumer_thread.start()
consumer_thread.join()
```
