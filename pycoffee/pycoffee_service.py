# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
print("1")

import os
import asyncio
from six.moves import input
import threading
import time
import requests
from azure.iot.device.aio import IoTHubDeviceClient

print("Starting")

async def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're reading from a file here.
    with open("/home/pi/src/pycoffee/connection_string.txt") as f:
        conn_str = f.read()

    print("Connection string:" + conn_str)


    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    await device_client.connect()

    # define behavior for receiving a message
    async def message_listener(device_client):
        while True:
            print("Wait for next message...")
            message = await device_client.receive_message()  # blocking call
            print("the data in the message received was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)
            print("content Type: {0}".format(message.content_type))
            print("")
            response = requests.get(url = "http://myStrom-Coffee/toggle")

    # define behavior for halting the application
    def stdin_listener():
        while True:
            print("running...")
            #time.sleep(1)
            #selection = input("Press Q to quit\n")
            #if selection == "Q" or selection == "q":
            #    print("Quitting...")
            #    break

    # Schedule task for message listener
    task = asyncio.create_task(message_listener(device_client))
    print("Task created. Now awaiting completion...")
    await task
    print("The task completed.")

    ## Run the stdin listener in the event loop
    #loop = asyncio.get_running_loop()
    #user_finished = loop.run_in_executor(None, stdin_listener)

    ## Wait for user to indicate they are done listening for messages
    #await user_finished

    # Finally, disconnect
    await device_client.disconnect()


if __name__ == "__main__":
    print("Starting in __main__")
    asyncio.run(main())

#    # define behavior for receiving a message
#    async def message_listener(device_client):
#        while True:
#            print("Start listening for message.")
#            message = await device_client.receive_message()  # blocking call
#            print("the data in the message received was ")
#            print(message.data)
#            print("custom properties are")
#            print(message.custom_properties)
#            print("content Type: {0}".format(message.content_type))
#            print("")
#            response = requests.get(url = "http://myStrom-Coffee/toggle")
