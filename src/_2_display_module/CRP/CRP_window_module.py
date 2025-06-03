"""
CRP_proc_window_module.py

These modules manages and handle a window for displaying CPU, RAM, and process
information using the `curses` library.

It includes functions for initializing the window, handling user input, updating
and refreshing the display, and managing data related to processes and system resources.

Multi-threading is used to ensure smooth performance and separation of tasks like
updating data, checking user input, and refreshing the display.

The code uses global variables, mutex locks, and conditions to coordinate actions across
multiple threads and manage shared data effectively.

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
import threading #mutex, condition

# defined libraries
from _3_display_component.CRP.CRP_win_component import CRPwin #inherit class for CRP window
from _4_system_data import CRP_control

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
w_CRP = None # variable save object CRP window

#thread signal
end_sig = None #default threadings loop

# mutex key
mutex_R1 = threading.Lock()# T1, T2.2, T4.2
mutex_R2 = threading.Lock()# T2.1, T2.2
mutex_R3 = threading.Lock()# T2.1, T2.2, T3.1, T3.2
# thread check user input T3.2 T3.1 (dùng luôn main process)
#mutex_R4  : T4.1 T4.2 bỏ qua

# time cycle
# all cycle must <= 1s else it can take > 1s close page
cycle_renew_list_proc = 1 # 1s sleep then renew list processes
cycle_update_list_proc = 0.3 # 300ms sleep then update data list process will display
cycle_renew_and_update_list_total_resource = 1 # 1s sleep then renew and update total resource
cycle_user_input = 0.2 # 200ms sleep then check buffer input
cycle_screen_refresh = 0.3 # 300ms sleep then push data buffer to screen

#check size first time and update static content
size_not_checked_fisrt_time =None #  default CommonErrorCode.NOT_CHECKED

# sort order
sort_order = None #default sort by pid

# stop status for functions: renew screen, renew total resource
mutex_catch_screen = threading.Lock()
condition_catch_screen = threading.Condition(mutex_catch_screen)
catch_screen_sig = None #default no catch
total_threads_stopped = None #default 0

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
    global sort_order
    global catch_screen_sig
    global total_threads_stopped

    end_sig = CommonErrorCode.NOT_END_SIG
    size_not_checked_fisrt_time = CommonErrorCode.NOT_CHECKED
    error_size = CommonErrorCode.OK
    sort_order = 0
    catch_screen_sig = CommonErrorCode.NOT_STOP_SIG
    total_threads_stopped = 0

# [handler for CPU/RAM/PROC window]
# initialize and check size, set color, set box
def init_CRP_window():
    global w_CRP
    #renew global variables
    renew_global_variable()
    #init guide window object
    w_CRP = CRPwin()

# wait to get key
# main thread combine with T3.1 and T3.2
# resource mutex key R3
def getkey_CRPwindow():
    global w_CRP
    global end_sig
    global sort_order
    global mutex_R3

    global mutex_catch_screen
    global catch_screen_sig
    global condition_catch_screen
    
    temp_input = "nothing"
    while ( (temp_input != '\n') and
        (temp_input != 'm') and
        (temp_input != 'q') and 
        (error_size == CommonErrorCode.OK)):

        with mutex_R3:
            # check buffer input
            temp_input = w_CRP.backwin.getch()
            # if nothing -> compare -1
            if temp_input == -1:
                continue
            # else check what user want
            else: temp_input = chr(temp_input)
            # clean stdin buffer before unlock
            while w_CRP.backwin.getch() != -1: continue
            
            # common signal
            if(temp_input == 'w'):
                w_CRP.move_order_up()#user want upper
            elif(temp_input == 's'):
                w_CRP.move_order_down()#user want lower
            
            #sort signal
            elif(temp_input == '0'):
                sort_order = 0
            elif(temp_input == '1'):
                sort_order = 1
            elif(temp_input == '2'):
                sort_order = 2
            elif(temp_input == '3'):
                sort_order = 3
            elif(temp_input == '4'):
                sort_order = 4
            elif(temp_input == '5'):
                sort_order = 5
            
            # stop screen update data
            elif(temp_input == 'c'):
                with mutex_catch_screen:
                    if catch_screen_sig == CommonErrorCode.NOT_STOP_SIG:
                        # notify stop update process data
                        catch_screen_sig = CommonErrorCode.STOP_SIG
                        # log
                        temp_log = "[stopped]"
                        # print red log stopped
                        w_CRP.backwin.addstr(0,w_CRP.back_win_col-1-len(temp_log),temp_log,w_CRP.COS[0])
                    elif catch_screen_sig == CommonErrorCode.STOP_SIG:
                        #notify continue update data
                        catch_screen_sig = CommonErrorCode.NOT_STOP_SIG
                        condition_catch_screen.notify_all()
                        #log
                        temp_log = "---------"
                        # recover origin status
                        w_CRP.backwin.addstr(0,w_CRP.back_win_col-1-len(temp_log),temp_log)

        # sleep for user react and other thread do
        time.sleep(cycle_user_input)
    #end
    end_sig = CommonErrorCode.END_SIG

    # check threads are stopping then notify to end
    with mutex_catch_screen:
        #unlock mode stop to catch data
        catch_screen_sig = CommonErrorCode.NOT_STOP_SIG
        #check if any threads still be stopping
        if total_threads_stopped > 0:
            condition_catch_screen.notify_all()

    # check if special signal input
    # open menu
    if temp_input == "m":
        return -1
    # if input == \n -> more PID properties
    elif temp_input == '\n':
        return CRP_control.list_proc[w_CRP.offset_list_proc + w_CRP.current_order_proc]["pid"]#PID
    #if input == q -> quit
    elif temp_input == 'q':
        return -2 # quit signal
    
    #check if error
    # error size
    elif error_size == CommonErrorCode.ERROR_INVALID_MIN_SIZE:
        return -3 # < size min
    elif error_size == CommonErrorCode.ERROR_SIZE_CHANGED:
        return -4 #size changed
    else:
        return -5

# end
def exit_CRP_window():
    global w_CRP
    del w_CRP #free completely window curses and switch back to the original terminal 
    if debug == CommonErrorCode.DEBUG:
        print("[OK - {}] closed the CRP window".format(exit_CRP_window.__name__),
              file=sys.stderr)
    # no return

# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window (support)
# check resize or size not invalid
def check_size_valid():
    global w_CRP
    global error_size
    global size_not_checked_fisrt_time

    # save old background size
    old_back_col = w_CRP.back_win_col
    old_back_row = w_CRP.back_win_row

    # [Check size valid]
    # get background size to check change size
    w_CRP.get_backwin_size()
    # now check if size invalid
    if((w_CRP.back_win_col < w_CRP.w_back_mincol) or
    (w_CRP.back_win_row < w_CRP.w_back_minrow)):
        error_size = CommonErrorCode.ERROR_INVALID_MIN_SIZE # error size < min

    # [Check if size change]
    if((old_back_col != w_CRP.back_win_col) or
    (old_back_row != w_CRP.back_win_row)):
        error_size = CommonErrorCode.ERROR_SIZE_CHANGED # size changed

    # if this is first time checksize, update static content
    if size_not_checked_fisrt_time == CommonErrorCode.NOT_CHECKED:
        size_not_checked_fisrt_time = CommonErrorCode.CHECKED#checked

        #and if size ok print static content only one time
        if error_size == CommonErrorCode.OK :
            #clear all window
            w_CRP.clear_all_window()
            w_CRP.update_background()#do first
            #test color
            w_CRP.Hello_World()
            #static content
            w_CRP.update_guide()

    # return error_size code
    return error_size

# B. push content to background (thread) (T1)
def push_to_screen():
    global w_CRP
    global end_sig
    global mutex_R1
    
    # push content to screen
    while(end_sig == CommonErrorCode.NOT_END_SIG):
        # push content from buffer to screen
        with mutex_R1:
            #check size screen first before push data  screen
            if check_size_valid() != CommonErrorCode.OK:
                return #end looping :) end thread
            #else push to screen
            curses.doupdate()
        #sleep
        time.sleep(cycle_screen_refresh)

# C. Renew processes list data (thread) (T2.1) (stop condition)
def renew_list_precesses_data():
    global w_CRP
    global end_sig

    global mutex_catch_screen
    global condition_catch_screen
    global total_threads_stopped

    global mutex_R2
    global mutex_R3

    while end_sig == CommonErrorCode.NOT_END_SIG :
        # stop renew processes list by condition variable
        mutex_catch_screen.acquire()
        total_threads_stopped +=1
        while catch_screen_sig == CommonErrorCode.STOP_SIG:
            condition_catch_screen.wait()
        total_threads_stopped -=1
        mutex_catch_screen.release()
        # get mutex then update total resource
        with mutex_R2:
            with mutex_R3:
                #check size screen first before push data  screen
                if check_size_valid() != CommonErrorCode.OK:
                    return #end looping :) end thread
                #else renew list proc
                w_CRP.renew_list_processes(sort_order)
        #then unlock R2 + R3
        #sleep
        time.sleep(cycle_renew_list_proc)

# D. Release data processes will display to buffer (thread) (T2.2)
def update_list_proc_display():
    global w_CRP
    global end_sig
    global mutex_R1
    global mutex_R2
    global mutex_R3

    while(end_sig == CommonErrorCode.NOT_END_SIG):
        with mutex_R1:
            with mutex_R2:
                with mutex_R3:
                    #check size screen first before push data  screen
                    if check_size_valid() != CommonErrorCode.OK:
                        return #end looping :) end thread
                    #else renew list proc
                    w_CRP.update_proc_content()
        #then unlock R1 + R2 + R3
        #sleep
        time.sleep(cycle_update_list_proc)

# E. Release data total resource will display to buffer (thread) (T4.1+T4.2) (stop condition)
def update_total_resource():
    global w_CRP
    global end_sig

    global mutex_catch_screen
    global condition_catch_screen
    global total_threads_stopped

    global mutex_R1

    while end_sig == CommonErrorCode.NOT_END_SIG:
        # stop total resource by condition variable
        mutex_catch_screen.acquire()
        total_threads_stopped +=1
        while catch_screen_sig == CommonErrorCode.STOP_SIG:
            condition_catch_screen.wait()
        total_threads_stopped -=1
        mutex_catch_screen.release()
        # get mutex then update total resource
        with mutex_R1:
            #check size screen first before push data  screen
            if check_size_valid() != CommonErrorCode.OK:
                return #end looping :) end thread
            #else renew list proc
            w_CRP.update_total_content()
        #then unlock R1
        #sleep
        time.sleep(cycle_renew_and_update_list_total_resource)