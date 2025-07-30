---
title: "Do you want to save on Log Analytics costs..?"
date: 2022-05-31
categories: 
  - "azure"
---

Howdy Folks

It's time to discuss Azure Monitor costs, As you all know Microsoft merge most of their logging service solutions under the Azure Monitor umbrella. And most of the services share a common log collection location for this service which is the Log Analytics workspace. The following diagram explains the services under each category.

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/05/image.png)

Next what we need to understand is how we get charged for Log analytics workspaces. So that we can work on reducing the costs.

As per the Microsoft documentation, we are getting charged based on

1. Data Retention
2. Data Ingestion

let's do a quick calculation and see how this going affecting our bill. Let's take an example scenario, let's assume we have a few Azure workloads that generate 2GB data every day and we are ingesting that to log analytics to retain for 90 days

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/05/image-1.png)

As per the above example, we can clearly see our charges will increase with **data ingestion** capacity but not much with the data retention.

## How to Find the Utilization?

Now that we need to know how much data you are ingesting per day and what sources are. It's somewhat easy to find out. you can simply run the following log query in the workspace

```
Usage
| project TimeGenerated, SourceSystem, DataType, Quantity
| summarize TotalGB = sum(Quantity) / 1024 by DataType
| sort by TotalGB desc
| render piechart
```

<figure>

[![](images/image-4.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/05/image-4.png)

<figcaption>

Log Analytics usage (piechart)

</figcaption>

</figure>

<figure>

[![](images/image-5.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/05/image-5.png)

<figcaption>

Log Analytics usage (table)

</figcaption>

</figure>

**Note - if you want to see the billable usage only please use the below query**

```
Usage| where IsBillable == true| project TimeGenerated, SourceSystem, DataType, Quantity| summarize TotalGB = sum(Quantity) / 1024 by DataType| sort by TotalGB desc| render piechart
```

## How to Save Cost?

So there are a few things that we could do to save the cost.

1. Consider moving to Commitment Tiers pricing model to the Log Analytics workspace.
2. Limit the daily ingestion for your workspace.
3. Consider using different logging options other than a workspace for noncritical logs (eg - blob storage)
4. Reduce the log retention

### Commitment Tiers

Other than the Pay-As-You-Go model, Log Analytics has Commitment Tiers, which can save around 30 percent compared to the Pay-As-You-Go price. We can commit to buying data ingestion for a workspace, starting at 100 GB/day, at a lower price than PAYG pricing. Any usage above the commitment level (overage) is billed at that same price per GB as provided by the current commitment tier.  
But I believe this should be the last option, after doing all the fine-tuning and monitoring for some of the log analytics usages. At least a couple of months

### Limit the daily ingestion for your workspace

One more way to reduce cost is to change the log level. You need to work with your teams and find out do you really need logs to be readily available in log analytics, for example, debug logs.  Usually the lower the log level, the higher the number of logs.

### Consider using different logging options

Just in the above section, we took debug logs as an example. you need these debug logs if there is something wrong. Nothing better than debugging logs when in an outage to troubleshoot and find out what is the problem. So now you must be thinking about what I can do to save money and keep these logs. That is when the other options come into the picture. Using low-cost storage as log destinations. You can point (required but not required all the time) logs to storage accounts. Archiving to storage accounts costs way less than log analytics workspace

[![](images/image-6.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/05/image-6.png)

###   
Reduce the log retention

The other thing that you could do is reduce the log retention time, You may have already known log retention for the first 31 days is free. But my honest opinion is unless you dump heaps of log data into log analytic, you won't get charged much for retention compared to the log ingestion.

## Conclusion

Long story short, saving cost again falls to your side :).If you can do the following you can reduce the cost you spend on log analytics workspaces and also you can have a valuable source of logs

1. Make sure you are logging in whats absolutely necessary
2. Move noncritical logs to low-cost storage
3. Periodically check the logs that you are ingesting into the log analytics

Until next time....... :D
