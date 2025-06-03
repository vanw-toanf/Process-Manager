import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from _1_auto_run.main_form import MyApplication

if __name__ == '__main__':
    app = MyApplication()
    app.run()