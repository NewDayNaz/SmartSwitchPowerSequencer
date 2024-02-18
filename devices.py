from pyHS100 import Discover, SmartPlug
import time

class GenericDevice:
    def __init__(self, label=None, ip=None, predelay=0, show_status=True):
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

class KasaSmartSwitch(GenericDevice):
    def __init__(self, label=None, ip=None, predelay=0, show_status=True):
        super().__init__(label, ip, predelay, show_status)
        self.plug = SmartPlug(self.ip) if self.ip != "all" else None
        if self.plug is not None:
            self.label = self.plug.alias

    def turn_off(self):
        time.sleep(self.predelay)
        if self.plug is not None:
            self.plug.turn_off()
        return True

    def turn_on(self):
        time.sleep(self.predelay)
        if self.plug is not None:
            self.plug.turn_on()
        return True

    def status(self):
        if self.plug is not None:
            status_str = "(%s)" % plug.state if plug else "UNAVAILABLE (OFFLINE)"
        return status_str
    
    def __del__(self):
        self.plug = None