import os
import asyncio
import threading
import requests
from azure.iot.device.aio import IoTHubDeviceClient

print("Starting")

async def main():
    # Read IoT Hub connection string from file.
    with open("/home/pi/src/CoffeeMachine/pycoffee/connection_string.txt") as f:
        conn_str = f.read()

    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    await device_client.connect()

    async def message_listener(device_client):
        while True:
            print("Wait for next message...")
            message = await device_client.receive_message()  # blocking call
            print("the data in the message received was ")
            print(message.data)
            print("")
            response = requests.get(url = "http://myStrom-Coffee/toggle")

    task = asyncio.create_task(message_listener(device_client))
    print("Task created. Now awaiting completion...")
    await task
    print("The task completed.")

    # Finally, disconnect
    await device_client.disconnect()
    print("Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
