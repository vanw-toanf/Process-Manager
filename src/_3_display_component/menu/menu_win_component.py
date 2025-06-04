"""
menu_win_component.py

This module defines the 'Main_win' class for rendering the menu using npyscreen.

Copyright (C) 2024  Giang Trinh.
"""

import npyscreen
from _3_display_component.container_class.container import Container

class Main_win(npyscreen.Form, Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Container.__init__(self)
        self.order_choice = ["PROCESSES", "about us"]
        self.max_num_choice = len(self.order_choice)
        self.numerical_order = 0

    def create(self):
        # Tiêu đề
        self.name = "Task Manager"

        # Hiển thị danh sách lựa chọn
        self.w_order = self.add(
            npyscreen.TitleMultiLine,
            name="Menu Functions",
            values=self.order_choice,
            value=0,
            max_height=len(self.order_choice) + 2,
            scroll_exit=True
        )
        self.w_order.when_value_edited = self.update_order

        # Hiển thị hướng dẫn sử dụng
        self.w_guide = self.add(
            npyscreen.BoxTitle,
            name="How to use",
            values=["w-Up | s-Down", "q-Quit | Enter-Select"],
            max_height=4,
            editable=False
        )

    def update_order(self):
        self.numerical_order = self.w_order.value

    def get_order(self):
        return self.numerical_order

    def order_down(self):
        self.numerical_order = (self.numerical_order + 1) % self.max_num_choice
        self.w_order.value = self.numerical_order
        self.w_order.display()

    def order_top(self):
        self.numerical_order = (self.numerical_order - 1) % self.max_num_choice
        self.w_order.value = self.numerical_order
        self.w_order.display()