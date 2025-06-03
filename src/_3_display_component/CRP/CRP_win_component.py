"""
CRP_win_component.py

This module defines the CRPwin class, a subclass of the Container class,
which is designed to build and manage a curses-based window for displaying
system process information.

The CRPwin class provides methods for constructing basic display layouts
and rendering the information about active system processes, as well as overall
statistics such as total processes, CPU usage, and RAM utilization.

Copyright (C) 2024  Giang Trinh.

This file is part of the Process Manager project and is licensed
under the GNU General Public License v3 or later.
"""


'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
from _3_display_component.container_class.container import Container
from _4_system_data import CRP_control
'''****************************************************************************
* Variable
****************************************************************************'''
# inherit the 'Container' class
class CRPwin(Container):
    # Initialize display windows
    def __init__(self):
        #Variable and constant
        ##[process window]
        #include: name, Pid, %CPU, %RAM, Status, time using
        self.w_proc_begin_col = None; self.w_proc_begin_row = None
        self.w_proc_col = None; self.w_proc_row = None

        # a, b, o, current_order
        self.len_order_list = None #a
        self.num_order_insert = 0 #b
        self.offset_list_proc = 0; self.current_order_proc = 0 # o, current

        self.col_proc_PID  = None;self.col_proc_NAME = None
        self.col_proc_CPU  = None;self.col_proc_MEM  = None
        self.col_proc_STATUS = None;self.col_proc_TIME = None
        self.col_proc_endmark = None

        #total window
        self.w_total_begin_col = None; self.w_total_begin_row = None
        self.w_total_col = None; self.w_total_row = None

        self.col_total_PID=None; self.col_total_Run=None; self.col_total_Slp=None
        self.col_total_Stp=None; self.col_total_Zom=None; self.col_total_NOW=None
        self.col_total_CPU=None; self.col_total_RAM=None; self.col_total_USE=None

        #guide window
        self.w_guide_begin_col = None; self.w_guide_begin_row = None
        self.w_guide_col = None; self.w_guide_row = None

        # window variable
        self.w_proc = None; self.w_total = None; self.w_guide = None

        # init backwindow
        Container.__init__(self)

        # calculate sub win size and coordinate content, prepare content
        self.cal_size_sub_window()

        self.calculate_coordinate_list_proc_content()
        self.renew_list_processes(sort_order=0)

        self.calculate_coordinate_total_content()

        # init sub window
        self.w_proc = curses.newwin(self.w_proc_row,self.w_proc_col,
                                     self.w_proc_begin_row,self.w_proc_begin_col)
        self.w_total = curses.newwin(self.w_total_row,self.w_total_col,
                                     self.w_total_begin_row,self.w_total_begin_col)
        self.w_guide = curses.newwin(self.w_guide_row,self.w_guide_col,
                                     self.w_guide_begin_row,self.w_guide_begin_col)
        
        # now add keypad(True)
        self.w_proc.keypad(True); self.w_total.keypad(True); self.w_guide.keypad(True)

        # add no delay for using getch()
        self.w_proc.nodelay(True); self.w_total.nodelay(True); self.w_guide.nodelay(True)

    def __del__(self):
        Container.__del__(self)



    '''_______________[interract with window]___________'''
    # [A. calculate and re-set size window]
    def cal_size_sub_window(self):
        # row: 100% = 10% top border + 50% menu + 10% free space + 20% guide + 10% bottom border (guard)
        # tips: increase % bottom border for 
        # reduce the overflow rate (error) due to not having time to recalculate

        #proc window
        self.w_proc_begin_col = self.back_win_col * 10 // 100
        self.w_proc_begin_row = self.back_win_row * 10 // 100
        self.w_proc_col = self.back_win_col * 80 // 100 #> 60block
        self.w_proc_row = self.back_win_row * 55 // 100

        #guide window
        self.w_guide_begin_col = self.back_win_col * 10 // 100
        self.w_guide_begin_row = self.back_win_row * 70 // 100
        self.w_guide_col = self.back_win_col * 31 // 100 #>=24block
        self.w_guide_row = self.back_win_row * 23 // 100

        #total window
        self.w_total_begin_col = self.back_win_col * 45 // 100
        self.w_total_begin_row = self.back_win_row * 70 // 100
        self.w_total_col = self.back_win_col * 45 // 100 # >35 block
        self.w_total_row = self.back_win_row * 23 // 100

    # clear all window
    def clear_all_window(self):
        self.backwin.clear()
        self.w_proc.clear()
        self.w_total.clear()
        self.w_guide.clear()

    #[B. Process window]
    #calculate_coordinate_list_proc_content and length order list
    def calculate_coordinate_list_proc_content(self):
        #1+1+7+1+16+1+5+1+5+1+10+1+8+1
        self.col_proc_PID  = 2
        self.col_proc_NAME = self.w_proc_col*17 // 100
        self.col_proc_CPU  = self.w_proc_col*43 // 100
        self.col_proc_MEM  = self.w_proc_col*52 // 100
        self.col_proc_STATUS = self.w_proc_col*62 // 100
        self.col_proc_TIME = self.w_proc_col*79 // 100
        self.col_proc_endmark = self.w_proc_col*98 // 100

        #calculate length orderlist
        self.len_order_list = self.w_proc_row-2

    # update list process 
    # first time run need 'calculate_coordinate_list_proc_content' to get len_order_list
    # (T2.1) 
    def renew_list_processes(self, sort_order):
        # require sort by index
        CRP_control.sort_order = sort_order

        # get newest data
        CRP_control.get_list_proc()
        # ? o+b <= c
        if (self.offset_list_proc + self.num_order_insert) <= CRP_control.leng_proc:
            self.num_order_insert = self.len_order_list
            return
        else:
            if CRP_control.leng_proc >= self.len_order_list:
                self.num_order_insert = self.len_order_list
                self.offset_list_proc = CRP_control.leng_proc - self.num_order_insert
                return
            else:
                self.num_order_insert = CRP_control.leng_proc
                self.offset_list_proc = 0
                if self.current_order_proc > self.num_order_insert - 1:
                    self.current_order_proc = self.num_order_insert - 1
                    return
                else:
                    return

    # Update content according to the displayed algorithm flow chart
    # (T2.2)
    def update_proc_content(self):
        #get data by slicing from listprocesses[o;o+b)
        insert_list = CRP_control.list_proc[self.offset_list_proc: self.offset_list_proc+self.num_order_insert]

        #clear screen first
        self.w_proc.clear()

        # renew border
        self.w_proc.box('|','-')
        # add name
        self.w_proc.addstr(0,self.col_proc_PID,    "|PID-0",curses.A_BOLD)
        self.w_proc.addstr(0,self.col_proc_NAME,   "|NAME-1",curses.A_BOLD)
        self.w_proc.addstr(0,self.col_proc_CPU,    "|CPU-2",curses.A_BOLD)
        self.w_proc.addstr(0,self.col_proc_MEM,    "|MEM-3",curses.A_BOLD)
        self.w_proc.addstr(0,self.col_proc_STATUS, "|STATUS-4",curses.A_BOLD)
        self.w_proc.addstr(0,self.col_proc_TIME,   "|TIME-5",curses.A_BOLD)
        self.w_proc.addstr(0,self.col_proc_endmark,"|",curses.A_BOLD)

        # add data
        temp_count = 0
        insert_line = 1
        for p in insert_list:
            if temp_count != self.current_order_proc:
                self.w_proc.addstr(insert_line,self.col_proc_PID,    "|{}".format(p["pid"]))
                self.w_proc.addstr(insert_line,self.col_proc_NAME,   "|{}".format(p["name"][:35]))#max name len = 35
                self.w_proc.addstr(insert_line,self.col_proc_CPU,    "|{}".format(p["cpu_percent"]))
                self.w_proc.addstr(insert_line,self.col_proc_MEM,    "|{}".format(p["memory_percent"]))
                self.w_proc.addstr(insert_line,self.col_proc_STATUS, "|{}".format(p["status"]))
                self.w_proc.addstr(insert_line,self.col_proc_TIME,   "|{}".format(p["create_time"]))
            else:
                self.w_proc.addstr(insert_line,self.col_proc_PID,    "|{}".format(p["pid"]),self.COS[2])
                self.w_proc.addstr(insert_line,self.col_proc_NAME,   "|{}".format(p["name"][:35]),self.COS[2])
                self.w_proc.addstr(insert_line,self.col_proc_CPU,    "|{}".format(p["cpu_percent"]),self.COS[2])
                self.w_proc.addstr(insert_line,self.col_proc_MEM,    "|{}".format(p["memory_percent"]),self.COS[2])
                self.w_proc.addstr(insert_line,self.col_proc_STATUS, "|{}".format(p["status"]),self.COS[2])
                self.w_proc.addstr(insert_line,self.col_proc_TIME,   "|{}".format(p["create_time"]),self.COS[2])
            temp_count +=1
            insert_line +=1

        # noutrefresh display
        self.w_proc.noutrefresh()

    # move up
    # (T3.2)
    def move_order_up(self):
        if self.current_order_proc == 0:
            if self.offset_list_proc == 0:
                return
            else:
                self.offset_list_proc -= 1
        else:
            self.current_order_proc -= 1
        
        # update content processes to buffer
        self.update_proc_content()

    # move down
    # (T3.1)
    def move_order_down(self):
        o_plus_a = self.offset_list_proc + self.len_order_list
        if o_plus_a < CRP_control.leng_proc:
            self.num_order_insert = self.len_order_list
            if self.current_order_proc == self.num_order_insert - 1:
                self.offset_list_proc+=1
            else:
                self.current_order_proc+=1
        else: # o+a >= c
            self.num_order_insert = CRP_control.leng_proc - self.offset_list_proc
            if self.current_order_proc == self.num_order_insert - 1:
                return
            else:
                self.current_order_proc+=1
        
        # update content processes to buffer
        self.update_proc_content()


    #[C. Total resource window]
    # calculate after calculate size window
    # demo
    # self.w_total.addstr(1,1,"PID:      |Run:      |CPU:     ")
    # self.w_total.addstr(2,1,"Slp:      |Stp:      |RAM:     ")
    # self.w_total.addstr(3,1,"NOW:      |Zom:      |USE:     ")
    def calculate_coordinate_total_content(self):
        self.col_total_PID = 1
        self.col_total_Run = self.w_total_col // 3 +1
        self.col_total_Slp = 1
        self.col_total_Stp = self.w_total_col // 3 +1
        self.col_total_Zom = self.w_total_col // 3 +1

        self.col_total_NOW = 1

        self.col_total_CPU = self.w_total_col * 2 // 3 +1
        self.col_total_RAM = self.w_total_col * 2 // 3 +1
        self.col_total_USE = self.w_total_col * 2 // 3 +1


    def update_total_content(self):
        #get total data
        CRP_control.get_dict_total_resource()

        #clear screen first
        self.w_total.clear()

        # set total data
        self.w_total.addstr(1,self.col_total_PID,"PID {}".format(CRP_control.total_resource_info["total_pid"]),curses.A_BOLD)
        self.w_total.addstr(1,self.col_total_Run,"Run {}".format(CRP_control.total_resource_info["running"]),curses.A_BOLD)
        self.w_total.addstr(1,self.col_total_CPU,"CPU {:.2f}%".format(CRP_control.total_resource_info["cpu_percent"]),self.COS[5])
        self.w_total.addstr(2,self.col_total_Slp,"Slp {}".format(CRP_control.total_resource_info["sleeping"]),curses.A_BOLD)
        self.w_total.addstr(2,self.col_total_Stp,"Stp {}".format(CRP_control.total_resource_info["stopped"]),curses.A_BOLD)
        self.w_total.addstr(2,self.col_total_RAM,"RAM {}MB".format(CRP_control.total_resource_info["total_ram"]),self.COS[3])
        self.w_total.addstr(3,self.col_total_Zom,"Zom {}".format(CRP_control.total_resource_info["zombie"]),curses.A_BOLD)
        self.w_total.addstr(3,self.col_total_NOW,"NOW {}".format(CRP_control.total_resource_info["current_time"]))
        self.w_total.addstr(3,self.col_total_USE,"USE {}MB".format(CRP_control.total_resource_info["used_ram"]),self.COS[3])

        # renew border
        self.w_total.box('|','-')
        # add name
        self.w_total.addstr(0,1,"[Total]", self.COS[2])
        # noutrefresh display
        self.w_total.noutrefresh()


    #[.static window display]
    #[D. guide users window]
    def update_guide(self):
        # add content
        self.w_guide.addstr(1,1,"w-Up   |s-Down")
        self.w_guide.addstr(2,1,"c-Catch|ent-More info")
        self.w_guide.addstr(3,1,"q-Quit |m-Menu")

        # renew border
        self.w_guide.box('|','-')
        # add name
        self.w_guide.addstr(0,1,"[How to use]", self.COS[1])
        # noutrefresh display
        self.w_guide.noutrefresh()

    #[E. background]
    def update_background(self):
        # renew border
        self.backwin.box('|','-')
        #add name
        self.backwin.addstr(0,1,"[Process Manager]",self.COS[4])
        #noutrefresh to apply new change
        self.backwin.noutrefresh()
