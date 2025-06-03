"""
menu_win_component.py

This module defines the 'Main_win' class, a subclass of the Container class.
The Main_win class provides functionality to render and handle basic user interactions
for menu selection.

Copyright (C) 2024  Giang Trinh.

This file is part of the Process Manager project and is licensed
under the GNU General Public License v3 or later.
"""

'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
from _3_display_component.container_class.container import Container

'''****************************************************************************
* Code
****************************************************************************'''
class Main_win(Container):
    ''' ____________Initialize display windows____________'''
    def __init__(self):
        #Variable and constant
        #sub order window
        self.w_order_begin_col = None; self.w_order_begin_row = None
        self.w_order_col = None; self.w_order_row = None
        self.numerical_order = 0
        self.order_choice = ("PROCESSES", "about us")
        self.max_num_choice = len(self.order_choice)
        #sub guide window
        self.w_guide_begin_col = None; self.w_guide_begin_row = None
        self.w_guide_col = None; self.w_guide_row = None

        # window variable
        self.w_order = None; self.w_guide = None
        # init backwindow
        Container.__init__(self)
        # calculate sub win size
        self.cal_size_sub_window()
        # init sub window
        self.w_order = curses.newwin(self.w_order_row,self.w_order_col,
                                     self.w_order_begin_row,self.w_order_begin_col)
        self.w_guide = curses.newwin(self.w_guide_row,self.w_guide_col,
                                     self.w_guide_begin_row,self.w_guide_begin_col)

        # now add keypad(True)
        self.w_order.keypad(True); self.w_guide.keypad(True)

        # add no delay for using getch()
        self.w_order.nodelay(True); self.w_guide.nodelay(True)

    # De-init
    def __del__(self):
        Container.__del__(self)
            
    '''_______________[interract with window]___________'''
    # [A. calculate and re-set size window]
    def cal_size_sub_window(self):
        # row: 100% = 10% top border + 50% menu + 10% free space + 20% guide + 10% bottom border (guard)
        # tips: increase % bottom border for 
        # reduce the overflow rate (error) due to not having time to recalculate

        #order window
        self.w_order_begin_col = self.back_win_col * 10 // 100
        self.w_order_begin_row = self.back_win_row * 10 // 100
        self.w_order_col = self.back_win_col * 80 // 100
        self.w_order_row = self.back_win_row * 55 // 100

        #guide window
        self.w_guide_begin_col = self.back_win_col * 10 // 100
        self.w_guide_begin_row = self.back_win_row * 70 // 100
        self.w_guide_col = self.w_order_col
        self.w_guide_row = self.back_win_row * 23 // 100 #min 5.5 ~ 5 block

    # clear all window
    def clear_all_window(self):
        self.backwin.clear()
        self.w_order.clear()
        self.w_guide.clear()

    # [C. order menu for order window]
    
    def update_order(self):
        #clear screen first
        self.w_order.clear()
        #empty space order window
        available_space = self.w_order_row - 2
        #if order display > numerical_order
        offset = None #ofset of list 'order_choice'
        peak = None #peak of list cut out of list 'order_choice'
        #calculate offset
        if (available_space > self.numerical_order):
            offset = 0
        else:#display with offset
            # offset = self.numerical_order + 1 - available_space
            offset = self.numerical_order - available_space + 1
        # peak = offset + available_space -1
        peak = offset + available_space - 1
        i=0
        for item in self.order_choice:
            #check out of range
            if(i<offset):
                i+=1 #increase i
                continue
            elif i>peak:
                break
            # print
            if(i == self.numerical_order):#if current order, highlight it
                self.w_order.addstr(i+1-offset,2,item,curses.A_REVERSE)
            else:
                self.w_order.addstr(i+1-offset,2,item)
                
            #increase i
            i+=1
            
        # renew border
        self.w_order.box('|','-')
        # add name
        self.w_order.addstr(0,1,"[Menu Functions]", self.COS[3])
        # noutrefresh display
        self.w_order.noutrefresh()


    # get current numerical order of current order
    def get_order(self):
        return self.numerical_order

    # using update_order after order_top, down
    # up
    def order_down(self):
        self.numerical_order+=1
        if(self.numerical_order == self.max_num_choice):
            self.numerical_order = 0
    # down
    def order_top(self):
        self.numerical_order-=1
        if(self.numerical_order < 0):
            self.numerical_order = self.max_num_choice - 1

    #[.static window display]
    #[D. guide users window]
    def update_guide(self):
        # renew border
        self.w_guide.box('|','-')
        # content
        self.w_guide.addstr(1,1,"w-Up   |s-Down")
        self.w_guide.addstr(2,1,"q-Quit |ent-Select")
        # add name
        self.w_guide.addstr(0,1,"[How to use]", self.COS[1])
        # noutrefresh display
        self.w_guide.noutrefresh()

    #[E. background]
    def update_background(self):
        # renew border
        self.backwin.box('|','-')
        #add name
        self.backwin.addstr(0,1,"[Task Manager]",self.COS[4])
        #noutrefresh to apply new change
        self.backwin.noutrefresh()