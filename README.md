# Driver for Fantech X9 Thor

This is an open-source driver for the Fantech X9 Thor RGB gaming mouse targeted for linux systems (although it should work in any environment that supports gtk).

### Requirements
The following python modules are required:
1. `pyusb`

2. `gdk` *

3. `gtk` *

\* = Module not required if you simply want to use the backend (althouhgh the backend is designed like a library so cant provide a lot of functionality unless its modified to behave like a script)

### Usage
Simply clone the repo and run the driver_frontend.py file. Since the project is written in python you can simply download the 2 files (driver_backend.py and driver_frontend.py) to the same folder and achieve the same functionality.

The current configuration you have set will be saved when the `save configuration` button is pressed, in a file called **driver.conf** in the same folder the program is run from.  

#### It should look similar to this (depends on gtk theme):

![example](https://i.imgur.com/mAXCjX2.png)
