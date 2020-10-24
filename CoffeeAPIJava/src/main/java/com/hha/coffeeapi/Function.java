package com.hha.coffeeapi;

import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import com.microsoft.azure.functions.ExecutionContext;
import com.microsoft.azure.functions.HttpMethod;
import com.microsoft.azure.functions.HttpRequestMessage;
import com.microsoft.azure.functions.HttpResponseMessage;
import com.microsoft.azure.functions.HttpStatus;
import com.microsoft.azure.functions.annotation.AuthorizationLevel;
import com.microsoft.azure.functions.annotation.FunctionName;
import com.microsoft.azure.functions.annotation.HttpTrigger;
import com.microsoft.azure.sdk.iot.service.*;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.security.keyvault.secrets.SecretClient;
import com.azure.security.keyvault.secrets.SecretClientBuilder;
import com.azure.security.keyvault.secrets.models.KeyVaultSecret;

/**
 * Azure Functions with HTTP Trigger.
 */
public class Function {
    private static final String IOT_HUB_SERVICE_CONNECTION_STRING = "IotHubServiceConnectionString";
    private static final String DEVICE_ID = "idefixRaspi1";
    private static final String KEY_VAULT_NAME = "hhakeyvault";
    private static final IotHubServiceClientProtocol protocol = IotHubServiceClientProtocol.AMQPS;

    private ServiceClient serviceClient;

    @FunctionName("CoffeeOn")
    public HttpResponseMessage runCoffeeOn(@HttpTrigger(name = "req", methods = { HttpMethod.GET,
            HttpMethod.POST }, authLevel = AuthorizationLevel.ANONYMOUS) HttpRequestMessage<Optional<String>> request,
            final ExecutionContext context) throws UnsupportedEncodingException {
        Logger log = context.getLogger();
        log.info("CoffeeOn triggered by HTTP request.");
        var connectionString = getConnectionString(log);
        openServiceClient(log, connectionString);
        sendMessageToDevice("coffeeon");
        closeServiceClient(log);
        return request.createResponseBuilder(HttpStatus.OK).body("Sent coffeeon message.").build();
    }

    @FunctionName("CoffeeOff")
    public HttpResponseMessage runCoffeeOff(@HttpTrigger(name = "req", methods = { HttpMethod.GET,
            HttpMethod.POST }, authLevel = AuthorizationLevel.ANONYMOUS) HttpRequestMessage<Optional<String>> request,
            final ExecutionContext context) throws UnsupportedEncodingException {
        Logger log = context.getLogger();
        log.info("CoffeeOff triggered by HTTP request.");
        var connectionString = getConnectionString(log);
        openServiceClient(log, connectionString);
        sendMessageToDevice("coffeeoff");
        closeServiceClient(log);
        return request.createResponseBuilder(HttpStatus.OK).body("Sent coffeeoff message.").build();
    }

    private void sendMessageToDevice(String message) throws UnsupportedEncodingException {
        Message messageToSend = new Message(message);
        messageToSend.setDeliveryAcknowledgementFinal(DeliveryAcknowledgement.Full);

        // Setting standard properties
        messageToSend.setMessageId(java.util.UUID.randomUUID().toString());

        // send the message
        CompletableFuture<Void> future = serviceClient.sendAsync(DEVICE_ID, messageToSend);
        try {
            future.get(30, TimeUnit.SECONDS);
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            e.printStackTrace();
        }
    }

    private String getConnectionString(Logger log) {
        final String kvUri = "https://" + KEY_VAULT_NAME + ".vault.azure.net";

        SecretClient secretClient = new SecretClientBuilder().vaultUrl(kvUri)
                .credential(new DefaultAzureCredentialBuilder().build()).buildClient();

        KeyVaultSecret retrievedSecret = secretClient.getSecret(IOT_HUB_SERVICE_CONNECTION_STRING);
        var connectionString = retrievedSecret.getValue();

        if (connectionString == null) {
            var message = "Could not find the IoT Hub Connection String in the environment variable " + IOT_HUB_SERVICE_CONNECTION_STRING + ". Make sure it is available in Azure Key Vault or exported as env variable in your development environment.";
            log.log(Level.SEVERE, message);
        }

        return connectionString;
    }

    private void openServiceClient(Logger log, String connectionString) {
        log.info("Creating ServiceClient...");
        try {
            serviceClient = ServiceClient.createFromConnectionString(connectionString, protocol);
        } catch (IOException e1) {
            e1.printStackTrace();
        }

        CompletableFuture<Void> future = serviceClient.openAsync();
        try {
            future.get();
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
        log.info("********* Successfully created a ServiceClient.");
    }

    private void closeServiceClient(Logger log) {
        try {
            serviceClient.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        CompletableFuture<Void> future = serviceClient.closeAsync();
        try {
            future.get();
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }

        serviceClient = null;
        log.info("********* Successfully closed ServiceClient.");
    }
}
