import npyscreen
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from _2_display_module.resource.resource_layout import ResourceBox
from _2_display_module.menu.menu_layout import MenuBox
from _2_display_module.process.process_layout import ProcessBox

class MainForm(npyscreen.Form):
    OK_BUTTON_TEXT = "Exit"
    def create(self):
        height, width = self.lines, self.columns
        self.welcome = self.add(npyscreen.TitleText, name="Welcome", value="This is Process Manager App", editable=False)
        
        
        try:
            self.add(ProcessBox, max_height=15)
            self.add(MenuBox, relx=2, rely=18, max_width=int(width * 0.35), max_height=6)
            self.add(ResourceBox, relx=2+int(width*0.36), rely=18, max_height=6)
        except npyscreen.wgwidget.NotEnoughSpaceForWidget:
            self.process_box = self.add(npyscreen.TitleText, name="Error", value="Not enough space for process list")

        self.next_form = None
        self.add(npyscreen.ButtonPress, name="Go to Second Form", when_pressed_function=self.go_to_second_form)

    def beforeEditing(self):
        self.next_form = None
    def go_to_second_form(self):
        self.next_form = 'SECOND'
        self.editing = False
    def afterEditing(self):
        if self.next_form:
            self.parentApp.setNextForm(self.next_form)
        else:
            self.parentApp.setNextForm(None)
class SecondForm(npyscreen.Form):
    OK_BUTTON_TEXT = "Back"
    def create(self):
        self.add(npyscreen.TitleText, name="Second Form", value="This is the Second Form", editable=False)
        # Thêm một số widget mẫu
        self.add(npyscreen.TitleText, name="Sample", value="Hello from Second Form!")
        # Thêm nút để quay lại MenuForm
        self.add(npyscreen.ButtonPress, name="Back to Main Form", when_pressed_function=self.switch_to_main_form)
    
    def switch_to_main_form(self):
        self.parentApp.switchForm('MAIN')

    def afterEditing(self):
        self.parentApp.switchForm('MAIN')
class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', MainForm, name='PROCESS MANAGER SYSTEM')
       self.addForm('SECOND', SecondForm, name='SECOND FORM')

if __name__ == '__main__':
   TestApp = MyApplication().run()