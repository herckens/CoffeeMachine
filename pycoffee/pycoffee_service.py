import os
import asyncio
import threading
import requests
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse

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
            message = await device_client.receive_message()
            print("the data in the message received was ")
            print(message.data)
            print("")
            if (message.data == "coffeeon"):
                response = requests.get(url = "http://myStrom-Coffee/relay?state=1")
                print("Executed coffeeon")
            elif (message.data == "coffeeoff"):
                response = requests.get(url = "http://myStrom-Coffee/relay?state=0")
                print("Executed coffeeoff")
            else:
                print("Command not recognized.")

    async def coffeeon_listener(device_client):
        while True:
            print("Wait for next coffeeon method call")
            method_request = await device_client.receive_method_request("coffeeon")
            response = requests.get(url = "http://myStrom-Coffee/relay?state=1")
            payload = {"result": response.ok}
            status = 200
            method_response = MethodResponse.create_from_method_request(method_request, status, payload)
            await device_client.send_method_response(method_response)
            print("Executed coffeeon")

    async def coffeeoff_listener(device_client):
        while True:
            print("Wait for next coffeeoff method call")
            method_request = await device_client.receive_method_request("coffeeoff")
            response = requests.get(url = "http://myStrom-Coffee/relay?state=0")
            payload = {"result": response.ok}
            status = 200
            method_response = MethodResponse.create_from_method_request(method_request, status, payload)
            await device_client.send_method_response(method_response)
            print("Executed coffeeoff")

    listeners = asyncio.gather(
        coffeeon_listener(device_client),
        coffeeoff_listener(device_client),
        message_listener(device_client)
    )

    await listeners
    print("The task completed.")

    # Finally, disconnect
    await device_client.disconnect()
    print("Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
