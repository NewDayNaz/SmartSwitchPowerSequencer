import asyncio
from kasa import SmartPlug
import time

class GenericDevice:
    def __init__(self, label=None, ip=None, predelay=0, show_status=False):
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
    def __init__(self, label=None, ip=None, predelay=0, show_status=False):
        super().__init__(label, ip, predelay, show_status)
        if label is None:
            plug = SmartPlug(self.ip)
            asyncio.run(plug.update())
            self.label = plug.alias
            plug = None

    def turn_off(self):
        time.sleep(self.predelay)
        plug = SmartPlug(self.ip)
        asyncio.run(plug.turn_off())
        plug.turn_off()
        plug = None
        return True

    def turn_on(self):
        time.sleep(self.predelay)
        plug = SmartPlug(self.ip)
        asyncio.run(plug.turn_on())
        plug = None
        return True

    def status(self):
        plug = SmartPlug(self.ip) if self.ip != "all" else None
        asyncio.run(plug.update())
        status_str = "(%s)" % plug.state if plug else "UNAVAILABLE (OFFLINE)"
        plug = None
        return status_str