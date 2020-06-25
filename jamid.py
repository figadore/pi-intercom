import os
import psutil
import subprocess
import time

def is_daemon_running():
    for proc in psutil.process_iter():
        if proc.name() == "jamid":
            return True
    return False

def start_daemon(debug=False):
    # Run jami daemon, piping colored outputs to specified log file
    print("Starting jamid")
    debug_flag = ""
    if debug:
        debug_flag = "-d"
    command = f'script -qfc "/usr/local/lib/arm-linux-gnueabihf/jamid {debug_flag} --auto-answer -c" /home/pi/log.txt > /dev/null'
    print("Watch output with 'tail -f ~/log.txt'")
    subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)


def reset():
    for proc in psutil.process_iter():
        if proc.name() == "jamid":
            print("Terminating jamid")
            proc.terminate()
            # Start daemon once old process terminates
            psutil.wait_procs([proc], timeout=3, callback=start_daemon)
