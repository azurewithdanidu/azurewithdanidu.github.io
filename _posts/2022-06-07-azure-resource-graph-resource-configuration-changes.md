---
title: "Azure Resource Graph - Resource Configuration Changes"
date: 2022-06-07
categories: 
  - "azure"
---

It is an Azure service designed to extend Azure Resource Management capabilities. The following can be achieved using this service

- Query resources with complex filtering, grouping, and sorting by resource properties.
- Explore resources iteratively based on governance requirements.
- Assess the impact of applying policies in a vast cloud environment.
- Query changes made to resource properties (preview).

Apart from all the others, today’s focus is on monitoring resource configuration changes using Azure Resource Graph explorer

The latest release resource configuration changes enable queries across your subscriptions and tenant to discover changes to resources with Azure Resource Graph.

You can,

- Find when changes were detected on an Azure Resource Manager property
- See property change details for each resource change
- Query changes at scale across your subscriptions, management group, or tenant
- Audit, troubleshoot, and govern your resource changes at scale
- By using Azure Resource Graph to query your resource changes, you can craft charts and pin results to Azure dashboards based on specific change queries.

Few things to note –

- This feature is already enabled by default in all the tenants
- Retention for the data is set to 14days by Microsoft

Let’s look at some of the examples

You can run the resource graph queries in

- Azure PowerShell
- Azure CLI
- Azure portal

**Using Azure portal**

**Login to Azure Portal and Search for Azure Resource Graph explorer**

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/06/image.png)

**Once you select the Resource Graph Explorer, you will be presented with bunch of sample queries, similar to a log analytics workspace.**

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/06/image-1.png)

**For us to see the resource changes I’m going to run the below query**

```
resourcechanges 
| extend changeTime=todatetime(properties.changeAttributes.timestamp) 
| project changeTime, properties.changeType, properties.targetResourceId, properties.targetResourceType, properties.changes 
| order by changeTime desc
```

**And I’m going to get all the changes that happened during the past 14 days. We can go into detail and understand what these changes and target resource details were**

[![](images/image-2.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/06/image-2.png)

[![](images/image-3.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/06/image-3.png)

**These details are helpful in terms of governance and audit perspective.** Each change details include below information

- targetResourceId - The resourceID of the resource on which the change occurred.
- targetResourceType - The resource type of the resource on which the change occurred.
- changeType - Describes the type of change detected for the entire change record.
- changes - Dictionary of the resource properties (with property name as the key) that were updated as part of the change
- changeAttributes - Array of metadata related to the change

You can run the same query by using

**Azure Powershell**

```
Search-AzGraph -Query 'resourcechanges | extend changeTime=todatetime(properties.changeAttributes.timestamp) | project changeTime, properties.changeType, properties.targetResourceId, properties.targetResourceType, properties.changes | order by changeTime desc'
```

Azure CLI

```
az graph query -q 'resourcechanges | extend changeTime=todatetime(properties.changeAttributes.timestamp) | project changeTime, properties.changeType, properties.targetResourceId, properties.targetResourceType, properties.changes | order by changeTime desc
```

Also, apart from the governance and audit perspective, there are a bunch of other use cases for this free Microsoft service. Like

1. Resource Count
2. Resource dependencies
3. Resource search based on parameters
4. Etc..

Below are some other sample queries that you can use

**_All the deleted resources over the past 7 days_**

```
resourcechanges
| extend changeTime = todatetime(properties.changeAttributes.timestamp), targetResourceId = tostring(properties.targetResourceId),
changeType = tostring(properties.changeType), correlationId = properties.changeAttributes.correlationId
| where changeType == "Delete"
| order by changeTime desc
| project changeTime, resourceGroup, targetResourceId, changeType, correlationId
```

**_All the deleted resources over the past 7 days in a particular resource group_**

```
resourcechanges| where resourceGroup == "ResourceGroup"| extend changeTime = todatetime(properties.changeAttributes.timestamp), targetResourceId = tostring(properties.targetResourceId),changeType = tostring(properties.changeType), correlationId = properties.changeAttributes.correlationId| where changeType == "Delete"| order by changeTime desc| project changeTime, resourceGroup, targetResourceId, changeType, correlationId
```

**You can learn more about**

[Azure Resource Graph documentation | Microsoft Docs](https://docs.microsoft.com/en-us/azure/governance/resource-graph/)

Until next time... :)
