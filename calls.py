import sys
import time
sys.path.append('/home/pi/repos/ring-daemon/tools/dringctrl')
import psutil #for daemon resets

from controller import DRingCtrl

name = 'pi-intercom'
autoanswer = True
ctrl = DRingCtrl(name, autoanswer)
sleeptime = 1

def CallAll():
    callId2 = ctrl.Call("cypress201@sip.linphone.org")
    print("callId2:" + callId2)
    time.sleep(sleeptime)
    callId1 = ctrl.Call("reese-pixel@sip.linphone.org")
    #callId2 = ctrl.Call("figadore@sip.linphone.org")
    print("callId1:" + callId1)
    time.sleep(sleeptime)
    confId = ctrl.createConference(callId1, callId2)
    if confId == "":
        print("\nWarning: Conference empty\n")

    for call in ctrl.getAllCalls():
        print(f"Printing details for call {call}")
        details = ctrl.getCallDetails(call)
        for k,detail in details.items():
            print(k + ": " + detail)
    print("Created conference id:" + confId)

def Hangup():
    for call in ctrl.getAllCalls():
        print(f"Hanging up call {call}")
        ctrl.HangUp(call)

def Reset():
    for proc in psutil.process_iter():
        if proc.name() == "jamid":
            proc.terminate()
    # Run jami daemon, piping colored outputs to specified log file
    command = 'script -qfc "/usr/local/lib/arm-linux-gnueabihf/jamid -d --auto-answer -c" /home/pi/log.txt > /dev/null'
    # Watch output with 'tail -f ~/log.txt'
