import logging


class Colors:
    COLORS = {
        "header": '\033[95m',
        "blue": '\033[94m',
        "green": '\033[92m',
        "yellow": '\033[93m',
        "red": '\033[91m',
        "end": '\033[0m'
    }


class Logger:
    def __init__(self, log_path):
        # Thiết lập logger với tên "my_logger"
        self.logger = logging.getLogger("my_logger")
        self.logger.setLevel(logging.DEBUG)  # Mức log

        # Kiểm tra xem logger đã có handler chưa để tránh thêm trùng lặp
        if not self.logger.handlers: # <--- DÒNG NÀY ĐÃ ĐƯỢC THÊM VÀO
            # Tạo file handler để ghi log vào file
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.DEBUG)

            # Định dạng log
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Gắn file handler vào logger
            self.logger.addHandler(file_handler)

    def log_info(self, message, extra=None): # <--- THÊM extra=None để tương thích
        self.logger.info(message, extra=extra)

    def log_warning(self, message, extra=None): # <--- THÊM extra=None
        self.logger.warning(message, extra=extra)

    def log_error(self, message, extra=None): # <--- THÊM extra=None
        self.logger.error(message, extra=extra)


def print_with_color(text, color):
    color_code = Colors.COLORS.get(color.lower(), Colors.COLORS["end"])
    print(f"{color_code}{text}{Colors.COLORS['end']}")