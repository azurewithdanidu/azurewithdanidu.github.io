---
title: "Save Cost with Azure Bicep Deployment Stacks ?"
date: 2025-02-02
categories: 
  - "azure"
  - "azure-devops"
  - "github-actions"
tags: 
  - "costoptimization"
  - "deploymentstacks"
  - "bicep"
  - "cloud"
  - "devops"
  - "github"
  - "infrastructure"
  - "microsoft"
---

Howdy Folks,

This time I'm here to talk about how to save cost using Azure Deployment Stacks. Assume everyone has a pretty good understanding about deployment stacks, let's see how we can use if for our advantage. To talk about it, I'm going to use a scenario. I believe it's the best way to explain and simulate the situation

Scenario

In our azure environment we have few virtual machines, and we use azure bastion to access the VMs, but our work only between 8am to 5pm. So, there is no point running Azure bastion 24/7 rather we save some money.

Here is the plan of attack

1. Bicep template to deploy Azure bastion

3. Have a variable to deploy bastion or not in the template

5. Create a scheduled devops pipeline and change the variable accordingly

Following is my bicep template, its a simple file just to show the process. there may be lot of hard coded values.

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/02/image.png)

important variable here is deployResource Bool value

Here is my pipeline files

I create 2 files to run on 2 schedules. one at morning 6am

**_<note: in this pipeline my deploy resources parameter is set to true, as i wanted to get bastion deployed in the morning>_**

[![](images/image-4.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/02/image-4.png)

and second one at 6pm

**_<note: in this pipeline my deploy resources parameter is set to false, as i wanted to delete bastion in the afternoon>_**

Based on how deployment stack works following is the output at

#### 6am everyday

[![](images/image-6.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/02/image-6.png)

#### 6pm everyday

[![](images/image-5.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/02/image-5.png)

You can use this methodology to many scenarios

1. If you have dev environments and if wanna save more cost

3. Unwanted resources during office hours like Azure bastions etc. ( Which gonna get charged once get provisioned)

And you might think why not use the same pipeline, I have few reasons behind it

1. Wanted differentiate runs easily

3. We have more flexibility when running things or scheuduling things

5. Keep things simple  
    

And definitely there is no problem using the same pipeline and achieve the same thing.

Also in the pipeline you can improve it by using pipeline templates and use variables intead of parameters etc.

### Conclusion

I wanted to show the power behind using Azure IAC, Deployment stacks and Pipelines, anyone who is leveraging these practices can manage you Azure cloud environment effectively and cost efficiently. Above example shows saving azure bastion cost by a half. So depending on your scenario and use case you can save more money without need to thing about reservations etc.

Btw You can get the solution sample using the below github link

[https://github.com/DaniduWeerasinghe911/deployment-stack-cost-saving?WT.mc\_id=AZ-MVP-5005246](https://github.com/DaniduWeerasinghe911/deployment-stack-cost-saving?WT.mc_id=AZ-MVP-5005246)

Until next time..... :)
