"""
One_proc_window_module.py

These modules provide the implementation for handling the window and user interactions 
in a curses-based interface for the Process Manager project. It includes functions to 
initialize and manage the process information window, handle user inputs for process 
control (e.g., suspend, resume, terminate, kill), and manage thread synchronization 
for safe screen updates.

Copyright (C) 2024, Giang Trinh.

This file is part of the Process Manager project and is licensed
under the GNU General Public License v3 or later.
"""


'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys
import curses
import time
import threading #mutex

# defined libraries
from _3_display_component.CRP.One_proc_win_component import OneProcWin #inherit class for one process window

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
w_OneProc = None # variable save object PID properties window
pid_input = None # PID input choice by user

#Enable sigterm
enable_sigterm = None # defaut not checked

#thread signal
end_sig = None #default threadings loop

# keymutex
lock_screen = threading.Lock()
    #Synchronize content updates and push content to the screen
    #using mutex 2 threads:
    #- update_PID_properties:
    #=> keep safe before push data to buffer screen
    #=> update content with user choice
    #=> sure not print missing content
    #- push_to_screen:
    #=> keep safe before push data from buffer to screen
    #=> sure push data is not changed

# time cycle
# all cycle must <= 1s else it can take > 1s close page
cycle_screen_refresh = 0.3 # 300ms sleep then push data buffer to screen
cycle_properties_update = 1 # 1s/time update PID properties
cycle_user_input = 0.2  # 200ms sleep then check buffer input

#check size first time and update static content
size_not_checked_fisrt_time =None #  default CommonErrorCode.NOT_CHECKED

#error code
error_size = None # default = CommonErrorCode.OK , no error size

'''****************************************************************************
* Code
****************************************************************************'''
#renew global variable if recall this window
def renew_global_variable():
    global end_sig
    global size_not_checked_fisrt_time
    global error_size
    global enable_sigterm

    end_sig = CommonErrorCode.NOT_END_SIG
    size_not_checked_fisrt_time = CommonErrorCode.NOT_CHECKED
    error_size = CommonErrorCode.OK
    enable_sigterm = CommonErrorCode.NOT_CHECKED

# [handler for one process window]
# initialize and check size, set color, set box
def init_One_proc_window(pid):
    global w_OneProc
    global pid_input
    #set pid
    pid_input = pid

    #renew global variables
    renew_global_variable()
    #init guide window object
    w_OneProc = OneProcWin()

# wait to get key
def getkey_One_proc_window():
    global w_OneProc
    global end_sig
    global enable_sigterm
    global lock_screen

    # wait user then update or execute or quit 'q'
    temp_input = 'nothing'
    while ((temp_input != 'q') and
           (temp_input != 'l') and
           (error_size == CommonErrorCode.OK)):
        # sleep for user react
        time.sleep(cycle_user_input)
        # then check buffer input
        temp_input = w_OneProc.w_proc.getch()
        # if nothing -> compare -1
        if temp_input == -1:
            continue
        # else check what user want
        else: temp_input = chr(temp_input)
        # clean stdin buffer before unlock
        while w_OneProc.w_proc.getch() != -1: continue
        
        if temp_input == 'u':
            temp_log = "[send signal unlocked]"
            w_OneProc.backwin.addstr(0,w_OneProc.back_win_col-1-len(temp_log),temp_log,w_OneProc.COS[0])
            #enable sigterm
            enable_sigterm = CommonErrorCode.CHECKED

        if enable_sigterm == CommonErrorCode.CHECKED:
            # check user input is s(suspend),r(resume),t(terminate),k(kill)
            if temp_input == 's':
                with lock_screen:
                    w_OneProc.send_sig(0)#sig 0 is suspend
            elif temp_input == 'r':
                with lock_screen:
                    w_OneProc.send_sig(1)#sig 1 is resume
            elif temp_input == 't':
                with lock_screen:
                    w_OneProc.send_sig(2)#sig 2 is terminate
            elif temp_input == 'k':
                with lock_screen:
                    w_OneProc.send_sig(3)#sig 3 is kill

    #end
    end_sig = CommonErrorCode.END_SIG

    #if input == m
    if temp_input == 'l':
        return -1 # list processes signal
    #if input == q
    elif temp_input == 'q':
        return -2 # quit signal
    # error size
    elif error_size == CommonErrorCode.ERROR_INVALID_MIN_SIZE:
        return -3 # < size min
    elif error_size == CommonErrorCode.ERROR_SIZE_CHANGED:
        return -4 #size changed
    else:
        return -5


# end
def exit_One_proc_window():
    global w_OneProc
    del w_OneProc #free completely window curses and switch back to the original terminal 
    if debug == CommonErrorCode.DEBUG:
        print("[OK - {}] closed the CRP window".format(exit_One_proc_window.__name__),
              file=sys.stderr)
    # no return

# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window (support)
# check resize or size not invalid
def check_size_valid():
    global w_OneProc
    global error_size
    global size_not_checked_fisrt_time

    # save old background size
    old_back_col = w_OneProc.back_win_col
    old_back_row = w_OneProc.back_win_row

    # [Check size valid]
    # get background size to check change size
    w_OneProc.get_backwin_size()
    # now check if size invalid
    if((w_OneProc.back_win_col < w_OneProc.w_back_mincol) or
    (w_OneProc.back_win_row < w_OneProc.w_back_minrow)):
        error_size = CommonErrorCode.ERROR_INVALID_MIN_SIZE # error size < min

    # [Check if size change]
    if((old_back_col != w_OneProc.back_win_col) or
    (old_back_row != w_OneProc.back_win_row)):
        error_size = CommonErrorCode.ERROR_SIZE_CHANGED # size changed

    # if this is first time checksize, update static content
    if size_not_checked_fisrt_time == CommonErrorCode.NOT_CHECKED:
        size_not_checked_fisrt_time = CommonErrorCode.CHECKED#checked

        #and if size ok print static content only one time
        if error_size == CommonErrorCode.OK :
            #clear all window
            w_OneProc.clear_all_window()
            w_OneProc.update_background()#do first
            #test color
            w_OneProc.Hello_World()
            #static content
            w_OneProc.update_guide()

    # return error_size code
    return error_size


# B. update_PID_properties to screen buffer
def update_PID_properties():
    global w_OneProc
    global end_sig
    global lock_screen

    # update PID properties
    while(end_sig == CommonErrorCode.NOT_END_SIG):
        with lock_screen:
            #check size screen first before push data to buffer screen
            if check_size_valid() != CommonErrorCode.OK:
                return #end looping :) end thread
            
            #else update properties
            w_OneProc.get_and_update_PID_properties(pid_input)
            
        #sleep for other threads and avoid continuous push data to buffer
        time.sleep(cycle_properties_update)

# C. push content to background (thread) (T1)
def push_to_screen():
    global w_OneProc
    global end_sig
    global lock_screen
     # push content to screen
    while(end_sig == CommonErrorCode.NOT_END_SIG):
        # push content from buffer to screen
        with lock_screen:
            #check size screen first before push data  screen
            if check_size_valid() != CommonErrorCode.OK:
                return #end looping :) end thread
            #else push to screen
            curses.doupdate()
        #sleep
        time.sleep(cycle_screen_refresh)

