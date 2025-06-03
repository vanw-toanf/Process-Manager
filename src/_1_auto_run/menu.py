import npyscreen

class MenuForm(npyscreen.Form):
    def create(self):
        # self.welcome = self.add(npyscreen.TitleText, name="Welcome", value="Process Manager", editable=False)       
        # # Menu lựa chọn chức năng
        # self.menu_choice = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=4, 
        #                           name="Menu", values=["View Processes", "View Process Details", "Exit"])
        
        # # Khu vực hiển thị danh sách tiến trình (giả lập)
        # self.process_list = self.add(npyscreen.TitleMultiLine, name="Process List Preview", 
        #                            values=["PID: 1  Name: init", "PID: 2  Name: bash", "PID: 3  Name: python"], 
        #                            max_height=5, scroll_exit=True)

        height, width = self.lines, self.columns
        self.welcome = self.add(npyscreen.TitleText, name="Welcome", value="Process Manager", editable=False)
        self.menu_choice = self.add(npyscreen.TitleSelectOne, scroll_exit=True, 
                                  max_height=min(4, height-10), name="Menu", 
                                  values=["View Processes", "View Process Details", "Exit"])
        
        # Thêm BoxTitle như một sub-form cho danh sách tiến trình
        try:
            self.process_box = self.add(npyscreen.BoxTitle, name="Process List Preview",
                                       max_height=min(8, height-15), values=["PID: 1  Name: init", "PID: 2  Name: bash"],
                                       editable=True, scroll_exit=True)
        except npyscreen.wgwidget.NotEnoughSpaceForWidget:
            self.process_box = self.add(npyscreen.TitleText, name="Error", value="Not enough space for process list")

class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', MenuForm, name='PROCESS MANAGER')

if __name__ == '__main__':
   TestApp = MyApplication().run()

   