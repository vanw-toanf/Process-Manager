import npyscreen
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from _2_display_module.resource.resource_layout import ResourceBox
from _2_display_module.menu.menu_layout import MenuBox
from _2_display_module.process.process_layout import ProcessBox
from _2_display_module.process.process_detail_layout import AutoUpdateProcessBox, ProcessMonitorForm

from _1_auto_run.running_process import start_CRP_threads, destroy_CRP_threads, pause_CRP_threads, resume_CRP_threads
from _4_system_data import CRP_control
from log.log import Logger
log = Logger(os.path.abspath("app.log"))
class MainForm(npyscreen.Form):
    OK_BUTTON_TEXT = "Exit"
    
    def create(self):
        self._exit_to_second = False
        self._selected_pid = None
        self.next_form = None
        height, width = self.useable_space()
        log.log_info(f"Terminal size: {width}x{height}")

        min_height, min_width = 24, 80

        # Kiểm tra kích thước terminal
        if height < min_height or width < min_width:
            warning = (
                f"⚠️ Terminal quá nhỏ ({width}x{height}).\n"
                f"Cần ít nhất {min_width}x{min_height} để hiển thị đầy đủ.\n"
                f"Vui lòng mở rộng terminal rồi chạy lại."
            )
            self.add(npyscreen.TitleFixedText, name="CẢNH BÁO", value=warning)
            self.disable_form = True  # 🔧 Cờ để tránh xử lý widget tiếp theo
            return
        else:
            self.disable_form = False

        # Giao diện chính
        self.welcome = self.add(npyscreen.TitleText, name="Welcome", value="This is Process Manager App", editable=False)

        try:
            self.process_box = self.add(ProcessBox, max_height=15)

            self.add(MenuBox, relx=2, rely=18, max_width=int(width * 0.35), max_height=6)

            self.resource_box = self.add(ResourceBox, relx=2 + int(width * 0.36), rely=18, max_height=6)

            start_CRP_threads(self.process_box, self.resource_box)

        except npyscreen.wgwidget.NotEnoughSpaceForWidget:
            self.process_box = self.add(npyscreen.TitleText, name="Error", value="Not enough space for process list")

        # Nút chuyển form
        self.add(npyscreen.ButtonPress, name="Go to Second Form", when_pressed_function=self.go_to_second_form)

    def beforeEditing(self):
        if getattr(self, 'disable_form', False):
            return
        self.process_box.is_visible = True
        self.resource_box.is_visible = True
        self._exit_to_second = False   # Reset lại để không tự động sang form 2
        resume_CRP_threads()
    def go_to_second_form(self):
        self.process_box.is_visible = False
        self.resource_box.is_visible = False
        pause_CRP_threads()
        self.next_form = 'SECOND'
        self.editing = False
    def afterEditing(self):
        if getattr(self, '_exit_to_second', False):
            second_form = self.parentApp.getForm('SECOND')
            second_form.process_box.set_pid(self._selected_pid)
            self.parentApp.setNextForm('SECOND')
            log.log_info("MainForm.afterEditing() -> SECOND")
        else:
            self.parentApp.setNextForm(None)
            log.log_info("MainForm.afterEditing() -> Exit")
    def on_ok(self):
        destroy_CRP_threads()
        self._exit_to_second = False
        self.parentApp.setNextForm(None)
        self.editing = False
    
    def on_process_selected(self, pid):
        log.log_info(f"MainForm.on_process_selected({pid}) called")
        self.process_box.is_visible = False
        self.resource_box.is_visible = False
        pause_CRP_threads()

        self._selected_pid = pid
        self._exit_to_second = True

    def while_waiting(self):
        if self._exit_to_second:
            log.log_info("MainForm.while_waiting(): exiting to SECOND")
            self.editing = False
            self.display()

class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
       self.addForm('MAIN', MainForm, name='PROCESS MANAGER SYSTEM')
       self.addForm('SECOND', ProcessMonitorForm)
    def onExit(self):
        destroy_CRP_threads()
        log.log_info("Ứng dụng đang thoát...", extra={'single': True})
        return super().onExit()

if __name__ == '__main__':
   TestApp = MyApplication().run()