Raspberry Pi Intercom

* `export JAMI_PW=<pw>`
* `/usr/local/lib/arm-linux-gnueabihf/jamid -cd --auto-answer #in another terminal`
* `python3 setup.py`
* `~/repos/ring-daemon/tools/dringctrl/dringctrl.py --register $(~/repos/ring-daemon/tools/dringctrl/dringctrl.py --get-enabled-accounts)`
* update ~/.config/jami/dring.yml to use speex codec that works on zero w (and fall back to pcm_mulaw): `activeCodecs: 86051/65542/`
* make a call: `~/repos/ring-daemon/tools/dringctrl/dringctrl.py --call sip:cypress203@192.168.0.203`
