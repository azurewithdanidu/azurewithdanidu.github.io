---
title: "Azure Bastion Sharable Link Clean Up"
date: 2023-08-26
categories: 
  - "azure"
  - "powershell"
tags: 
  - "azureapi"
  - "azurebastion"
  - "azurevm"
  - "bastion"
  - "sharablelinks"
---

Howdy Folks

This time it's about Azure Bastion. There was a requirement in one of the recent projects around Azure Bastion Sharable Links. Before we get into more details let's talk about what are the sharable links

## Overview

As per Microsoft,

"The Bastion **Shareable Link** feature lets users connect to a target resource (virtual machine or virtual machine scale set) using Azure Bastion without accessing the Azure portal. This article helps you use the Shareable Link feature to create a shareable link for an existing Azure Bastion deployment.

[![](images/image-7.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/08/image-7.png)

When a user without Azure credentials clicks a shareable link, a webpage opens that prompts the user to sign into the target resource via RDP or SSH. Users authenticate using username and password or private key, depending on what you have configured for the target resource. The shareable link does not contain any credentials - the admin must provide sign-in credentials to the user."

This is a pretty good addition to Azure Bastion, but it does come with a security flow too. Since we will be sharing these links with external users/vendors, Links that we generate does not expire or cannot set an expiry at the moment. I'm sure MS will give this option really soon.

But until then requirement was

Automatically delete these links every day at 12am, So vendors would need to talk to the internal IT department to get access again.

## Solution.

At the moment we have 2 options to achieve this. either thru GUI or using API. So, there is no PowerShell option. So, I came up with a script to perform the cleanup using Azure Automation Runbook.

### Explanation -

Azure automation service principal was granted following permissions.

- Microsoft.Network/bastionHosts/deleteShareableLinks/action

- Microsoft.Network/bastionHosts/deleteShareableLinksByToken/action

- Microsoft.Network/bastionHosts/getShareableLinks/action

Script will

1. Query the tenant to get the bastion details

3. Go thru all the subscriptions to query all the virtual machines with sharable links

5. Make sure links are not more than 1 day older, if so, it will delete the link.

You need to update the script with subscription id where you have the bastion. deployed.

Following is the script

```
# Define the subscription ID for the platform/Bastion Service
$PlatformSubscriptionId = ""

# Define header for HTTP requests
$header = @{
    "Content-Type" = "application/json"
    # Acquire token for authentication
    Authorization  = ("Bearer " + (Get-AzAccessToken).Token)
}

# Select the given subscription
select-azsubscription -SubscriptionId $PlatformSubscriptionId

# Attempt to retrieve Bastion information; suppress any errors
$azBastion = Get-AzBastion -ErrorAction SilentlyContinue   

# Check if the Bastion provisioning was successful
if ($azBastion.ProvisioningState -eq "Succeeded") {
    # Extract necessary details from the Bastion information
    $ResourceGroupName = $azBastion.ResourceGroupName
    $SubscriptionId = $azBastion.Id.Split('/')[2]
    $Name = $azBastion.Name      

    Write-Output "🔵 Bastion Host Name: $name"

    # Define the URI for the shareable link request
    $uri = "https://management.azure.com/subscriptions/$($PlatformSubscriptionId)/resourceGroups/$($azBastion.ResourceGroupName)/providers/Microsoft.Network/bastionHosts/$($azBastion.Name)/GetShareableLinks?api-version=2023-02-01"
    
    # Retrieve a list of all subscriptions
    $SubscriptionList = Get-AzSubscription | Select-Object Id, Name

    # Iterate over each subscription
    foreach ($sub in $SubscriptionList) {
        select-azsubscription -SubscriptionId $sub.Id
        Write-Output "Processing Subscription $($sub.Name)"

        # Fetch all VMs under the current subscription
        $vmList = Get-AzVm

        # Iterate over each VM in the subscription
        foreach ($vm in $vmList) {         
            Write-Host "Processing VM $($vm.Name)"
            $requestBody =""
            # Define the request body to get shareable link for the VM
            $requestBody = @{
                "vms" = @(
                    @{
                        "vm" = @{
                            "id" = $vm.Id
                        }
                    }
                )
            }

            # Check if request body exists and is not null
            if ($null -ne $requestBody) {    
                # Make HTTP request to fetch shareable link
                $getBastionLink = Invoke-RestMethod -Method Post -Uri $uri -Headers $header -Body (ConvertTo-Json $requestBody -Depth 10) -SkipHttpErrorCheck   
                
                # Check if the link exists
                if ($null -ne $getBastionLink.value) {
                    # Convert string date to DateTime object
                    $convertedDate = [DateTime]::parseexact($getBastionLink.value.createdAt,"MM/dd/yyyy HH:mm:ss",[System.Globalization.CultureInfo]::InvariantCulture)
                    # Calculate difference in days from link creation date to now
                    $daysDifference = (Get-Date) - $convertedDate
                    
                    # Check if link was created more than 1 days ago
                    if ($daysDifference.Days -gt 1) {
                        # Print details and potentially delete old links
                        Write-Output "Deleting the Shareable Link for the Virtual Machine: $($vm.Name)"
                        $uri = "https://management.azure.com/subscriptions/$($PlatformSubscriptionId)/resourceGroups/$($azBastion.ResourceGroupName)/providers/Microsoft.Network/bastionHosts/$($azBastion.Name)/deleteShareableLinks?api-version=2023-02-01"                 
                        $output = Invoke-WebRequest -Method Post -Uri $uri -Headers $header -Body (ConvertTo-Json $requestBody -Depth 10) 
                    }
                    else {
                        # The link is not older than 1 days
                        Write-Output "The date is not older than 1 days."
                        continue  
                    } 
                }
                else {
                    # No ABS Link for the VM
                    # Write-Output "ABS Link does not exist for the Virtual Machine: $($vm.Name)" 
                    continue     
                }                  
            }
            else {
                # Something went wrong, potentially with the VM
                Write-Output "VM $($vm.Name) Something went wrong."
                continue  
            }
        }
    }
}
else {
    # No Azure Bastion was found in the provided subscription
    Write-Output "NO Azure Bastion Exists within the permitted subscription."
    continue
}
```

Following is the link to my GitHub page. Please feel free to comment if you got any questions or feel free to contribute to GitHub with any changes.

Github --> https://github.com/DaniduWeerasinghe911/Azure-Bastion-Link-Cleanup/tree/main

Microsoft Reference --> https://learn.microsoft.com/en-us/azure/bastion/shareable-link
