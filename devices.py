from pyHS100 import Discover, SmartPlug
import requests
import time

class GenericDevice:
    def __init__(self, label=None, ip=None, predelay=0, show_status=True, internal_id=""):
        self.internal_id = ""
        self.label = label
        self.ip = ip
        self.predelay = predelay
        self.show_status = show_status

    def turn_off(self):
        return False

    def turn_on(self):
        return False

    def status(self):
        return ""

    def __str__(self):
        return f"Device with IP: {self.ip}, label: {self.label}, predelay: {self.predelay}, show_status: {self.show_status}"

class ESPHomeButton(GenericDevice):
    def __init__(self, label=None, ip=None, predelay=0, show_status=True, internal_id=""):
        super().__init__(label, ip, predelay, show_status, internal_id)

    def turn_off(self):
        try:
            resp = requests.get(f"http://{self.ip}/button/{self.internal_id}/press")
            return (resp.status_code == 200)
        except:
            return False

    def turn_on(self):
        try:
            resp = requests.get(f"http://{self.ip}/button/{self.internal_id}/press")
            return (resp.status_code == 200)
        except:
            return False

    def status(self):
        try:
            resp = requests.get(f"http://{self.ip}/", timeout=3)
            status_str = "(%s)" % "UNKNOWN (ONLINE)" if (resp.status_code == 200) else "UNAVAILABLE (ERROR)"
            return status_str
        except:
            return "UNAVAILABLE (OFFLINE)"

class KasaSmartSwitch(GenericDevice):
    def __init__(self, label=None, ip=None, predelay=0, show_status=True):
        super().__init__(label, ip, predelay, show_status)
        self.plug = SmartPlug(self.ip) if self.ip != "all" else None
        if self.plug is not None:
            self.label = self.plug.alias
        self.plug = None

    def turn_off(self):
        time.sleep(self.predelay)
        if self.plug is None:
            self.plug = SmartPlug(self.ip) if self.ip != "all" else None
        if self.plug is not None:
            self.plug.turn_off()
        self.plug = None
        return True

    def turn_on(self):
        time.sleep(self.predelay)
        if self.plug is None:
            self.plug = SmartPlug(self.ip) if self.ip != "all" else None
        if self.plug is not None:
            self.plug.turn_on()
        self.plug = None
        return True

    def status(self):
        if self.plug is None:
            self.plug = SmartPlug(self.ip) if self.ip != "all" else None
        if self.plug is not None:
            status_str = "(%s)" % self.plug.state if self.plug else "UNAVAILABLE (OFFLINE)"
        self.plug = None
        return status_str
    
    def __del__(self):
        self.plug = None