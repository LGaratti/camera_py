import threading
import os
import time

# Event objects for thread synchronization
save_event = threading.Event()
info_event = threading.Event()
visualization_event = threading.Event()
exit_event = threading.Event()

fps_list = []

def console_input():
    global fps_list
    command_avaiable = "\n s) save \n i) info \n v) visualize \n q) quit \n"
    while not exit_event.is_set():
        if save_event.is_set():
            print("Please Wait")
            continue
        if info_event.is_set():
            cmd = input("Insert q to quit info visualization: ")
            if cmd == 'q':
                # Calculate and print the average FPS
                if fps_list:
                    average_fps = sum(fps_list) / len(fps_list)
                    print(f"Average FPS: {average_fps:.2f}")
                    fps_list = []
                info_event.clear()
            continue
        if visualization_event.is_set():
            print("Visualization is active, press 'q' in visualization window to stop")
            time.sleep(1)
            continue
        cmd = input("Commands Avaiable: "+command_avaiable+" Insert a command: ")
        if cmd == 's':
            save_event.set()
        if cmd == 'i':
            info_event.set()
        if cmd == 'v':
            visualization_event.set()
        if cmd == 'q':
            exit_event.set()
        os.system('cls' if os.name == 'nt' else 'clear')