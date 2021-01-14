import sys
import os
import argparse
import socket

sys.path.append('/home/pi/repos/ring-daemon/tools/dringctrl')
from controller import DRingCtrl
from time import sleep

name = 'faketest'
hostname = socket.gethostname()
password = os.environ['JAMI_PW']
autoanswer = True
ctrl = DRingCtrl(name, autoanswer)

def create():
    """Create a new sip account"""
    accDetails = {
            "Account.type":"SIP",
            "Account.alias":hostname,
            "Account.hostname":"sip.linphone.org",
            "Account.username":hostname,
            "Account.localPort":"5060",
            "Account.displayName":hostname,
            "Account.username":hostname,
            "Account.password":password,
            "Account.videoEnabled":"false",
            "Account.displayName":hostname
    }

    accountId = ctrl.addAccount(accDetails)
    print("New Account ID " + accountId)


def update():
    #accountId = "262319acd93f5c7b"
    accDetails = {"Account.type":"SIP", "Account.alias":hostname,
                  "Account.hostname":"sip.linphone.org", "Account.username":hostname,
                  "Account.displayName":hostname,
                  "Account.username":hostname,
                  "Account.videoEnabled":"false",
                  "Account.password":password,
                  "Account.displayName":hostname}
    credentials = [{"Account.password": password, "Account.username": hostname, "Account.realm": "*"}]
    ctrl.setAccountDetails(accountId, accDetails)

create()
