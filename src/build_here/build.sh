pyinstaller --onefile --icon="../computer.ico" --name="PRM" \
    --add-data="../about.txt:." \
    --add-data="../_1_auto_run:._1_auto_run" \
    --hidden-import=psutil \
    --hidden-import=npyscreen \
    ../main.py