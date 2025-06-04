"""
container.py

This module defines the 'Container' class, which sets up and manages
the base environment for npyscreen-based applications.

Copyright (C) 2024  Giang Trinh.
"""

class Container:
    def __init__(self):
        # Danh sách màu hoặc style (dùng cho npyscreen)
        self.COS = [
            "DANGER",  # red (for alert)
            "GOOD",    # magenta (for guide)
            "CURSOR",  # blue (for suggest)
            "WARNING", # yellow (for highlight)
            "LABEL",   # green (for highlight)
            "NOTICE",  # cyan (for notification)
        ]
    
    def Hello_World(self):
        # Hàm này có thể không cần thiết nữa vì npyscreen không cần vẽ thủ công
        # Nếu cần hiển thị tiêu đề, bạn có thể tích hợp vào form của npyscreen
        pass