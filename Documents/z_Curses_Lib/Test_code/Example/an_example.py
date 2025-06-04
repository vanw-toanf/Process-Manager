'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
import note
'''****************************************************************************
* Variable
****************************************************************************'''
win1_shape = (5,20,2,5)
win2_shape = (5,20,7,5)

win1_choice = ("- Change color","- Change style","- ON/off border")
max_num_choice = 3

'''****************************************************************************
* Code
****************************************************************************'''
def mainwindow(stdscr):
    # test main window
    stdscr.box('|','-')
    stdscr.addstr(3, 2, "Hello ", curses.A_REVERSE)
    stdscr.addstr("Dang in bat dau o hang 3, cot 2", curses.A_ITALIC)
    stdscr.addstr(4, 2, "Error ", curses.A_REVERSE)
    stdscr.addstr(4,8,"Khi thay doi kich thuoc cua so thi chuong trinh bi tat !!!", curses.A_ITALIC)
    stdscr.addstr(5,8,"hoac co hanh vi sai.", curses.A_ITALIC)
    stdscr.addstr(6,8,"Vi no coi tin hieu resize cung la input", curses.A_ITALIC)
    # clear for another purpose
    stdscr.getkey(); stdscr.clear(); stdscr.box('!','~')
    stdscr.refresh()

    # add newwindow into main win
    #newwin(heigh, width, begin row, begin col)
    win1 = curses.newwin(win1_shape[0],win1_shape[1],win1_shape[2],win1_shape[3])
    win1.box('|','-')
    win1.addstr(0,5,"Win1")
    win1.addstr(1,1,"Hello")
    win1.addstr(2,1,"- Press any key!!!")
    win1.refresh()

    #get a key and print it on main win
    win1.addstr(3,1,win1.getkey())
    win1.refresh()

    #create a list order to change style, color, box
    #win1 is order list, win2 is changed list
    #check system color
    curses.start_color()#set up default curses color
    if not curses.has_colors():
        stdscr.addstr(0, 0, "Terminal does not support colors")
        stdscr.refresh()
        stdscr.getkey()
        return
    else:
        # Định nghĩa các cặp màu
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    #setup win1
    win1.clear(); win1.box('|','-'); win1.addstr(0,5,"Win1")
    win1.addstr(1,1,win1_choice[0],curses.A_REVERSE)
    win1.addstr(2,1,win1_choice[1])
    win1.addstr(3,1,win1_choice[2])
    win1.refresh()
    num_choice = 0
    #setup win2
    win2 = curses.newwin(win2_shape[0],win2_shape[1],win2_shape[2],win2_shape[3])
    win2.addstr(0,5,"Win2")
    win2.addstr(1,5,"TEST STRING")
    win2.refresh()
    #change style
    #change color
    #change box
    stdscr.addstr(0,0,"Press 'q' to quit")
    stdscr.refresh()
    temp_input = 'nothing'
    temp_status = 0
    while temp_input != 'q':
        temp_input = win1.getkey()
        # if user press up
        if (temp_input == curses.KEY_UP) or ((temp_input == 'w')):
            win1.addstr(num_choice+1,1,win1_choice[num_choice])
            num_choice+=1
            if(num_choice==3):
                num_choice = 0
            win1.addstr(num_choice+1,1,win1_choice[num_choice],curses.A_REVERSE)
            win1.refresh()
        elif ((temp_input  == curses.KEY_ENTER)or(temp_input  == '\n')):
            temp_status = 1 - temp_status
            if(num_choice == 0):#color
                if(temp_status):
                    win2.addstr(1,5,"TEST STRING",curses.color_pair(1))
                else:
                    win2.addstr(1,5,"TEST STRING")
            if(num_choice == 1):#style
                if(temp_status):
                    win2.addstr(1,5,"TEST STRING",curses.A_REVERSE)
                else:
                    win2.addstr(1,5,"TEST STRING")
            if(num_choice == 2):#border
                if(temp_status):
                    win2.box('|','-')
                else:
                    win2.box(' ',' ')
            win2.addstr(0,5,"Win2")
            win2.refresh()

    # Ket thuc chuong trinh
    # stdscr.refresh()
    stdscr.clear()
    stdscr.addstr(0,0,"Press any key to quit")
    stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    # Note
    note.note_default_setting()
    input("\n[Press any key to open 'wrapper']\n\n")


    # Start with wrapper.
    curses.wrapper(mainwindow)