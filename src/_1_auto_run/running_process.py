import threading 
import sys
import os
from log.log import Logger
log = Logger(os.path.abspath("app.log"))

def running_processes():
    log.log_info("Starting Process Manager Application")