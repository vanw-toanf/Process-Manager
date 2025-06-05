from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget

class SystemInfoBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0) 

        self.cpu_label = QLabel("CPU Total: N/A")
        self.ram_label = QLabel("RAM Total: N/A")
        self.swap_label = QLabel("Swap: N/A")

        self.layout.addWidget(self.cpu_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.ram_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.swap_label)

    def update_info(self, cpu_percent, mem_info, swap_info):
        self.cpu_label.setText(f"CPU Total: {cpu_percent:.1f}%")

        if mem_info:
            self.ram_label.setText(
                f"RAM: {mem_info['used_gb']:.2f}/{mem_info['total_gb']:.2f} GB ({mem_info['percent']}%)"
            )
        else:
            self.ram_label.setText("RAM Total: Error")

        if swap_info:
            self.swap_label.setText(
                f"Swap: {swap_info['used_gb']:.2f}/{swap_info['total_gb']:.2f} GB ({swap_info['percent']}%)"
            )
        elif swap_info is None: 
             self.swap_label.setText("Swap: Not available")
        else:
            self.swap_label.setText("Swap: Error")