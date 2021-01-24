Raspberry Pi Intercom

* `export JAMI_PW=<pw>`
* `/usr/local/lib/arm-linux-gnueabihf/jamid -cd --auto-answer #in another terminal`
* `python3 setup.py`
* `~/repos/ring-daemon/tools/dringctrl/dringctrl.py --register $(~/repos/ring-daemon/tools/dringctrl/dringctrl.py --get-enabled-accounts)`
