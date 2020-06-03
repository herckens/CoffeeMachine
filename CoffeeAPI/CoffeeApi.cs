using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Net.Http;
using Microsoft.Azure.Devices;
using System.Text;

namespace CoffeeAPI
{
    public static class CoffeeApi
    {
        static ServiceClient serviceClient;

        [FunctionName("CoffeeOn")]
        public static async Task<IActionResult> RunCoffeeOn(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("CoffeeOn triggered by HTTP request.");

            var connectionString = GetConnectionString(log);
            log.LogInformation("Got the connection string.");

            serviceClient = ServiceClient.CreateFromConnectionString(connectionString);
            log.LogInformation("Connected to IoT Hub.");
            var commandMessage = new Message(Encoding.ASCII.GetBytes("Cloud to device message."));
            var timeout = TimeSpan.FromSeconds(10);
            await serviceClient.SendAsync("idefixRaspi1", commandMessage, timeout);
            log.LogInformation("Message is sent.");

            string responseMessage = "The request has successfully been sent to IoT Hub.";
            return new OkObjectResult(responseMessage);
        }

        [FunctionName("CoffeeOff")]
        public static async Task<IActionResult> RunCoffeeOff(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("CoffeeOff triggered by HTTP request.");

            var connectionString = GetConnectionString(log);
            log.LogInformation("Got the connection string.");

            serviceClient = ServiceClient.CreateFromConnectionString(connectionString);
            log.LogInformation("Connected to IoT Hub.");
            var commandMessage = new Message(Encoding.ASCII.GetBytes("Cloud to device message."));
            var timeout = TimeSpan.FromSeconds(10);
            await serviceClient.SendAsync("idefixRaspi1", commandMessage, timeout);
            log.LogInformation("Message is sent.");

            string responseMessage = "The request has successfully been sent to IoT Hub.";
            return new OkObjectResult(responseMessage);
        }

        private static string GetConnectionString(ILogger log)
        {
            var connectionString = Environment.GetEnvironmentVariable("IotHubServiceConnectionString");

            if (connectionString == null)
            {
                var message = "Could not find the IoT Hub Connection String in the environment variable IotHubServiceConnectionString. Make sure it is available in Azure Key Vault or exported as env variable in your development environment.";
                log.LogError(message);
                throw new InvalidOperationException(message);
            }

            return connectionString;
        }
    }
}
