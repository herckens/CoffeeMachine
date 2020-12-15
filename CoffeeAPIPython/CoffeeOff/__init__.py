import logging

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = "HHAKeyVaultP"
keyVaultURI = f"https://{keyVaultName}.vault.azure.net"
DeviceName = "idefixRaspi"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connectionString = get_connection_string()
    hub = IoTHubRegistryManager(connectionString)
    
    hub.send_c2d_message(DeviceName, "coffeeoff")

    return func.HttpResponse(
            "The coffee off command has been sent successfully.",
            status_code=200
    )


def get_connection_string():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=keyVaultURI, credential=credential)
    connectionString = client.get_secret("IotHubServiceConnectionString").value
    return connectionString
