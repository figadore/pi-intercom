import sys
import time
sys.path.append('/home/pi/repos/ring-daemon/tools/dringctrl')

from controller import DRingCtrl


class Intercom:
    def __init__(self):
        name = 'pi-intercom'
        autoanswer = True
        self.ctrl = DRingCtrl(name, autoanswer)
        sleeptime = 1

    def call_all(self):
        #callId2 = ctrl.Call("cypress201@sip.linphone.org")
        callId2 = self.ctrl.Call("cypress201@192.168.0.201")
        print("callId2:" + callId2)
        #time.sleep(sleeptime)
        #callId1 = self.ctrl.Call("reese-pixel@sip.linphone.org")
        ##callId2 = self.ctrl.Call("figadore@sip.linphone.org")
        #print("callId1:" + callId1)
        #time.sleep(sleeptime)
        #confId = self.ctrl.createConference(callId1, callId2)
        #if confId == "":
        #    print("\nWarning: Conference empty\n")

        #for call in self.ctrl.getAllCalls():
        #    print(f"Printing details for call {call}")
        #    details = self.ctrl.getCallDetails(call)
        #    for k,detail in details.items():
        #        print(k + ": " + detail)
        ##print("Created conference id:" + confId)

    def hangup(self):
        for call in self.ctrl.getAllCalls():
            print(f"Hanging up call {call}")
            self.ctrl.HangUp(call)

