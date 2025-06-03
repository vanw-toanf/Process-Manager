import sys
import curses
import time
import threading
from log.log import Logger
log = Logger("./app.log") 

def push_to_screen():
    print("")