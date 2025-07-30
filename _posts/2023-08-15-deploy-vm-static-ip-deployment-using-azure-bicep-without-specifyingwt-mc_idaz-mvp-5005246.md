---
title: "Deploy VM Static IP Deployment Using Azure Bicep (Without Specifying)"
date: 2023-08-15
categories: 
  - "azure"
  - "azure-devops"
tags: 
  - "bicep"
  - "devops"
---

Howdy Folks

It's been some time since I last delved into a technical discussion on Azure Bicep, and today's subject promises to be an intriguing one: the deployment of Azure virtual machines (VMs) with static IPs. Specifically, we'll explore the methodology of dynamically allocating a static IP without explicitly designating what that IP is. Put differently, the objective here is to select the next available IP in a virtual network subnet and fix it as a static address for the VM, all within the same template.

Certainly, there are alternative routes to achieve this, such as utilizing Azure Command-Line Interface (CLI) or Azure PowerShell. But what caught my intellectual curiosity was the question of whether this could be accomplished solely using Azure Bicep. The pursuit of this possibility led me to the following approach, which I believe fellow enthusiasts and technical experts will find both challenging and rewarding.

I won't claim that this solution is perfect, but it gets the job done. There might be other ways to do this, but I think this approach is the closest one that uses only Azure Bicep as a language. And one of the good things about this is Azure will find the next available IP address for us :).

## high-level steps.

1. Create a seperate module for VM Nic

3. Called the VM nic module twice inside the VM Module
    - First step is to create a nic using dynamic ip
    
    - Output the IP from the first module run and use it as an input for the second time to make it static.

hopefully below diagram may help you.

[![](images/image-6.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/08/image-6.png)

## Bicep templates

### NIC Module

```
@description('Virtual machine name. Do not include numerical identifier.')
@maxLength(14)
param virtualMachineNameSuffix string

@description('Virtual machine location.')
param location string = resourceGroup().location

@description('Resource Id of Subnet to place VM into.')
param subnetId string

@description('Private IP address')
param privateIpAddress string = ''

param privateIPAllocationMethod string = 'dynamic'

@description('Object containing resource tags.')
param tags object = {}

resource staticNic 'Microsoft.Network/networkInterfaces@2021-02-01' =  {
  name: '${virtualMachineNameSuffix}-nic01'
  location: location
  tags: !empty(tags) ? tags : json('null')
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          subnet: {
            id: subnetId
          }
          privateIPAllocationMethod: privateIPAllocationMethod
          privateIPAddress:(privateIPAllocationMethod =='Dynamic') ? null: privateIpAddress
        }
      }
    ]
  }
}

output nicId string = staticNic.id
output nicName string = staticNic.name
output ipAddress string = staticNic.properties.ipConfigurations[0].properties.privateIPAddress
```

Note - Following output line is the critical part of exporting the assigned IP.

**output ipAddress string = staticNic.properties.ipConfigurations\[0\].properties.privateIPAddress**

### VM Module (NIC Part)

If you look a the first module call, we are basically deploying the NIC using dynamic allocation method to get the next available IP for us. And in the second call we are using the output from first call. (Highlighted)

```
module nic 'virtual-machine-nic.bicep' = {
  name: '${virtualMachineNameSuffix}-nic01-deployment'
  params: {
    location: location
    subnetId: subnetId
    virtualMachineNameSuffix: virtualMachineNameSuffix
    privateIPAllocationMethod:'Dynamic'
  }
}

module nicStaticIp 'virtual-machine-nic.bicep' = {
  name: '${virtualMachineNameSuffix}-nic01-deployment-static'
  params: {
    location: location
    subnetId: subnetId
    virtualMachineNameSuffix: virtualMachineNameSuffix
    privateIPAllocationMethod:'Static'
    privateIpAddress:nic.outputs.ipAddress
  }
}

you can get the full code in my GitHub below.
https://github.com/DaniduWeerasinghe911/Azure-Bicep-Static-IP-VM-Deployment/tree/main
```

In conclusion, the exploration into deploying Azure virtual machines with static IPs using Azure Bicep has proven to be a fascinating and rewarding endeavor. Although the solution might not be the only approach, it represents a well-crafted method that leverages the power of Azure Bicep as a sole language. By orchestrating the dynamic allocation of IPs and transforming them into static assignments, we've managed to streamline a critical aspect of VM management. This method not only simplifies the process but also aligns with the evolving landscape of cloud infrastructure management. It is a testament to the flexibility and robustness of Azure Bicep and underscores the possibilities that await those eager to delve into the intricacies of cloud automation. For enthusiasts and professionals alike, it opens a new avenue to explore, refine, and innovate.

As always reach out to me if you have any questions or suggestions. :)

Until next time....
