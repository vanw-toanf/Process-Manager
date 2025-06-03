import npyscreen

class MenuForm(npyscreen.FormWithMenus):
    def create(self):
        self.add(npyscreen.TitleText, name="Process Manager", editable=False)
        self.choice = self.add(
            npyscreen.TitleSelectOne,
            name="Select an option:",
            values=["View system resources", "Placeholder function", "Exit"],
            max_height=4,
            scroll_exit=True
        )
        self.main_menu = self.add_menu(name="Main Menu", shortcut="^M")
        self.main_menu.addItemsFromList([("Exit Application", self.exit_application, "^X")])
    
    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()
    
    def get_choice_and_return(self):
        return self.choice.value[0] if self.choice.value else -1
    
    def init_menu_window(self):
        return len(self.choice.values)
    
    def exit_menu_window(self):
        pass
    
    def update_menu_list(self):
        pass
    
    def push_to_screen(self):
        pass