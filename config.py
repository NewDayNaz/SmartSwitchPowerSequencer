device_list = ["10.10.10.247", "10.10.10.249", "10.10.10.248", "10.10.10.246", "10.10.10.226"]
# Soundboard, Stagebox, Speaker L, Speaker R, TV
sound_device_list = ["10.10.10.254", "10.10.10.251", "10.10.10.252", "10.10.10.253"]
# sound_device_list = []

sections = [
    {
        "id": "sound",
        "name": "Sound System Dashboard",
        "prefix_rows": [
            {
                "show_status": True,
                "label": "Sound system",
                "ip": "all"
            }
        ],
        "order_turn_on": "desc",
        "order_turn_off": "asc",
        "devices": [
            {
                "ip": "10.10.10.254",
                "predelay": 0
            },
            {
                "ip": "10.10.10.251",
                "predelay": 15
            },
            {
                "ip": "10.10.10.252",
                "predelay": 5
            },
            {
                "ip": "10.10.10.253",
                "predelay": 5
            }
        ]
    },
    {
        "id": "lighting",
        "name": "Lighting Dashboard",
        "prefix_rows": [
            {
                "show_status": True,
                "label": "All lighting switches",
                "ip": "all"
            }
        ],
        "order_turn_on": "desc",
        "order_turn_off": "desc",
        "devices": [
            {
                "ip": "10.10.10.247",
                "predelay": 0
            },
            {
                "ip": "10.10.10.249",
                "predelay": 1
            },
            {
                "ip": "10.10.10.248",
                "predelay": 1
            },
            {
                "ip": "10.10.10.246",
                "predelay": 1
            },
            {
                "ip": "10.10.10.226",
                "predelay": 1
            },
        ]
    },
]