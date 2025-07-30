---
title: "Unlocking Azure Arc: Benefits for Hybrid Data Centers – Part 2"
date: 2024-09-24
categories: 
  - "azure"
  - "azure-arc"
tags: 
  - "azure-devops"
  - "azurearc"
  - "infrastructure"
---

Howdy Folks.

In this post we are going to look at how to perform management operations on Azure ARC onboarded server. There are various amounts of new options available for Azure ARC. If you are devops person, you could do all of these things using Bicep templates and Pipelines. The only manual thing would be to onboard the server to Azure ARC

### Azure ARC | Site Manager

Azure Arc Site Manager provides a powerful way to manage and monitor your on-premises environments by treating them as Azure Arc sites. These Arc sites are integrated with Azure resource groups or subscriptions, giving you a unified view to track connectivity, receive alerts, and apply updates across your infrastructure. Azure site manager is FREE to use. You can group the servers into different sites and manage them based on the location.

There are couple of methods that on-prem or other cloud servers can interact with the Azure ARC management interface.

1. Over the Public Internet

3. Private Link Connections

In this blog, my on-prem server is connect to Azure ARC via public internet. As you can see my server is connected but, I haven't turned on Application insights or policies neither windows update settings

[![](images/image-3.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-3.png)

### Windows Updates

To enable windows updates or check windows updates we would need to select "updates" option in the left hand menu

[![](images/image-4.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-4.png)

Interface is much more similar to a normal Azure Virtual Machine update.

[![](images/image-5.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-5.png)

If you wanted to check updated once you can select the option 1 or if you want to turn on periodic updates you can select the option 2. In this case I would want to enable periodic assessments. So, I would select option 1 and turn on periodic assessments

[![](images/image-6.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-6.png)

And once you kick start a search you, will be able to see if there any missing patches etc..

You could also manage the windows updates for ARC servers using Azure Update manager, which also provide a centralized dashboard across all your servers

[![](images/image-9.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-9.png)

You could also create an update schedule in Azure Update Manager for ARC and all of your other server, wherever they are, this will provide valuable insights, so that you won't need to maintain 2 different processes for Azure and On-prem.

[![](images/image-10.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/09/image-10.png)

### Conclusion

Azure Arc makes it easier than ever to manage and monitor your on-premises and multi-cloud environments alongside your native Azure resources. With tools like Azure Arc Site Manager and Azure Update Manager, you can streamline server management, automate updates, and centralize operations, whether your infrastructure is in the cloud or on-premises. By integrating these tools into your DevOps workflows using Bicep templates and pipelines, you can further enhance automation and efficiency. Azure Arc gives you the flexibility to manage your hybrid environment with the power of Azure, all from a single control plane. REMEMBER ALL THIS ONLY for under 10 dollars per server.

Watch out for the ARC related bicep repository.....
