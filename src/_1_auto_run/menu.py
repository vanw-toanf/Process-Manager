import npyscreen
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from _2_display_module.resource.resource_layout import ResourceBox
from _2_display_module.menu.menu_layout import MenuBox
from _2_display_module.process.process_layout import ProcessBox

class MenuForm(npyscreen.Form):
    def create(self):
        height, width = self.lines, self.columns
        self.welcome = self.add(npyscreen.TitleText, name="Welcome", value="This is Process Manager App", editable=False)

        try:
            self.add(ProcessBox, max_height=15)
            self.add(MenuBox, relx=2, rely=18, max_width=int(width * 0.35), max_height=6)
            self.add(ResourceBox, relx=2+int(width*0.36), rely=18, max_height=6)
        except npyscreen.wgwidget.NotEnoughSpaceForWidget:
            self.process_box = self.add(npyscreen.TitleText, name="Error", value="Not enough space for process list")

class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', MenuForm, name='PROCESS MANAGER')

if __name__ == '__main__':
   TestApp = MyApplication().run()