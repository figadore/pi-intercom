import sys
import time
import stations
sys.path.append('/home/pi/repos/ring-daemon/tools/dringctrl')

from controller import DRingCtrl

station_defs = [
    {
        "display_name": "reese-desk",
        "device_type": "RPI4",
        "ip": "192.168.0.200",
        "username": "cypress200",
        "sip_domain": "sip.linphone.org",
    },
    {
        "display_name": "faith-desk",
        "device_type": "RPI4",
        "led_pin1": "27",
        "led_pin2": "4",
        "ip": "192.168.0.201",
        "username": "cypress201",
        "sip_domain": "sip.linphone.org",
    },
    {
        "display_name": "kitchen",
        "device_type": "RPIZero",
        "ip": "192.168.0.202",
        "username": "cypress202",
        "sip_domain": "sip.linphone.org",
    },
    {
        "display_name": "reese-pc",
        "device_type": "Windows",
        "ip": "192.168.0.21",
        "username": "figadore",
        "led_pin1": "10",
        "led_pin2": "22",
        "sip_domain": "sip.linphone.org",
    },
    {
        "display_name": "reese-phone",
        "device_type": "Android",
        "username": "reese-pixel",
        "sip_domain": "sip.linphone.org",
    },
]

class Intercom(DRingCtrl):
    def __init__(self, button_handler):
        print("Intercom init")
        name = 'pi-intercom'
        autoanswer = True
        super().__init__(name, autoanswer)
        sleeptime = 1
        self.stations = self.init_stations(station_defs)
        self.active_call_count = 0
        self.button_handler = button_handler

    def init_stations(self, station_defs):
        stations_list = []
        for station_def in station_defs:
            station = stations.Station(
                display_name=station_def["display_name"],
                device_type=station_def["device_type"],
                username=station_def["username"],
                ip=station_def.get("ip"),
                sip_domain=station_def["sip_domain"],
                led_pin1=station_def.get("led_pin1", None),
                led_pin2=station_def.get("led_pin2", None)
            )
            stations_list.append(station)
        return stations_list

    def call_all(self):
        #callId2 = self.Call("cypress201@sip.linphone.org")
        callId2 = self.Call("cypress201@192.168.0.201")
        print("callId2:" + callId2)
        self.printClientCallList()

        #time.sleep(sleeptime)
        #callId1 = self.Call("reese-pixel@sip.linphone.org")
        ##callId2 = self.Call("figadore@sip.linphone.org")
        #print("callId1:" + callId1)
        #time.sleep(sleeptime)
        #confId = self.createConference(callId1, callId2)
        #if confId == "":
        #    print("\nWarning: Conference empty\n")

        #for call in self.getAllCalls():
        #    print(f"Printing details for call {call}")
        #    details = self.getCallDetails(call)
        #    for k,detail in details.items():
        #        print(k + ": " + detail)
        ##print("Created conference id:" + confId)

    def hangup_all(self):
        for call in self.getAllCalls():
            print(f"Hanging up call {call}")
            self.HangUp(call)

    def onCallStateChanged_cb(self, call_id, state, code):
        station = self.get_station(call_id)
        print(f"intercom call {call_id} state changed to {state} with code {code}")
        if station is None:
            print(f"Uh oh, station for {call_id} not found")
        station.set_call_status(state)
        if state == "CONNECTING":
            self.active_call_count = self.active_call_count + 1
        if state == "OVER":
            self.active_call_count = self.active_call_count - 1
            if self.active_call_count == 0:
                # hangup button should now be a call button
                self.button_handler.reset_buttons()

    def onConferenceCreated_cb(self):
        print("onConferenceCreated_cb")
        # TODO get conf id somehow
        pass

    def get_station(self, call_id):
        details = self.getCallDetails(call_id)
        peer_number = details["PEER_NUMBER"]
        for station in self.stations:
            if station.get_call_id() == call_id:
                return station
            # Example peer_number: <sip:cypress201@192.168.0.201>
            sip = f"<sip:{station.username}@{station.sip_domain}>"
            ip2ip = f"<sip:{station.username}@{station.ip}>"
            if peer_number == ip2ip or peer_number == sip:
                print("found station")
                print(station)
                station.set_call_id(call_id)
                return station
            else:
                print(f"{peer_number} == {ip2ip} or {peer_number} == {sip}")
        return None
