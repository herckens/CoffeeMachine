Place your Azure IoT Hub connection string into a file called "connection_string.txt" in this folder.

Set up as a systemd service:
    $ sudo cp pycoffee.service /lib/systemd/system/
    $ sudo systemctl enable pycoffee.service
    $ sudo systemctl start pycoffee.service
