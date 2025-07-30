---
title: "NSG and UDR Support for Private Endpoints"
date: 2022-08-29
categories: 
  - "azure"
---

Hey Folks,

It's been a while since I blogged about something. This time it's about NSG and UDR support for Private endpoints. This feature is now publicly available. This was one of the most wanted features in Azure Networking.

Before we get into more details. Let's have some general understanding of what are private endpoints and what was the issue before and how this feature fixes all these issues.

## What are Private Endpoints?

According to MS documentation, "A private endpoint is a network interface that uses a private IP address from your virtual network. This network interface connects you privately and securely to a service that's powered by Azure Private Link"

Basically, Private endpoints allow you to connect to Microsoft Services to securely using a private address. So that the traffic will not flow thru MS public networks. This basically creates a network interface card for the services on a selected subnet.

## What were the issues/Limitations with Private Endpoints?

Now unlike regular network cards, these types of virtual network cards are a bit different. First:

- Private Endpoints only support TCP (not ICMP/UDP)
- They do not support NSG flow logs.
- Does not support UDR/NSG now **(Now it does)** :D.

So this particular feature fixed the last limitation in the list. Because private endpoints were unsupported by NSG before, we couldn't control the network traffic from the network layer. The only option we had was either from the service level network restriction or having access controls to limit the access to the service. But now with the support, we can restrict the inbound traffic to the public endpoints

UDR issue is a somewhat kind of annoying situation. By default, private endpoints will automatically create a /32 default route which will automatically propagate to the vnet route table it resides in and other peered VNETs

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/08/image.png)

By default, MS routing prioritizes the specific routes and also uses the following flow

- User-defined routes
- BGP routes
- System routes

Because of this if we have any private endpoints sitting in spoke networks, and also when spoke to spoke routing is forced via an Azure Firewall or an NVA, Traffic routing will be asymmetric

In a high-level

Traffic from the spoke A to Spoke B (where we have the private endpoint) resources uses the UDR to point to the Azure Firewall/NVA

The Azure firewall/NVA sees the destination traffic, processes the Network rules, and will route the traffic based on the published system routes for private endpoints.

But what happens is when PE will respond to the VM directly cause it does not honor the UDRs. and then the Assymatric routing will come into the picture.

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/08/image-1.png)

**But Luckily because of this new feature release, both of the above-mentioned issues are no longer there** :D

## Enabling NSG and UDR support for Private Endpoints

This feature enhancement will remove the need to create a /32 address prefix when defining custom routes. You will now have the ability to use a wider address prefix in the user-defined route tables for traffic destined to a private endpoint (PE) by way of a network virtual appliance (NVA). In order to leverage this feature, you will need to set a specific subnet level property, called PrivateEndpointNetworkPolicies, to be enabled on the subnet containing private endpoint resources.

### Enable using Powershell

```
$net = @{ 
Name = 'myVNet' ResourceGroupName = 'myResourceGroup' 
} 
$vnet = Get-AzVirtualNetwork @net 
$sub = @{ 
Name = 'default' VirtualNetwork = $vnet 
AddressPrefix = '10.1.0.0/24' 
PrivateEndpointNetworkPoliciesFlag = 'Enabled' 
} 
Set-AzVirtualNetworkSubnetConfig @sub $vnet | Set-AzVirtualNetwork
```

### Enable Using Bicep

```
    subnets: [ for subnet in subnets: {
      name: subnet.name
      properties: {
        addressPrefix: subnet.addressPrefix
        networkSecurityGroup: empty(subnet.networkSecurityGroup) ? json('null') : {
          id: subnet.networkSecurityGroup
        }
        routeTable: empty(subnet.routeTable) ? json('null') : {
          id: subnet.routeTable
        }
        privateEndpointNetworkPolicies: 'Enabled'
    }]
```
