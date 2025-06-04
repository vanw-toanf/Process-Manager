"""
Process Manager: A program to manage and monitor system processes.
Copyright (C) 2024  Giang Trinh, VuongNQ, and the development team.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import npyscreen
import os
from _1_auto_run.auto_menu import menu_auto_run
from _1_auto_run.auto_CRP import CRP_auto_run
from error_code import *

class AboutUsForm(npyscreen.Form):
    def create(self):
        self.name = "About Us"
        # Đọc nội dung từ file about.txt
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "build_here/about.txt")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().splitlines()
        except Exception as e:
            content = [f"Error reading about.txt: {str(e)}"]

        # Hiển thị nội dung trong một BoxTitle
        self.about_content = self.add(
            npyscreen.BoxTitle,
            name="About Process Manager",
            values=content,
            max_height=10,
            editable=False
        )

        # Thêm nút quay lại
        self.add(npyscreen.ButtonPress, name="Back to Menu (Enter)", when_pressed_function=self.back_to_menu)

    def back_to_menu(self):
        self.parentApp.switchForm("MENU")

class ProcessManagerApp(npyscreen.NPSAppManaged):
    def onStart(self):
        # Khởi tạo các form
        self.menu_form = menu_auto_run
        self.crp_form = CRP_auto_run

        # Thêm form cho About Us
        self.addForm("MENU", self.create_menu_form, name="Task Manager")
        self.addForm("ABOUT", AboutUsForm, name="About Us")

    def create_menu_form(self):
        ret = self.menu_form()
        if ret == -1:  # Quit signal
            self.setNextForm(None)  # Thoát ứng dụng
        elif ret == 0:  # PROCESSES
            ret_crp = self.crp_form()
            if ret_crp == -1:  # Quit signal
                self.setNextForm(None)  # Thoát ứng dụng
        elif ret == 1:  # About Us
            self.switchForm("ABOUT")

    def main(self):
        # Bắt đầu với form menu
        self.switchForm("MENU")

if __name__ == "__main__":
    app = ProcessManagerApp()
    app.run()