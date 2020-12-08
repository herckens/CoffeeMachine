Place your Azure IoT Hub connection string into a file called "connection_string.txt" in this folder.

Install azure-iot-device module for user and root.
    $ pip3 install azure-iot-device
    $ sudo pip3 install azure-iot-device

Set up as a systemd service:
    $ sudo cp pycoffee.service /lib/systemd/system/
    $ sudo systemctl enable pycoffee.service
    $ sudo systemctl start pycoffee.service
