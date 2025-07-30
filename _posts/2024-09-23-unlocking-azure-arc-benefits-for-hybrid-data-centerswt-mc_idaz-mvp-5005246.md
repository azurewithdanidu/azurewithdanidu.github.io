---
title: "Unlocking Azure Arc: Benefits for Hybrid Data Centers - Part 1"
date: 2024-09-23
categories: 
  - "azure"
tags: 
  - "azurevm"
---

Azure ARC caught me because of all the new features and price point value its gives. This topic is more suitable for folks who has hybrid data centers like onprem-azure, aws-azure etc.

Seems to be Azure Arc is silent beast. With Azure ARC I do see few key benefits for all the on Prem server

- Defender for Endpoint

- Azure Update Manager

- Remote Management

- Compliance Policies and Goverance

- Centralized monitoring

You can simply get 1st 3 features just for **30AUD per month a server.** Honestly, I believe it's a real bargain compared to other virus guard solution and similar. Again, this would be ideal for hybrid customers.

In this article we are going look at some of the settings in 10000 feet high level and try to get an entry to this particular topic.

According to Microsoft.....

Azure Arc provides a centralized, unified way to:

- Manage your entire environment together by projecting your existing non-Azure and/or on-premises resources into Azure Resource Manager.

- Manage virtual machines, Kubernetes clusters, and databases as if they are running in Azure.

- Use familiar Azure services and management capabilities, regardless of where your resources live.

- Continue using traditional ITOps while introducing DevOps practices to support new cloud native patterns in your environment.

- Configure custom locations as an abstraction layer on top of Azure Arc-enabled Kubernetes clusters and cluster extensions.

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image.png)

There are bunch of different options and value additions, but there are few key things which caught my eye and most of them are free of charge

They are...

- **Inventory** - Tag your resources, organize them into resource groups, subscriptions, and management groups, and query at scale with Azure Resource Graph to unify your environments.

- **Manage** - Administrate your servers anywhere using SSH Arc, Windows Admin Center (WAC), and Custom Script Extension.

- **Automate** - With Azure Auto manage Machine Best Practices, easily onboard and configure Azure services across security, monitoring, and governance.

- **Update -** Manage windows updates for on Prem workloads **(NOT FREE)**

The table below outlines each method to help you identify which one is most suitable for your deployment. For more detailed instructions, click the links to explore the steps for each topic.

| Method | Description |
| --- | --- |
| Manual | Manually install the agent |
| Manual | Connect machines using Windows Admin Center. |
| Manual | Use PowerShell to connect machines either individually or in bulk. |
| Bulk Installs | Using SCCM |
| Bulk Installs | Connect Windows machines using Group Policy. |
| Bulk Installs | Utilize Arc-enabled VMware vSphere |
| Bulk Installs | Install the Arc agent on SCVMM VMs |
| Bulk Installs | Connect your AWS environment through Azure Arc's multi cloud connector |

Microsoft has well documented the onboarding process in the below link  
[https://learn.microsoft.com/en-us/azure/azure-arc/servers/onboard-portal](https://learn.microsoft.com/en-us/azure/azure-arc/servers/onboard-portal)

Once you enable you will end with below

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-1.png)

For each server you onboard you will get all of the below options to manage the server

[![](images/image-2.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-2.png)

Out of these controls following options are free to use

1. Inventory

3. Change Tracking

5. Run Command

However Other options get charged based on the usage, especially windows updates. or Arc-enabled servers, it is charged at a daily prorated value which amounts to **$7.363/server/month** (assuming 31 days of connected usage).

[https://azure.microsoft.com/en-us/pricing/details/azure-arc/security-and-monitoring-services/](https://azure.microsoft.com/en-us/pricing/details/azure-arc/security-and-monitoring-services/)

On top of all these you can push Defender for endpoint using Azure ARC too, and again you will get charged separately for it

Extracted - [https://azure.microsoft.com/en-us/pricing/details/azure-arc/security-and-monitoring-services/](https://azure.microsoft.com/en-us/pricing/details/azure-arc/security-and-monitoring-services/)

| Services | Price | Notes |
| --- | --- | --- |
| Servers: Microsoft Defender for Cloud | $0.010/Server/hour for Plan 1   $0.030/Server/hour for Plan 2 | Free for the first 30 days, with 500MB/server included data.   [Pricing—Microsoft Defender \| Microsoft Azure](https://azure.microsoft.com/en-us/pricing/details/defender-for-cloud/). |
| SQL Server: Microsoft Defender for Cloud for Arc-enabled SQL Server | $0.030/Instance/hour | Microsoft Defender for SQL for non-Arc enabled, non-Azure instances costs $16.1243/vCore/month.   [Pricing—Microsoft Defender \| Microsoft Azure](https://azure.microsoft.com/en-us/pricing/details/defender-for-cloud/). |
| Azure Monitor: Basic Log Data Ingestion | $1.0676 per GB\* | 5 GB per billing account/month is included.   [Pricing - Azure Monitor \| Microsoft Azure](https://azure.microsoft.com/en-us/pricing/details/monitor/). |
| Azure Monitor: Analytics Log Data Ingestion | $4.919 per GB\* | 5 GB per billing account/month is included.   [Pricing - Azure Monitor \| Microsoft Azure](https://azure.microsoft.com/en-us/pricing/details/monitor/). |

In our next blog, let's look at how to use each of the above controls and benefits.

Until next time...!
