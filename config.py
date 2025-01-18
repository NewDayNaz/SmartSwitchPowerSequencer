from devices import GenericDevice, KasaSmartSwitch

title = "Power Dashboard"
sections = [
    {
        "id": "display",
        "name": "Display Dashboard",
        "prefix_devices": [
            GenericDevice(label="Display system", ip="all", show_status=True),
        ],
        "order_turn_on": "desc",
        "order_turn_off": "asc",
        "devices": [
            ESPHomeButton(ip="10.10.10.199", label="Projector", internal_id="projector_power_button")
        ]
    },
    {
        "id": "sound",
        "name": "Sound System Dashboard",
        "prefix_devices": [
            GenericDevice(label="Sound system", ip="all", show_status=True),
        ],
        "order_turn_on": "desc",
        "order_turn_off": "asc",
        "devices": [
            KasaSmartSwitch(ip="10.10.10.254"),
            KasaSmartSwitch(ip="10.10.10.251", predelay=15),
            KasaSmartSwitch(ip="10.10.10.252", predelay=5),
            KasaSmartSwitch(ip="10.10.10.253", predelay=5),
        ],
    },
    {
        "id": "lighting",
        "name": "Lighting Dashboard",
        "prefix_devices": [
            GenericDevice(label="All lighting switches", ip="all", show_status=True),
        ],
        "order_turn_on": "desc",
        "order_turn_off": "desc",
        "devices": [
            KasaSmartSwitch(ip="10.10.10.247"),
            KasaSmartSwitch(ip="10.10.10.249", predelay=1),
            KasaSmartSwitch(ip="10.10.10.248", predelay=1),
            KasaSmartSwitch(ip="10.10.10.246", predelay=1),
            KasaSmartSwitch(ip="10.10.10.226", predelay=1),
        ],
    },
]
