# Driver for Fantech X9 Thor

This is an open-source driver for the Fantech X9 Thor RGB gaming mouse targeted for linux systems (although it should work in any environment that supports gtk).

### Requirements

The project is written in python3 so that's a core requirement. 

`Gtk3` and `gobject-introspection` are required for the GUI to work, refer to your distro's documentation on how to get those installed, although a lot of popular distros will have it pre-installed so you can skip to the next step if it is.

The following python module is also required:
1. `pyusb`

To install the module simply running `pip install pyusb` should suffice (if you don't have pip refer to your distro's documentation on how to get it).

Some distros (like arch) also provide standalone packages that will install pyusb to your system so search in your repos if you'd prefer your package manager to handle it for you instead of pip.

### Usage
Simply clone the repo using git.

`git clone https://github.com/GuessWhatBBQ/FantechX9ThorDriver.git`

Run the file called driver_frontend.py using python

`python driver_frontend.py`

On a side note:
Since python needs access to the usb ports, it might require appropriate UDEV rules to be set up ([see here](https://wiki.archlinux.org/index.php/udev#Accessing_firmware_programmers_and_USB_virtual_comm_devices)) or the program to be run as root (the easier way but absolutely not recommended).

The easy way being: `sudo python driver_frontend.py` (but again this is absolutely not recommended, use at your own risk).

Since the project is written in python you can simply download the 2 files (driver_backend.py and driver_frontend.py) to the same folder and achieve the same functionality.

The current configuration you have set will be saved when the `save configuration` button is pressed, in a file called **driver.conf** in the same folder the program is run from.  

#### It should look similar to this (depends on gtk theme):

![example](https://i.imgur.com/mAXCjX2.png)
