import npyscreen
import curses

class MyForm(npyscreen.Form):
    def create(self):
        self.my_text = self.add(npyscreen.TitleText, name="Enter Text:")

    def handle_enter(self, *args, **keywords):
        npyscreen.notify_wait("You pressed Enter!")

    def while_editing(self, *args, **keywords):
        self.my_text.entry_widget.add_handlers({
            curses.KEY_ENTER: self.handle_enter
        })

class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MyForm, name="My Form")

if __name__ == "__main__":
    app = MyApplication().run()