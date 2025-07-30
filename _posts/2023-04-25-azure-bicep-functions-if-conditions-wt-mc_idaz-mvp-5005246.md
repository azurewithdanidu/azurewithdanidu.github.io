---
title: "Azure Bicep Functions - If conditions"
date: 2023-04-25
categories: 
  - "azure"
  - "azure-devops"
  - "bicep"
tags: 
  - "azure-bicep"
  - "biceps"
  - "conditional-deployment"
  - "conditions"
  - "devops"
  - "if-condition"
---

Howdy Folks

It's being sometimes I blogged about something. Today I'm here to talk about Bicep functions. This will be a series of blogs that I will be to illustrate how to use Bicep functions with use cases. Hopefully this will help someone. :)

## IF Conditions

[![](images/image-3.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/04/image-3.png)

At times, there may be a need to deploy a resource or module optionally in Bicep. This can be achieved by using the "if" keyword, which allows you to specify whether the resource or module should be deployed. The "if" condition evaluates to either true or false, and based on the evaluation, the resource is either created or not created. However, it's important to note that the "if" condition can only be applied to the entire resource or module, and not to individual properties.

There are few scenarios where we have to use if conditions.

1. Deploying Resource/ modules

3. When passing parameter/variable values to modules or resources

5. Defining variables

Once you understand the concept its going be quite useful and easy for you to articulate modules and main files using this.

MS Document - https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/conditional-resource-deployment

## Scenario

Based on project requirements, we need to deploy Azure APIM instance. Solution has 3 environments. Each environment would need three types of APIM.

Prod - Premium

SIT - Standard

Dev - Developer

For production environment customer wants to use selected public address. So that he can retain the same IP address incase if we redeploy the API instance

So here is what we are going to do.

We will be creating a public IP address only for the premium APIM and for the other do we are going to let Micrsoft choose the public IP address.

https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-ip-addresses

## Solution

- Preparing the IP address resource

I'm going to create one module file for all required components. IP address is one of those major ones. when doing the IP address resource I used an if condition as per below

```
resource publicIp 'Microsoft.Network/publicIpAddresses@2019-02-01' = if(contains(skuName,'Premium')) {
  name: publicIPAddressName
  location: location
  tags: !empty(tags) ? tags : json('null')  
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}
```

This statement "**contains(skuName,'Premium')**" will look at the skuName parameter, if the parameter value contains premium it will return the value as true. Since we used a if condition if condition will evaluate the output value from contains and deploy the IP address resource.

If the return value is false resource will not get deployed. :)

Now using if condition in this resource is not enough to address the situation.

> - Preparing publicip setting value using a if condition
> 
> Next step is use if condition when setting the public IP property value. So that here its is as below
> 
> Hopefully this explains how we can use the if condition in Azure. Bicep
> 
> **publicIpAddressId: contains(skuName,'Premium') ? publicIp.id : null // Only supported by Premium**
> 
> _Full Module File as per below_
> 
> ```
> // Deploys APIM that Standard Version
> 
> @description('Azure API Management Resource Name.')
> param apimName string
> 
> @description('Location of the resource.')
> param location string = resourceGroup().location
> 
> @description('Name of the Sku. VNET Integration only supported on Developer or Premium')
> 
> param skuName string = 'standard'
> 
> @description('Capacity of the SKU. For Consumption SKU capacity must be specified as 0.')
> param skuCapacity int
> 
> @description('Publisher Name')
> param publisherName string
> 
> @description('Publisher Email')
> param publisherEmail string
> 
> @description('Optional. List of Availability Zones to deploy to. Valid on in AZ regions.')
> param availabilityZones array = []
> 
> @description('Object containing resource tags.')
> param tags object = {}
> 
> 
> 
> var publicIPAddressName = '${apimName}-pip'
> 
> // Public IP Resource Definition
> resource publicIp 'Microsoft.Network/publicIpAddresses@2019-02-01' = if(contains(skuName,'Premium')) {
> name: publicIPAddressName
> location: location
> tags: !empty(tags) ? tags : json('null') 
> sku: {
> name: 'Standard'
> }
> properties: {
> publicIPAllocationMethod: 'Static'
> }
> }
> 
> // APIM Resource Definition
> resource apim 'Microsoft.ApiManagement/service@2021-01-01-preview' = {
> name: apimName
> location: location
> tags: !empty(tags) ? tags : json('null')
> sku: {
> capacity: skuCapacity
> name: skuName
> }
> identity: {
> type: 'SystemAssigned'
> }
> properties: {
> publicIpAddressId: contains(skuName,'Premium') ? publicIp.id : null // Only supported by Premium
> publisherEmail: publisherEmail
> publisherName: publisherName
> virtualNetworkConfiguration: null
> hostnameConfigurations: [
> {
> type: 'Proxy'
> hostName: '${apimName}.azure-api.net'
> negotiateClientCertificate: false
> defaultSslBinding: true
> certificateSource: 'BuiltIn'
> }
> ]
> customProperties: {
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TripleDes168': 'true'
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls11': 'true'
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls10': 'true'
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Ssl30': 'true'
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls11': 'true'
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls10': 'true'
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Ssl30': 'true'
> 'Microsoft.WindowsAzure.ApiManagement.Gateway.Protocols.Server.Http2': 'true'
> }
> virtualNetworkType: 'None'
> certificates:null
> disableGateway: false
> apiVersionConstraint: {}
> }
> zones: empty(availabilityZones) ? json('null') : availabilityZones
> 
> }
> 
> ```
> 
> Now we have usual operators for the if conditions.

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/04/image-1.png)

[![](images/image-2.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/04/image-2.png)

If you want to know more about if conditions and operators following Microsoft documents will help you

https://learn.microsoft.com/en-us/training/modules/build-flexible-bicep-templates-conditions-loops/

https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/operators-logical

https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/operators
