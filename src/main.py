import npyscreen
from _2_display_module.resource.resource_layout import ResourceBox

class MenuForm(npyscreen.Form):
    def create(self):
        width = self.columns
        self.add(ResourceBox, relx=int(width * 0.5), rely=2, max_width=40, max_height=10)

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MenuForm, name='Demo')

if __name__ == '__main__':
    App().run()
