"""
container.py

This module defines the 'Container' class, which sets up and manages
a curses-based environment.

It provides basic methods for initializing the screen, retrieving
screen size, setting color schemes and configuring input/output modes
such as enabling keypad input, nodelay mode, cbreak mode, noecho mode,
and hiding the cursor.

Copyright (C) 2024  Giang Trinh.

This file is part of the Process Manager project and is licensed
under the GNU General Public License v3 or later.
"""


'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
'''****************************************************************************
* Code
****************************************************************************'''
class Container:
    # [Initialize display windows]
    def __init__(self):
        # [Attribute]
        # background window size
        self.back_win_col=None
        self.back_win_row=None
        # at least 80col*24row
        self.w_back_mincol= 80
        self.w_back_minrow= 24

        # pseudo color or style
        # only use when call Container.Check_color_and_set()
        self.COS = None
        # [
        # "red black or BOLD", # for alert
        # "magenta black or DIM", # for not important or guide
        # "blue black or UNDERLINE", # for suggest
        # "yellow black or REVERSE", # for highlight
        # "green black or STANDOUT", # for highlight
        # "cyan black or BLINK"] # for notification

        # [init Window]
        # init main window
        self.backwin = curses.initscr()
        # add cbreak (auto enter), keypad(true)(convert special key to curses key), noecho (hide input)
        # :) i don't know why initscr not auto do it
        # cbreak, noecho only set once
        curses.cbreak(), curses.noecho()
        # hide cursor
        curses.curs_set(0)
        # now add keypad(True), this function have to set for every new window
        self.backwin.keypad(True)

        # now add non blocking mode to use getch()
        # and getch() auto  return -1 if buffer user input empty
        self.backwin.nodelay(True)

        # [Check and Update]
        # update background window size to update child window size
        self.get_backwin_size()

        # check color and set
        self.Check_color_and_set()

    #de-init
    def __del__(self):
        curses.endwin()

    # ______________[checking resource]_____________
    # [A. Should check size main window before printing anything]
    def get_backwin_size(self):
        # idont know why need refresh before get background size (getmaxyx)
        # but but dont do this, getmaxyx always return old size value
        # so great is call refresh before getmaxyx - get_backwin_size
        # because refresh = noutrefresh + doupdate
        # so we use noutrefresh if dont need push anything to screen
        self.backwin.noutrefresh()# curses update background value 
        self.back_win_row, self.back_win_col = self.backwin.getmaxyx()
    
    # [B. check color and set color]
    # if you want color, call it
    # if color not avalable -> change it by another style then update into list COS[]
    # defaut basic color: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    # but real test on 'bash' on linux we see that:
    #  0: black, 1: red, 5: green, 4: yellow, 3: blue, 2: magneta, 6: cyan
    # color pair index start is 1
    # basic style: A_BLINK, A_BOLD, A_DIM, A_REVERSE, A_STANDOUT, A_UNDERLINE,...
    def Check_color_and_set(self):
        curses.start_color()#set up default curses color
        if not curses.has_colors():
            self.COS = [curses.A_BOLD,curses.A_DIM,curses.A_UNDERLINE,
                   curses.A_REVERSE, curses.A_STANDOUT, curses.A_BLINK]
        else:# have color
            curses.init_pair(1, 1, 0)#red
            curses.init_pair(2, 2, 0)#mag
            curses.init_pair(3, 3, 0)#blue
            curses.init_pair(4, 4, 0)#yellow
            curses.init_pair(5, 5, 0)#green
            curses.init_pair(6, 6, 0)#cyan
            self.COS = [curses.color_pair(1), curses.color_pair(5), curses.color_pair(4),
                   curses.color_pair(3), curses.color_pair(2), curses.color_pair(6)]
            
    # ______________[interract with window]_____________
    
    #[print hello to test color]
    #must Check_color_and_set() before use this function
    def Hello_World(self):
        self.backwin.addstr(0, self.back_win_col//2 -15 ,"Team5",self.COS[0])
        self.backwin.addstr(0, self.back_win_col//2 -10 ,"_Proc",self.COS[1])
        self.backwin.addstr(0, self.back_win_col//2 -5  ,"ess__",self.COS[2])
        self.backwin.addstr(0, self.back_win_col//2     ,"Manag",self.COS[3])
        self.backwin.addstr(0, self.back_win_col//2 +5  ,"er___",self.COS[4])
        self.backwin.addstr(0, self.back_win_col//2 +10 ,"Hello",self.COS[5])
        self.backwin.noutrefresh()
