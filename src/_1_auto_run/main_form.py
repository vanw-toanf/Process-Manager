import npyscreen
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from _2_display_module.resource.resource_layout import ResourceBox
from _2_display_module.menu.menu_layout import MenuBox
from _2_display_module.process.process_layout import ProcessBox
from _2_display_module.process.process_detail_layout import AutoUpdateProcessBox, ProcessMonitorForm

from _1_auto_run.running_process import start_CRP_threads, destroy_CRP_threads
from _4_system_data import CRP_control
class MainForm(npyscreen.Form):
    OK_BUTTON_TEXT = "Exit"
    def create(self):
        height, width = self.lines, self.columns
        self.welcome = self.add(npyscreen.TitleText, name="Welcome", value="This is Process Manager App", editable=False)
        
        try:
            # self.add(ProcessBox, max_height=15)
            self.process_box = self.add(ProcessBox, max_height=15)
            
            self.add(MenuBox, relx=2, rely=18, max_width=int(width * 0.35), max_height=6)
            self.resource_box = self.add(ResourceBox, relx=2+int(width*0.36), rely=18, max_height=6)
            start_CRP_threads(self.process_box, self.resource_box)
            
        except npyscreen.wgwidget.NotEnoughSpaceForWidget:
            self.process_box = self.add(npyscreen.TitleText, name="Error", value="Not enough space for process list")
        
        self.next_form = None
        self.add(npyscreen.ButtonPress, name="Go to Second Form", when_pressed_function=self.go_to_second_form)

    def beforeEditing(self):
        start_CRP_threads(self.process_box, self.resource_box)
    def go_to_second_form(self):
        destroy_CRP_threads()
        self.next_form = 'SECOND'
        self.editing = False
    def afterEditing(self):
        destroy_CRP_threads()
        if self.next_form:
            self.parentApp.setNextForm(self.next_form)
        else:
            self.parentApp.setNextForm(None)

    def on_ok(self):
        destroy_CRP_threads()
        self.parentApp.setNextForm(None)
        self.editing = False

class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
       self.addForm('MAIN', MainForm, name='PROCESS MANAGER SYSTEM')
       self.addForm('SECOND', ProcessMonitorForm, name='SECOND FORM')

if __name__ == '__main__':
   TestApp = MyApplication().run()