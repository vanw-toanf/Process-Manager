import curses
from _3_display_component.container_class.container import Container
from _4_system_data import CRP_control
'''****************************************************************************
* Variable
****************************************************************************'''
# inherit the 'Container' class
class OneProcWin(Container):
    # Initialize display windows
    def __init__(self):
        #Variable and constant
        ##[process properties window]
        self.w_proc_begin_col = None; self.w_proc_begin_row = None
        self.w_proc_col = None; self.w_proc_row = None

        #guide window
        self.w_guide_begin_col = None; self.w_guide_begin_row = None
        self.w_guide_col = None; self.w_guide_row = None

        # window variable
        self.w_proc = None; self.w_guide = None

        # init backwindow
        Container.__init__(self)

        # calculate sub win size and coordinate content, prepare content
        self.cal_size_sub_window()

        # init sub window
        self.w_proc = curses.newwin(self.w_proc_row,self.w_proc_col,
                                     self.w_proc_begin_row,self.w_proc_begin_col)
        self.w_guide = curses.newwin(self.w_guide_row,self.w_guide_col,
                                     self.w_guide_begin_row,self.w_guide_begin_col)
        
        # now add keypad(True)
        self.w_proc.keypad(True); self.w_guide.keypad(True)

        # add no delay for using getch()
        self.w_proc.nodelay(True); self.w_guide.nodelay(True)

    def __del__(self):
        Container.__del__(self)



    '''_______________[interract with window]___________'''
    # [A. calculate and re-set size window]
    def cal_size_sub_window(self):
        # row: 100% = 10% top border + 65% menu + 5% free space + 15% guide + 5% bottom border (guard)
        #proc window
        self.w_proc_begin_col = self.back_win_col * 10 // 100
        self.w_proc_begin_row = self.back_win_row * 10 // 100
        self.w_proc_col = self.back_win_col * 80 // 100 #> 60block
        self.w_proc_row = self.back_win_row * 65 // 100

        #guide window
        self.w_guide_begin_col = self.back_win_col * 10 // 100
        self.w_guide_begin_row = self.back_win_row * 80 // 100
        self.w_guide_col = self.w_proc_col
        self.w_guide_row = self.back_win_row * 15 // 100

    # clear all window
    def clear_all_window(self):
        self.backwin.clear()
        self.w_proc.clear()
        self.w_guide.clear()

    #[B. PID properties window]
    def get_and_update_PID_properties(self, pid):
        #get properties. if error , log error
        ret = CRP_control.get_process_info(pid)

        #clear process properties window
        self.w_proc.clear()

        # renew border
        self.w_proc.box('|','-')

        #check error code
        if ret != 0:
            if ret == -1:# No such process
                self.w_proc.addstr(self.w_proc_row//2,1,"PID [{}] Not Found".format(pid),self.COS[0])
            elif ret == -2:# Access denied
                self.w_proc.addstr(self.w_proc_row//2,1,"PID [{}] Access denied".format(pid),self.COS[0])
            elif ret == -3:# Zombie process
                self.w_proc.addstr(self.w_proc_row//2,1,"PID [{}] is Zombie process".format(pid),self.COS[0])
            else:
                self.w_proc.addstr(self.w_proc_row//2,1,"PID [{}] Unexpected Error".format(pid),self.COS[0])
        #if no error -> print
        else:
            line_div_2 = self.w_proc_col//2
            line_2_div_3 = self.w_proc_col*2//3
            line_div_3 = self.w_proc_col//3

            self.w_proc.addstr(0,1,"[Basic Info]",curses.A_BOLD)
            self.w_proc.addstr(1,1,"Name: {}".format(CRP_control.PID_properties["Name"][:self.w_proc_col-10]),self.COS[3])
            self.w_proc.addstr(2,1,"PID: "+CRP_control.PID_properties["PID"],self.COS[3])
            self.w_proc.addstr(2,line_div_2,"PPID: "+CRP_control.PID_properties["PPID"],self.COS[3])
            self.w_proc.addstr(3,1,"Status: "+CRP_control.PID_properties["Status"],self.COS[3])
            self.w_proc.addstr(3,line_div_2,"Username: "+CRP_control.PID_properties["Username"],self.COS[3])
            self.w_proc.addstr(4,1,"Command: {}".format(CRP_control.PID_properties["Command"][:self.w_proc_col-13]),self.COS[3])
            self.w_proc.addstr(5,1,"Execute: {}".format(CRP_control.PID_properties["Executable"][:self.w_proc_col-13]),self.COS[3])
            self.w_proc.addstr(6,1,"CWD: {}".format(CRP_control.PID_properties["CWD"][:self.w_proc_col-13]),self.COS[3])
            self.w_proc.addstr(7,1,"-"*(self.w_proc_col-2),curses.A_BOLD)
            self.w_proc.addstr(7,1,"[Memory Info]",curses.A_BOLD)
            self.w_proc.addstr(8,1,"VMS: "+CRP_control.PID_properties["MEM_VMS"]+"MB",self.COS[3])
            self.w_proc.addstr(8,line_div_3,"RSS: "+CRP_control.PID_properties["MEM_RSS"]+"MB",self.COS[3])
            self.w_proc.addstr(8,line_2_div_3,"Percent: "+CRP_control.PID_properties["MEM_Percent"]+"%",self.COS[3])
            self.w_proc.addstr(9,1,"-"*(self.w_proc_col-2),curses.A_BOLD)
            self.w_proc.addstr(9,1,"[CPU Info]",curses.A_BOLD)
            self.w_proc.addstr(10,1,"CPU num: "+CRP_control.PID_properties["CPU Num"],self.COS[3])
            self.w_proc.addstr(10,line_div_3,"CPU usage: "+CRP_control.PID_properties["CPU Usage"]+"%",self.COS[3])
            self.w_proc.addstr(10,line_2_div_3,"Num threads: "+CRP_control.PID_properties["Num Threads"],self.COS[3])
            self.w_proc.addstr(11,1,"Run time: "+CRP_control.PID_properties["Runtime"],self.COS[3])
            self.w_proc.addstr(11,line_div_3,"User time: "+CRP_control.PID_properties["User Time"]+"s",self.COS[3])
            self.w_proc.addstr(11,line_2_div_3,"Sys time: "+CRP_control.PID_properties["Sys Time"]+"s",self.COS[3])
            self.w_proc.addstr(12,1,"-"*(self.w_proc_col-2),curses.A_BOLD)
            self.w_proc.addstr(12,1,"[IO Info]",curses.A_BOLD)
            self.w_proc.addstr(13,1,"Read count: "+CRP_control.PID_properties["I/O Read Count"],self.COS[3])
            self.w_proc.addstr(13,line_div_3,"Write count: "+CRP_control.PID_properties["I/O Write Count"],self.COS[3])
            self.w_proc.addstr(13,line_2_div_3,"Open Files: "+CRP_control.PID_properties["Open Files Count"],self.COS[3])

        # noutrefresh display
        self.w_proc.noutrefresh()
        
    #[C. send signal]
    # while pid properties is displaying we can use
    # suspend (0), resume (1), terminate (2), kill (3)
    # to control process
    def send_sig(self, your_order):
        try:
            if your_order == 0:  # Suspend
                CRP_control.PID_object.suspend()
            elif your_order == 1:  # Resume
                CRP_control.PID_object.resume()
            elif your_order == 2:  # Terminate
                CRP_control.PID_object.terminate()
            elif your_order == 3:  # Kill
                CRP_control.PID_object.kill()
            else:
                return
        except Exception as e:#ignore nosuch PID, AccessDenied,...
            return

    #[static window display]
    #[D. guide users window]
    def update_guide(self):
        # add content
        self.w_guide.addstr(1,1,"s-Suspend |r-Resume |t-terminate |k-Kill |q-Quit |l-list")

        # renew border
        self.w_guide.box('|','-')
        # add name
        self.w_guide.addstr(0,1,"[How to use] push 'u' before s/r/t/k", self.COS[1])
        # noutrefresh display
        self.w_guide.noutrefresh()

    #[D. background]
    def update_background(self):
        # renew border
        self.backwin.box('|','-')
        #add name
        self.backwin.addstr(0,1,"[PID Properties]",self.COS[4])
        #noutrefresh to apply new change
        self.backwin.noutrefresh()
