import asyncio
from kasa import SmartPlug
import time

class GenericDevice:
    def __init__(self, label=None, ip=None, predelay=0, show_status=False):
        self.label = label
        self.ip = ip
        self.predelay = predelay
        self.show_status = show_status

    async def update(self):
        return False

    async def turn_off(self):
        return False

    async def turn_on(self):
        return False

    async def status(self):
        return ""

    def __str__(self):
        return f"Device with IP: {self.ip}, label: {self.label}, predelay: {self.predelay}, show_status: {self.show_status}"

class KasaSmartSwitch(GenericDevice):
    def __init__(self, label=None, ip=None, predelay=0, show_status=False):
        super().__init__(label, ip, predelay, show_status)

    async def update(self):
        if self.label is None:
            plug = SmartPlug(self.ip)
            await plug.update()
            self.label = plug.alias
            plug = None
        return True

    async def turn_off(self):
        time.sleep(self.predelay)
        plug = SmartPlug(self.ip)
        await plug.turn_off()
        plug = None
        return True

    async def turn_on(self):
        time.sleep(self.predelay)
        plug = SmartPlug(self.ip)
        await plug.turn_on()
        plug = None
        return True

    async def status(self):
        plug = SmartPlug(self.ip) if self.ip != "all" else None
        await plug.update()
        status_str = "(%s)" % plug.state if plug else "UNAVAILABLE (OFFLINE)"
        plug = None
        return status_str