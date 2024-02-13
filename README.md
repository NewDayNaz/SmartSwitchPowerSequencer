# SmartSwitchPowerSequencer

SmartSwitchPowerSequencer is a Python Flask web server that provides a user-friendly dashboard for controlling the power state of lights or sound devices in a pre-defined sequence using TP-Link Kasa Smart Switches.

## Warning!

Please be aware of the type of loads you are plugging into these switches; a lot of them are not rated for a full 15A load and quite a few are only rated for 10-12A.
I am using the classic Kasa HS100 smart plugs (sadly now EoL) which are actually rated for a 15A load.

## Features

- **Sequenced Power Control**: Define sequences for powering up or down devices in a specific order.
- **TP-Link Kasa Integration**: Utilizes the TP-Link Kasa Smart Home API for controlling smart switches.
- **User-friendly Dashboard**: A sleek web interface for easily managing power sequences.
- **Customizable**: Easily add, edit, or remove devices and sequences according to your needs.

## Requirements

- Python 3.x
- Flask
- pyHS100

## Installation

1. Clone this repository:

```bash
git clone https://github.com/NewDayNaz/SmartSwitchPowerSequencer.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. TODO: Configure your TP-Link Kasa Smart Switches by following the instructions provided in the `config.py` file.

4. Run the Flask web server:

```bash
set FLASK_APP=server.py
python -m flask run --host=0.0.0.0
```

5. Access the dashboard by navigating to `http://localhost:5000` in your web browser.

## Usage

1. Navigate to the web interface.
2. Access the dashboard to trigger the defined sequences and control your devices.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project utilizes the TP-Link Kasa Smart Home API for smart switch integration.
- Built with Python Flask.
