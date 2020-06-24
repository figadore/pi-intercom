import os
import psutil
import subprocess

def is_daemon_running():
    for proc in psutil.process_iter():
        if proc.name() == "jamid":
            return True
    return False

def start_daemon(debug=False):
    # Run jami daemon, piping colored outputs to specified log file
    debug_flag = ""
    if debug:
        debug_flag = "-d"
    command = f'script -qfc "/usr/local/lib/arm-linux-gnueabihf/jamid {debug_flag} --auto-answer -c" /home/pi/log.txt > /dev/null'
    print("Watch output with 'tail -f ~/log.txt'")
    subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #os.spawnl(os.P_NOWAIT, 'script', '-qfc', f"/usr/local/lib/arm-linux-gnueabihf/jamid {debug_flag} --auto-answer -c",  '/home/pi/log.txt', '>', '/dev/null')

def reset():
    for proc in psutil.process_iter():
        if proc.name() == "jamid":
            proc.terminate()
    start_daemon()
