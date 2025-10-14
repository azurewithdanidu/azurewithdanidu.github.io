---
title: "Running Containers with an Interactive Terminal Sessions in Azure"
date: 2025-07-17
categories: 
  - "azure"
  - "azure-devops"
tags: 
  - "batch"
  - "bicep"
  - "compute"
  - "infrastructure"
---

> NOTE: This blog iHub Sample code
> 
> [https://github.com/azurewithdanidu/docker-with-azure-batch/tree/main](https://github.com/azurewithdanidu/docker-with-azure-batch/tree/main)

Howdy Folks

When we think about running containers in Azure, the usual suspects come to mind: **AKS**, **Container Apps**, or **App Services** — all great choices for **long-running services** like APIs, background workers, or microservices. But not all container workloads fall into that category.

What if your container is:

- Meant to **run once and exit**?

- Designed for **batch processing**, not serving traffic?

- Built to **process files**, **run tests**, or perform **compute-heavy parallel tasks**?

These **short-lived**, often **stateless** containers don’t need to be "always-on" or part of a service mesh. They just need compute — on-demand, scalable, and efficient.

Services like AKS or Container Apps aren’t a natural fit for these use cases.  
**Have you ever wondered what you can do in this situation in Azure?**

When most people think about containers, they picture a backend service or API running inside a container — always on, listening on port 80, scaling with load. And yes, those use cases are absolutely valid — in fact, they dominate modern container platforms like Kubernetes and Azure Container Apps.

But what’s often overlooked is that **containers can be used like powerful, portable CLI tools**.

Some Scenarios like,

**PyTorch Docker Container**

PyTorch, leading machine learning framework, also has an official Docker image that allows you to run models using PyTorch’s dynamic computation graph.

- **Docker Hub**: pytorch/pytorch

- **Command**: bashCopyEdit`docker run -it pytorch/pytorch bash`

- **Description**: This image comes with all necessary PyTorch libraries, and you can use it to train and deploy models in your own environment.

**Jupyter Notebooks with AI Libraries**

Jupyter notebooks are an essential tool for data scientists and AI practitioners. You can find pre-built Docker containers that come with Jupyter and many machine learning libraries like TensorFlow, PyTorch, Scikit-learn, and others.

- **Docker Hub**: jupyter/tensorflow-notebook

- **Command**: bashCopyEdit`docker run -p 8888:8888 jupyter/tensorflow-notebook`

- **Description**: This container includes Jupyter Notebook with TensorFlow pre-installed. It's great for experimenting with AI models interactively in a notebook environment.

So, having said that what is the one of the best solutions in Azure?

**Azure Batch** is a cloud-based service that allows you to run large-scale parallel and high-performance computing tasks. It automatically handles job scheduling, resource provisioning, and scaling, making it ideal for scenarios like **data processing**, **image analysis**, and **AI model training**. Azure Batch supports containerized workloads, offering a flexible and cost-effective solution for batch processing in the cloud.

here is more about Azure batch - [https://learn.microsoft.com/en-us/azure/batch/batch-technical-overview](https://learn.microsoft.com/en-us/azure/batch/batch-technical-overview)

## Solution

So, what is the solution overview

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image.png)

So I have a docker image, which I will be publishing to my Azure Container Registry. Azure Batch will simply Pulls the image from ACR and run as docker image when it gets a request from my Front-end web App

What happens inside Azure Batch is as follows

1. You need to Create Azure Batch Account

3. You need to create a compute pool within Azure batch account where you get multiple options, including running those compute pool inside your network, run as docker images etc.

5. You need to create job inside the compute pool

7. You need to create a task inside the job with commands or tasks that you need to execute against our docker container.

And one this I realize is you cannot create Jobs or Tasks from IAC, you have to use either the Graph or Azure SDK to create them once we have the pool configured

Here is what I ended up with in my resource group

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-1.png)

Here is the configuration inside the Azure Batch pool configuration

[![](images/image-2.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-2.png)

I have a user assigned managed identity that is assigned to the pool that has permission to pull container image from the ACR

here are the steps to create a pool manually

Go to Pool and click create and select the options as per below, important to select the highlighted as we need an VM image that has docker already configured, this is the only image that's available that has the required configuration as of this moment that I am writing this.

Also make sure to select the user assigned managed identity

[![](images/image-4.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-4.png)

Next step is selecting the image and the container registry. when doing the container name make sure have the full name including the acr domain name as I typed below.

Also, when selecting the container registry DO NOT USE the username password option simply selects the managed identity and type the acr login server name

[![](images/image-5.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-5.png)

next is to select the VM sku and the dedicated VM, you can keep the other as default, but if you wanna change it you can select them as however you want it.

Next Step is to create the JOB and Task to execute, we can do it in GUI but instead, I wrote a small python web app to Interact with Azure Batch using its access key so I can execute commands from a web layer

[![](images/image-7.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-7.png)

Idea is I create the job from the web portal and also submit tasks. As you can see Task is requesting the 4 basic inputs,

1. Job Id to run this task

3. Task Name

5. Container Image name to make execute the command, don't get confused reason we selected the container details in the Pool is the cache the container image so that we can execute things faster

7. And the command to execute (Note - I'm not executing proper commands for the container that I'm using hence getting execution failures :P)

[![](images/image-8.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-8.png)

Azure Batch makes it easy to run large-scale parallel and high-performance computing jobs in the cloud.  
In this example

1. Created a pool of compute nodes.

3. Submitted a new task (`task3`) using a containerized image.

5. Observed its state update in the Azure portal — going from active to completed.

Perfect for automating batch jobs like ML inference or image processing!

[![](images/image-9.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-9.png)

### Conclusion

When you have short-lived, compute-heavy container workloads that don’t need to be "always-on," **Azure Batch** is an ideal solution. It offers a powerful and scalable way to run containerized jobs — from model training and data processing to automated testing — without the overhead of managing container orchestration platforms like AKS or Container Apps.

In my solution, I leveraged Azure Batch to pull Docker images from Azure Container Registry and run tasks on demand via a custom front-end web app. While infrastructure like pools and identities can be provisioned using IaC tools, job and task creation is best handled dynamically via SDKs or the Batch API — just as I’ve done using Python.

👉 I’ve published all the **IaC templates** and the **front-end web app code** in my GitHub repo if you’d like to try it out yourself.

[https://github.com/azurewithdanidu/docker-with-azure-batch/tree/main](https://github.com/azurewithdanidu/docker-with-azure-batch/tree/main)
