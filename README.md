Raspberry Pi Intercom

* `export JAMI_PW=<pw>`
* `python3 setup.py`
* `/usr/local/lib/arm-linux-gnueabihf/jamid -c -d #in another terminal`
* `~/repos/ring-daemon/tools/dringctrl/dringctrl.py --register $(~/repos/ring-daemon/tools/dringctrl/dringctrl.py --get-enabled-accounts)`
