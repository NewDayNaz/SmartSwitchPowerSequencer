import time

class Device:
    def __init__(self, label=None, ip=None, predelay=0, show_status=False):
        self.label = label
        self.ip = ip
        self.predelay = predelay
        self.show_status = show_status

    def turn_off(self):
        time.sleep(self.predelay)
        plug = SmartPlug(self.ip)
        plug.turn_off()
        plug = None
    def turn_on(self):
        time.sleep(self.predelay)
        plug = SmartPlug(self.ip)
        plug.turn_on()
        plug = None
    def status(self):
        plug = SmartPlug(self.ip) if self.ip != "all" else None
        status_str = "(%s)" % plug.state if plug else "UNAVAILABLE (OFFLINE)"
        plug = None
        return status_str

    def __str__(self):
        return f"Device with IP: {self.ip}, label: {self.label}, predelay: {self.predelay}, show_status: {self.show_status}"

sections = [
    {
        "id": "sound",
        "name": "Sound System Dashboard",
        "prefix_rows": [
            Device(label="Sound system", ip="all", show_status=True),
        ],
        "order_turn_on": "desc",
        "order_turn_off": "asc",
        "devices": [
            Device(ip="10.10.10.254"),
            Device(ip="10.10.10.251", predelay=15),
            Device(ip="10.10.10.252", predelay=5),
            Device(ip="10.10.10.253", predelay=5),
        ]
    },
    {
        "id": "lighting",
        "name": "Lighting Dashboard",
        "prefix_rows": [
            Device(label="All lighting switches", ip="all", show_status=True),
        ],
        "order_turn_on": "desc",
        "order_turn_off": "desc",
        "devices": [
            Device(ip="10.10.10.247"),
            Device(ip="10.10.10.249", predelay=1),
            Device(ip="10.10.10.248", predelay=1),
            Device(ip="10.10.10.246", predelay=1),
            Device(ip="10.10.10.226", predelay=1),
        ]
    },
]