# Overview

This is a simple script which makes a USB-connected Wasatch Photonics spectrometer
accessible via BLE (Bluetooth Low Energy).

# Dependencies

- [Wasatch.PY](https://github.com/WasatchPhotonics/Wasatch.PY) for spectrometer interface
- [pybleno](https://github.com/Adam-Langley/pybleno) for BLE interface ("only tested on Linux Raspbian" :-)

# Invocation

Run the BLE service:

    $ sudo PYTHONPATH=/path/to/Wasatch.PY python -u main.py

(Sudo required because pybleno [uses raw sockets](https://github.com/Adam-Langley/pybleno/issues/12#issuecomment-386927390)).
