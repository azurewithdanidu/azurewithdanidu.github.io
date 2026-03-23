---
title: "Running Containers with Interactive Terminal Sessions in Azure"
date: 2025-07-18 10:00:00 +1000
categories: [Azure, Compute]
tags: [azure, batch, bicep, compute, infrastructure]
description: "Run containerized workloads on Azure Batch — from Docker images in ACR to job execution via a custom Flask web app, all backed by Bicep IaC."
author: danidu
toc: true
comments: true
pin: false
mermaid: false
math: false
image:
  path: https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image.png
  alt: "Running Containers with Interactive Terminal Sessions in Azure"
---

> This blog is backed by GitHub Sample code: <https://github.com/azurewithdanidu/docker-with-azure-batch/tree/main>
{: .prompt-info }

Howdy Folks,

When we think about running containers in Azure, the usual suspects come to mind: AKS, Container Apps, or App Services — all great choices for long-running services like APIs, background workers, or microservices. But not all container workloads fall into that category.

What if your container is:

- Meant to run once and exit?
- Designed for batch processing, not serving traffic?
- Built to process files, run tests, or perform compute-heavy parallel tasks?

These short-lived, often stateless containers don't need to be "always-on" or part of a service mesh. They just need compute — on-demand, scalable, and efficient.

Services like AKS or Container Apps aren't a natural fit for these use cases. Have you ever wondered what you can do in this situation in Azure?

When most people think about containers, they picture a backend service or API running inside a container — always on, listening on port 80, scaling with load. And yes, those use cases are absolutely valid — in fact, they dominate modern container platforms like Kubernetes and Azure Container Apps.

But what's often overlooked is that containers can be used like powerful, portable CLI tools.

Some scenarios like:

### PyTorch Docker Container

**PyTorch**, a leading machine learning framework, also has an official Docker image that allows you to run models using PyTorch's dynamic computation graph.

- Docker Hub: `pytorch/pytorch`
- Command: `docker run -it pytorch/pytorch bash`
- Description: This image comes with all necessary PyTorch libraries, and you can use it to train and deploy models in your own environment.

### Jupyter Notebooks with AI Libraries

Jupyter notebooks are an essential tool for data scientists and AI practitioners. You can find pre-built Docker containers that come with Jupyter and many machine learning libraries like TensorFlow, PyTorch, Scikit-learn, and others.

- Docker Hub: `jupyter/tensorflow-notebook`
- Command: `docker run -p 8888:8888 jupyter/tensorflow-notebook`
- Description: This container includes Jupyter Notebook with TensorFlow pre-installed. It's great for experimenting with AI models interactively in a notebook environment.

So, having said that — what is one of the best solutions in Azure?

**Azure Batch** is a cloud-based service that allows you to run large-scale parallel and high-performance computing tasks. It automatically handles job scheduling, resource provisioning, and scaling, making it ideal for scenarios like data processing, image analysis, and AI model training. Azure Batch supports containerized workloads, offering a flexible and cost-effective solution for batch processing in the cloud.

Here is more about Azure Batch — [https://learn.microsoft.com/en-us/azure/batch/batch-technical-overview](https://learn.microsoft.com/en-us/azure/batch/batch-technical-overview)

---

## Solution

So, what is the solution overview?

![Solution Overview](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image.png)

I have a Docker image, which I will be publishing to my **Azure Container Registry**. **Azure Batch** will simply pull the image from ACR and run it as a Docker container when it gets a request from my front-end web app.

What happens inside Azure Batch is as follows:

1. You need to create an **Azure Batch Account**
2. You need to create a **compute pool** within the Azure Batch account where you get multiple options, including running those compute pools inside your network, running as Docker images, etc.
3. You need to create a **job** inside the compute pool
4. You need to create a **task** inside the job with commands or tasks that you need to execute against your Docker container

And one thing I realized is — you **cannot** create Jobs or Tasks from IaC. You have to use either the Graph API or Azure SDK to create them once you have the pool configured.

---

### Resource Group Overview

Here is what I ended up with in my resource group:

![Resource Group](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-1.png)

---

### Azure Batch Pool Configuration

Here is the configuration inside the Azure Batch pool:

![Batch Pool Configuration](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-2.png)

I have a **user-assigned managed identity** that is assigned to the pool that has permission to pull container images from the ACR.

---

### Creating a Pool — Step by Step

Here are the steps to create a pool manually:

Go to **Pool** and click **Create** and select the options as per below. It's important to select the highlighted option as we need a VM image that has Docker already configured — this is the only image that's available with the required configuration as of this moment.

> Make sure to select the **user-assigned managed identity** when creating the pool. This is how the pool nodes authenticate to ACR to pull your container images.
{: .prompt-warning }

![Pool Creation — VM Image and Managed Identity](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-4.png)

Next step is selecting the container image and the container registry. When specifying the container name, make sure to have the **full name including the ACR domain name** as shown below.

Also, when selecting the container registry **DO NOT USE** the username/password option — simply select the **managed identity** and type the ACR login server name.

![Container Registry Configuration](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-5.png)

Next is to select the **VM SKU** and the **dedicated VM count**. You can keep the other settings as default, but if you want to change them you can configure however you want.

> The `microsoft-dsvm` publisher with `ubuntu-hpc` offer (SKU `2204`) comes pre-installed with a Docker-compatible Moby container runtime. This is the recommended image for container workloads on Azure Batch. See: [Supported VM images](https://learn.microsoft.com/en-us/azure/batch/batch-docker-container-workloads#supported-vm-images)
{: .prompt-tip }

---

### IaC with Bicep

While the portal walkthrough above is useful for understanding, in production you want all of this deployed via **Infrastructure as Code**. I've created Bicep templates that deploy the Batch account and pool with container configuration.

Here's the key part of the Bicep deployment — the container configuration in the pool:

```bicep
containerConfiguration: {
  type: 'DockerCompatible'
  containerImageNames: containerImageNames
  containerRegistries: [
    {
      registryServer: containerRegistryServer
      identityReference: {
        resourceId: managedIdentityResourceId
      }
    }
  ]
}
```

This does three important things:

1. **Sets the container runtime to `DockerCompatible`** — enables the Docker-compatible runtime on pool nodes.
2. **Prefetches container images** — images are pulled to each node when the pool is created, not when tasks start. This eliminates startup delays.
3. **Authenticates to ACR via managed identity** — using `identityReference` instead of username/password. No secrets to rotate.

To deploy:

```bash
# Clone the repository
git clone https://github.com/azurewithdanidu/docker-with-azure-batch.git
cd docker-with-azure-batch

# Deploy the infrastructure
az deployment group create \
  --resource-group your-resource-group \
  --template-file bicep/ml-batch/main.bicep \
  --parameters \
    location=eastus \
    batchAccountName=your-batch-account \
    managedIdentityResourceId="/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity-name>" \
    containerRegistryServer=your-registry.azurecr.io
```

> Make sure the user-assigned managed identity has the **Batch Contributor** role on the Batch account and the **AcrPull** role on your Azure Container Registry before deploying.
{: .prompt-warning }

---

### The Front-End Web App

The next step is to create the **Job** and **Task** to execute. We can do it in the GUI, but instead, I wrote a small Python web app to interact with Azure Batch using its access key so I can execute commands from a web layer.

![Flask Web App — Job and Task Management](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-7.png)

The idea is I create the job from the web portal and also submit tasks. As you can see, the Task form requests 4 basic inputs:

1. **Job ID** — to run this task under
2. **Task Name** — a unique identifier for the task
3. **Container Image name** — to execute the command against. Don't get confused — the reason we selected the container details in the Pool is to **cache the container image** so that we can execute things faster
4. **Command to execute** — the actual command to run inside the container

> Note: In the screenshots I'm not executing proper commands for the container I'm using, hence getting execution failures :P
{: .prompt-info }

![Task Submission Form](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-8.png)

Here's how the task creation works in code:

```python
def create_task(batch_client, job_id, task_id, command, image_name):
    """Create a container task."""
    task_container_settings = batchmodels.TaskContainerSettings(
        image_name=image_name,
        working_directory="taskWorkingDirectory"
    )

    user_identity = batchmodels.UserIdentity(
        auto_user=batchmodels.AutoUserSpecification(
            scope="pool",
            elevation_level="nonadmin"
        )
    )

    constraints = batchmodels.TaskConstraints(
        retention_time=datetime.timedelta(days=7),
        max_wall_clock_time=datetime.timedelta(hours=72),
        max_task_retry_count=0
    )

    task = batchmodels.TaskAddParameter(
        id=task_id,
        command_line=command,
        container_settings=task_container_settings,
        user_identity=user_identity,
        constraints=constraints
    )

    return batch_client.task.add(job_id=job_id, task=task)
```

> When Batch creates a container task, it uses `docker create` under the hood. The `command_line` you specify becomes the `CMD` for the container, while the image's `ENTRYPOINT` remains unchanged. See: [Container task command line](https://learn.microsoft.com/en-us/azure/batch/batch-docker-container-workloads#container-task-command-line)
{: .prompt-tip }

---

### Seeing It All Come Together

Azure Batch makes it easy to run large-scale parallel and high-performance computing jobs in the cloud. In this example:

1. Created a pool of compute nodes
2. Submitted a new task (`task3`) using a containerized image
3. Observed its state update in the Azure portal — going from active to completed

Perfect for automating batch jobs like ML inference or image processing!

![Task Execution — State Updates in Azure Portal](https://hungryboysl.wordpress.com/wp-content/uploads/2025/07/image-9.png)

---

### Conclusion

When you have short-lived, compute-heavy container workloads that don't need to be "always-on," **Azure Batch** is an ideal solution. It offers a powerful and scalable way to run containerized jobs — from model training and data processing to automated testing — without the overhead of managing container orchestration platforms like AKS or Container Apps.

In my solution, I leveraged Azure Batch to pull Docker images from Azure Container Registry and run tasks on demand via a custom front-end web app. While infrastructure like pools and identities can be provisioned using IaC tools, job and task creation is best handled dynamically via SDKs or the Batch API — just as I've done using Python.

👉 I've published all the IaC templates and the front-end web app code in my GitHub repo if you'd like to try it out yourself:

**[https://github.com/azurewithdanidu/docker-with-azure-batch](https://github.com/azurewithdanidu/docker-with-azure-batch)**

Hope this will help someone in need :) Feel free to reach out if you have any questions!

Until next time...!

---

## References

- [What is Azure Batch? — Microsoft Learn](https://learn.microsoft.com/en-us/azure/batch/batch-technical-overview)
- [Run container workloads on Azure Batch — Microsoft Learn](https://learn.microsoft.com/en-us/azure/batch/batch-docker-container-workloads)
- [Supported VM images for Azure Batch containers — Microsoft Learn](https://learn.microsoft.com/en-us/azure/batch/batch-docker-container-workloads#supported-vm-images)
- [Azure Batch documentation — Microsoft Learn](https://learn.microsoft.com/en-us/azure/batch/)
- [Azure Bicep documentation — Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/)
- [Azure Container Registry documentation — Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-registry/)
- [Full source code — GitHub](https://github.com/azurewithdanidu/docker-with-azure-batch)
