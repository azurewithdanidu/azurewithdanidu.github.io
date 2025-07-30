---
title: "Keep Your CV Up to Date with Azure Devops"
date: 2024-02-04
categories: 
  - "azure"
  - "azure-devops"
tags: 
  - "bicep"
  - "cloud"
  - "devops"
  - "terraform"
---

## Introduction

In an era where digital presence is not just an option but a necessity, showcasing one's professional journey online becomes paramount. This realization led me to embark on an exciting project: hosting my Curriculum Vitae (CV) as a dynamic website. The goal was not just to digitize my CV but to create a platform that reflects my technical skills and professional accomplishments in a more interactive and accessible format. To bring this vision to life, I turned to Azure App Services and Azure DevOps, leveraging the robust `startbootstrap-resume` NPM package as my foundation.

The `startbootstrap-resume` package offered a sleek, modern, and fully customizable template, ideal for presenting a professional CV. Its responsive design ensured that my website would be accessible across various devices, from desktops to smartphones, providing a seamless user experience. However, the journey from a static CV to a dynamic website required a reliable, scalable, and efficient tech stack. This is where Azure's ecosystem came into play.

## Why Azure?

### Choice of Azure App Services and Azure DevOps

My choice of Azure App Services and Azure DevOps was driven by the desire for a seamless, integrated development and deployment experience. Azure App Services promised a hassle-free hosting environment with a focus on high availability, security, and scalability. It offered a straightforward path to deploy web applications without getting bogged down in infrastructure management. On the other hand, Azure DevOps served as the backbone for automating the CI/CD pipeline, ensuring that every update to my CV could be seamlessly integrated and deployed with minimal manual intervention.

Azure DevOps, with its comprehensive suite of development tools, provided a unified platform for project management, version control, and automated deployments. The synergy between Azure App Services and Azure DevOps meant that I could focus more on enhancing my CV's content and less on the operational aspects of web hosting and maintenance.

### Benefits of Azure for Personal Projects

Azure's ecosystem offers a plethora of advantages for personal projects, especially for those looking to demonstrate their technical prowess through practical applications. Here are a few key benefits that stood out to me:

- **Scalability**: Azure App Services easily scales to accommodate traffic spikes, ensuring that my website remains available and responsive, irrespective of the number of visitors.

- **Security**: Azure provides built-in security features, safeguarding my website against common vulnerabilities and threats, thus protecting my professional information.

- **Continuous Integration and Continuous Deployment (CI/CD)**: Azure DevOps automates the build and deployment process, significantly reducing the turnaround time for updating my website. This automation not only streamlines workflows but also ensures that my online CV is always up-to-date.

- **Cost-Effectiveness**: With Azure's pay-as-you-go pricing model, I could control my project's costs without compromising on performance or availability. This aspect is particularly appealing for personal projects where budget constraints are a consideration.

### Azure App Service Configuration

The deployment of the App Service was orchestrated through a Bicep file, which described the service's properties, such as the runtime stack and region. This approach not only streamlined the setup process but also ensured that the infrastructure could be replicated or updated with minimal effort. The integration with Azure DevOps further automated the deployment, bringing my CV website to life with each commit.

### Azure DevOps and CI/CD Integration

Azure DevOps played a pivotal role in automating the build and deployment pipeline. By connecting the repository with Azure DevOps and utilizing Bicep templates within the CI/CD pipeline, changes to the infrastructure and application were automatically applied. This setup minimized manual tasks and facilitated a smooth, continuous delivery process.

I created the following pipeline to deploy the app service using Azure Bicep and Deploy the app code as a package to my web app.,

```
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- checkout: self

- task: AzureCLI@2
    name: LintSubscriptionBuild
    displayName: 'Run preflight validation' 
    inputs: 
      azureSubscription: ${{ variables.azureServiceConnection }}
      scriptType: 'pscore'  
      scriptLocation: 'inlineScript'  
      inlineScript: |
        az account set --subscription 'SUBID'
        az deployment sub what-if --location ${{ variables.location }} `
        --template-file bicep/main/cv-webapp.main.bicep `
        --parameters bicep/main/cv-webapp.main.bicepparam

- task: UseNode@1
  inputs:
    version: '16.x'
  displayName: 'Install Node.js'

- script: |
    ls
    npm install --cache /tmp/empty-cache
  displayName: 'npm install'

- script: |
    npm run build
  displayName: 'npm build'
  workingDirectory: '$(Build.SourcesDirectory)'

- task: ArchiveFiles@2
  inputs:
    rootFolderOrFile: '$(System.DefaultWorkingDirectory)/dist'
    includeRootFolder: false
    archiveType: 'zip'
    archiveFile: '$(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip'
    replaceExistingArchive: true

- task: PublishPipelineArtifact@1
  inputs:
    artifactName: cv
    targetPath: '$(Build.ArtifactStagingDirectory)'
    publishLocation: 'pipeline'
  displayName: 'Publish npm artifact'

- task: DownloadPipelineArtifact@2
  inputs:
    source: 'current'
    artifactName: cv
    targetPath: $(Build.SourcesDirectory)
    
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'azure-mvp-subscription'
    appType: 'webAppLinux'
    appName: 'danidu-resume-cv-web'
    resourceGroupName: 'danidu-resume-cv-rg'
    package: $(Build.SourcesDirectory)/**/*.zip
```

## How to Use My Repository

Leveraging my repository for your project is straightforward. Here’s a simple guide to get you started:

### Clone My Repository

[https://github.com/DaniduWeerasinghe911/azure-danidu-resume?WT.mc\_id=AZ-MVP-5005246](https://github.com/DaniduWeerasinghe911/azure-danidu-resume?WT.mc_id=AZ-MVP-5005246)

Begin by cloning the repository to your local machine. This step brings all the necessary files and configurations into your development environment.

### Update Your Information

Navigate to the specified configuration file within the repository. Here, you will update it with your personal and professional details to customize the CV to your profile.

/src/pug/index.pug

### Update Your Photo

Replace the default photo with your own in the specified folder. Ensure you use the same filename to maintain consistency and avoid broken links.

/src/assets/profile.jpg

### Import the Pipeline into Azure DevOps and Run the Pipeline

Finally, import the CI/CD pipeline configuration into Azure DevOps. This configuration is designed to automate the deployment process. Once imported, run the pipeline to deploy your customized CV website to Azure App Service seamlessly.

Hope you enjoy this fun little project. I will be adding few more things in to the pipeline in the coming weeks like

- DNS Updates

- Custom Domains

- Etc....

Until next time...!

My Repo  
[https://github.com/DaniduWeerasinghe911/azure-danidu-resume?WT.mc\_id=AZ-MVP-5005246](https://github.com/DaniduWeerasinghe911/azure-danidu-resume?WT.mc_id=AZ-MVP-5005246)

You can find the original bootstrap code in the below link.

[https://www.npmjs.com/package/startbootstrap-resume](https://www.npmjs.com/package/startbootstrap-resume)
