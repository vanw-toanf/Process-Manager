"""
CRP_win_component.py

This module defines the CRPwin class for displaying system process information using npyscreen.

Copyright (C) 2024  Giang Trinh.
"""

import npyscreen
from _3_display_component.container_class.container import Container
from _4_system_data import CRP_control

class CRPwin(npyscreen.Form, Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Container.__init__(self)
        self.len_order_list = 10  # Số lượng process hiển thị tối đa
        self.num_order_insert = 0
        self.offset_list_proc = 0
        self.current_order_proc = 0
        self.sort_order = 0

    def create(self):
        self.name = "Process Manager"

        # Danh sách process
        self.w_proc = self.add(
            npyscreen.GridColTitles,
            name="Processes",
            col_titles=["PID", "NAME", "CPU%", "MEM%", "STATUS", "TIME"],
            values=[],
            select_whole_line=True,
            max_height=self.len_order_list + 2
        )

        # Thông tin tổng quan
        self.w_total = self.add(
            npyscreen.BoxTitle,
            name="Total",
            values=[],
            max_height=5,
            editable=False
        )

        # Hướng dẫn sử dụng
        self.w_guide = self.add(
            npyscreen.BoxTitle,
            name="How to use",
            values=["w-Up | s-Down", "c-Catch | Enter-More info", "q-Quit | m-Menu"],
            max_height=5,
            editable=False
        )

        # Cập nhật dữ liệu ban đầu
        self.renew_list_processes(self.sort_order)
        self.update_proc_content()
        self.update_total_content()

    def renew_list_processes(self, sort_order):
        CRP_control.sort_order = sort_order
        CRP_control.get_list_proc()
        if (self.offset_list_proc + self.num_order_insert) <= CRP_control.leng_proc:
            self.num_order_insert = self.len_order_list
        else:
            if CRP_control.leng_proc >= self.len_order_list:
                self.num_order_insert = self.len_order_list
                self.offset_list_proc = CRP_control.leng_proc - self.num_order_insert
            else:
                self.num_order_insert = CRP_control.leng_proc
                self.offset_list_proc = 0
                if self.current_order_proc > self.num_order_insert - 1:
                    self.current_order_proc = self.num_order_insert - 1

    def update_proc_content(self):
        insert_list = CRP_control.list_proc[self.offset_list_proc: self.offset_list_proc + self.num_order_insert]
        self.w_proc.values = [
            [p["pid"], p["name"][:35], p["cpu_percent"], p["memory_percent"], p["status"], p["create_time"]]
            for p in insert_list
        ]
        self.w_proc.highlighted_row = self.current_order_proc
        self.w_proc.display()

    def update_total_content(self):
        CRP_control.get_dict_total_resource()
        self.w_total.values = [
            f"PID {CRP_control.total_resource_info['total_pid']} | Run {CRP_control.total_resource_info['running']} | CPU {CRP_control.total_resource_info['cpu_percent']:.2f}%",
            f"Slp {CRP_control.total_resource_info['sleeping']} | Stp {CRP_control.total_resource_info['stopped']} | RAM {CRP_control.total_resource_info['total_ram']}MB",
            f"NOW {CRP_control.total_resource_info['current_time']} | Zom {CRP_control.total_resource_info['zombie']} | USE {CRP_control.total_resource_info['used_ram']}MB"
        ]
        self.w_total.display()

    def move_order_up(self):
        if self.current_order_proc == 0:
            if self.offset_list_proc == 0:
                return
            else:
                self.offset_list_proc -= 1
        else:
            self.current_order_proc -= 1
        self.update_proc_content()

    def move_order_down(self):
        o_plus_a = self.offset_list_proc + self.len_order_list
        if o_plus_a < CRP_control.leng_proc:
            self.num_order_insert = self.len_order_list
            if self.current_order_proc == self.num_order_insert - 1:
                self.offset_list_proc += 1
            else:
                self.current_order_proc += 1
        else:
            self.num_order_insert = CRP_control.leng_proc - self.offset_list_proc
            if self.current_order_proc == self.num_order_insert - 1:
                return
            else:
                self.current_order_proc += 1
        self.update_proc_content()