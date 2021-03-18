using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Microsoft.Azure.Devices;
using Azure.Security.KeyVault.Secrets;
using Azure.Identity;

namespace Hha.CoffeeMachine
{
    public static class CoffeeApi
    {
        private const string DeviceName = "idefixRaspi";
        private const string KeyVaultName = "HHAKeyVaultP";
        static ServiceClient serviceClient;

        [FunctionName("CoffeeOn")]
        public static async Task<IActionResult> RunCoffeeOn(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("CoffeeOn triggered by HTTP request.");

            var connectionString = await GetConnectionStringAsync(log);
            log.LogInformation("Got the connection string.");

            serviceClient = ServiceClient.CreateFromConnectionString(connectionString);
            log.LogInformation("Connected to IoT Hub.");

            var methodInvocation = new CloudToDeviceMethod("coffeeon") { ResponseTimeout = TimeSpan.FromSeconds(30) };
            methodInvocation.SetPayloadJson("10");
            var response = await serviceClient.InvokeDeviceMethodAsync(DeviceName, methodInvocation);

            string responseMessage = $"The 'CoffeeOn' request has successfully been sent to IoT Hub. Response: {response.Status}";
            return new OkObjectResult(responseMessage);
        }

        [FunctionName("CoffeeOff")]
        public static async Task<IActionResult> RunCoffeeOff(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("CoffeeOff triggered by HTTP request.");

            var connectionString = await GetConnectionStringAsync(log);
            log.LogInformation("Got the connection string.");

            serviceClient = ServiceClient.CreateFromConnectionString(connectionString);
            log.LogInformation("Connected to IoT Hub.");

            var methodInvocation = new CloudToDeviceMethod("coffeeoff") { ResponseTimeout = TimeSpan.FromSeconds(30) };
            methodInvocation.SetPayloadJson("10");
            var response = await serviceClient.InvokeDeviceMethodAsync(DeviceName, methodInvocation);

            string responseMessage = $"The 'CoffeeOff' request has successfully been sent to IoT Hub. Response: {response.Status}";
            return new OkObjectResult(responseMessage);
        }

        private static async Task<string> GetConnectionStringAsync(ILogger log)
        {
            var kvUri = "https://" + KeyVaultName + ".vault.azure.net";
            var client = new SecretClient(new Uri(kvUri), new DefaultAzureCredential());

            string connectionString;
            try
            {
                var keyVaultResponse = await client.GetSecretAsync("IotHubServiceConnectionString");
                connectionString = keyVaultResponse.Value.Value;
            }
            catch (Exception e)
            {
                var message = $"Could not get the IoT Hub Connection String from Azure Key Vault. Make sure it is available in Azure Key Vault. Exception: {e.Message}";
                log.LogError(message);
                throw e;
            }

            return connectionString;
        }
    }
}
