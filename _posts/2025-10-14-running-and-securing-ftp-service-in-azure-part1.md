---
title: "Running And Securing FTP Service in Azure"
date: 2025-10-14
categories:
  - azure
  - azure-infrastructure
  - ftp
  - security
  - storage
tags:
  - bicep
  - compute
  - infrastructure
  - networking
  - security
  - storage
---

Howdy Folks,

In this post, we will explore how to set up and secure an FTP service in Microsoft Azure. FTP (File Transfer Protocol) is a standard network protocol used for transferring files between a client and server. While FTP is widely used, it is important to implement security measures to protect data during transfer. Mostly we talk about hosting app services, databases, and other cloud-native solutions, but sometimes you need to run legacy services like FTP. In this guide, we will cover the necessary steps to deploy an FTP service in Azure using Azure Blob Storage for file storage, and we will implement security best practices to ensure safe file transfers.

Let's get started!

## FTP Architecture Options in Azure

First, let's talk about a few possible architectures for running FTP in Azure using Storage Accounts. The architecture depends on your requirements, current environment, and budget. Here are a few common architectures:

### 1. SFTP Enabled Storage Account with Storage Account Firewall

- Use Azure Blob Storage with SFTP enabled for secure file transfers.
- Configure the Storage Account firewall to restrict access to specific IP addresses or virtual networks.
- This is the simplest and most cost-effective solution for secure file transfers.

![SFTP Storage Account with Firewall](/assets/img/posts/2025-10-14-image.png)

### 2. SFTP Enabled Storage Account with Azure Firewall Configuration

- Use Azure Blob Storage with SFTP enabled for secure file transfers.
- Configure Azure Firewall to restrict access to the Storage Account based on IP addresses or virtual networks.
- This solution provides an additional layer of security by leveraging Azure Firewall capabilities.
- This will be a bit more expensive than the first option.
- Also, this will provide more visibility and control over the traffic.

![SFTP Storage Account with Azure Firewall](/assets/img/posts/2025-10-14-image-1.png)

---

## Option 1: Storage Account with Firewall

Okay, let's dive into the steps to set up and secure an FTP service in Azure using the first architecture option:

### Step 1: Create an Azure Storage Account with SFTP Enabled

When you are creating a new storage account, make sure to enable **Hierarchical namespace**. Only then can you use the SFTP feature in storage accounts.

![Storage Account Creation with Hierarchical Namespace](/assets/img/posts/2025-10-14-image.png)

### Step 2: Configure SFTP on the Storage Account

1. Navigate to the Storage Account in the Azure portal.
2. Under **Settings**, you will find the **SFTP** option. Click on it.

   ![SFTP Configuration in Azure Portal](/assets/img/posts/2025-10-14-image-1.png)

3. Enable SFTP and configure the required settings, such as authentication methods (SSH keys or password).
4. Create local users for SFTP access and assign appropriate permissions to the Blob containers.

> **Note**: At the moment, you can only create local users. You cannot use Azure AD users for SFTP access.

![SFTP Local User Configuration](/assets/img/posts/2025-10-14-image-2.png)

As you can see when creating a local user, you can select the authentication type, either SSH or password. You can also assign permissions to specific containers in the storage account.

You can find more details about configuring the SFTP feature in the [official documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/secure-file-transfer-protocol-support?tabs=azure-portal).

But the most important part is to secure the storage account, so let's move to the next step.
### Step 3: Secure the Storage Account

1. Navigate to the Storage Account in the Azure portal.
2. Under **Security + networking**, select **Networking**.
3. Click **Manage public network access** and allow traffic from selected networks.
4. Configure the firewall settings to restrict access to the Storage Account from specific IP addresses or virtual networks.

This is where you limit the access to the storage account from specific networks. Specifically, if it's outside of your network, you can whitelist the IP addresses that can access the storage account.

![Storage Account Networking Configuration](/assets/img/posts/2025-10-14-image-3.png)

### Security Analysis: Pros and Cons

Now let's see how secure this is and what visibility we have into the traffic.

#### Pros

1. This option provides basic layer 3 and layer 4 security. You can restrict access to the storage account based on IP addresses and virtual networks.
2. This is fairly simple and cost-effective to set up.
3. You can enable diagnostic settings to log and monitor access to the storage account, but you could only track the following operations: Storage Read, Storage Write, Storage Delete, and Transaction.
4. You can possibly enable Defender for Storage accounts to get threat protection for your storage account.

#### Cons

1. You cannot inspect the traffic. You can only restrict access based on IP addresses and virtual networks.
2. This option cannot centralize the entry point for your traffic or force traffic inspection.
3. You can only use local users for SFTP access. You cannot use Azure AD users or managed identities. :(

![Storage Account Security and Limitations](/assets/img/posts/2025-10-14-image-4.png)

### Infrastructure as Code: Bicep Template

If you want to set everything up using infrastructure as code, here is a sample Bicep code to create a storage account with SFTP enabled and firewall rules configured:

```bicep
@description('The name of the storage account')
param storageAccountName string = 'stsftp${uniqueString(resourceGroup().id)}'

@description('The location for all resources')
param location string = resourceGroup().location

@description('The environment name (dev, staging, prod)')
param environment string = 'dev'

@description('Allowed IP addresses for storage account firewall')
param allowedIpAddresses array = []

@description('SFTP local user configurations')
param sftpUsers array = [
  {
    name: 'sftpuser1'
    homeDirectory: 'uploads'
    permissionScopes: [
      {
        permissions: 'rcwdl'
        service: 'blob'
        resourceName: 'uploads'
      }
    ]
    hasSharedKey: false
    hasSshKey: true
    hasSshPassword: false
  }
]

// Deploy Storage Account using AVM module
module storageAccount 'br/public:avm/res/storage/storage-account:0.9.1' = {
  name: 'storageAccountDeployment'
  params: {
    name: storageAccountName
    location: location
    skuName: 'Standard_LRS'
    kind: 'StorageV2'
    
    // Enable hierarchical namespace for SFTP
    isHnsEnabled: true
    
    // Enable SFTP
    isSftpEnabled: true
    
    // Local users for SFTP
    localUsers: sftpUsers
    
    // Network access configuration
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
      ipRules: [for ip in allowedIpAddresses: {
        value: ip
        action: 'Allow'
      }]
    }
    
    // Enable blob public access
    allowBlobPublicAccess: false
    
    // Security settings
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    
    // Diagnostic settings
    diagnosticSettings: [
      {
        name: 'storageAccountDiagnostics'
        workspaceResourceId: '/subscriptions/${subscription().subscriptionId}/resourceGroups/${resourceGroup().name}/providers/Microsoft.OperationalInsights/workspaces/law-${environment}-${location}'
        logCategoriesAndGroups: [
          {
            categoryGroup: 'allLogs'
            enabled: true
          }
        ]
        metricCategories: [
          {
            category: 'Transaction'
            enabled: true
          }
        ]
      }
    ]
    
    // Tags
    tags: {
      Environment: environment
      Purpose: 'SFTP File Transfer'
      CreatedBy: 'Bicep-AVM'
    }
  }
}

// Create blob container for uploads
module blobContainer 'br/public:avm/res/storage/storage-account/blob-service/container:0.2.1' = {
  name: 'uploadsContainerDeployment'
  params: {
    storageAccountName: storageAccount.outputs.name
    name: 'uploads'
    publicAccess: 'None'
  }
  dependsOn: [
    storageAccount
  ]
}

// Output important information
output storageAccountName string = storageAccount.outputs.name
output sftpEndpoint string = storageAccount.outputs.primaryEndpoints.dfs
output storageAccountId string = storageAccount.outputs.resourceId
output sftpHostname string = '${storageAccountName}.blob.core.windows.net'

```


This Bicep code creates an Azure Storage Account with SFTP enabled, configures local users for SFTP access, and sets up firewall rules to restrict access based on specified IP addresses. It also creates a Blob container for file uploads.

---

## Option 2: Storage Account with Azure Firewall

Okay, now let's look at our slightly more complex architecture using Azure Firewall to secure the storage account.

In this architecture, we will use Azure Blob Storage with SFTP enabled for secure file transfers. We will configure Azure Firewall to restrict access to the Storage Account based on IP addresses or virtual networks. This solution provides an additional layer of security by leveraging Azure Firewall capabilities.

![Azure Firewall SFTP Architecture](/assets/img/posts/2025-10-20-image.png)

### Step 1: Create an Azure Storage Account with SFTP Enabled

The first step is to create an Azure Storage Account with SFTP enabled, as we did in the previous section. Make sure to enable **Hierarchical namespace** when creating the storage account.

![Storage Account Creation with HNS Enabled](/assets/img/posts/2025-10-14-image.png)

For the other steps, please refer to the steps above.

### Step 2: Additional Configuration Steps

The additional steps in this process are going to be:

1. Creating a private endpoint for the blob endpoint of the storage account
2. Setting up Azure Firewall with required rules to allow traffic to the storage account via the private endpoint

Let's get started!

### Step 3: Create a Private Endpoint for the Storage Account

1. Navigate to the Storage Account in the Azure portal.
2. Under **Settings**, select **Private endpoint connections** and click on **+ Private endpoint**.
3. Follow the wizard to create a private endpoint for the blob service of the storage account. Make sure to select the appropriate virtual network and subnet where the Azure Firewall is deployed.

Below is my private endpoint configuration:

![Private Endpoint Configuration for Storage Account](/assets/img/posts/2025-10-20-image-1.png)

> **Note**: Since we are dealing with network layer traffic, private endpoint DNS configuration is not that important. I'll show you why in the next step.

### Step 4: Configure Azure Firewall

Now let's move into the Azure Firewall configuration.

Below is the **DNAT rule** in the Azure Firewall. This is where we are mapping the internal IP address with the public IP address of the firewall.

![Azure Firewall DNAT Rule Configuration](/assets/img/posts/2025-10-20-image-2.png)

And then we can have a **network rule** to allow traffic from specific IP addresses to the private endpoint of the storage account.

### Step 5: Test the Connection

Now here is my connection to the storage account through the firewall:

![SFTP Connection via Azure Firewall](/assets/img/posts/2025-10-20-image-3.png)

#### Key Points to Note

1. We are connecting to the IP address of the firewall, not the storage account directly.
2. We can allow only specific IP addresses to access the storage account via the firewall.
3. But we still use storage account username and password or SSH keys to authenticate.
4. As you can see, private endpoint DNS configuration is not that important here since we are dealing with network layer traffic.
5. If you want to use a custom domain, you would need to add a record under that domain to point to the firewall public IP address.

---

## Conclusion

In conclusion, using Azure Firewall to secure an SFTP-enabled Storage Account provides an additional layer of security and control over the traffic accessing the FTP service. This architecture allows you to:

- Centralize the entry point for your traffic
- Enforce security policies effectively
- Gain better visibility and monitoring capabilities
- Implement advanced threat protection

While this approach is more complex and expensive than using Storage Account firewall rules alone, it provides significantly enhanced security features that may be required for enterprise or compliance-driven scenarios.

Choose the architecture that best fits your requirements, budget, and security needs. For simple use cases, the Storage Account firewall approach may suffice, but for enhanced security and control, the Azure Firewall solution is recommended.