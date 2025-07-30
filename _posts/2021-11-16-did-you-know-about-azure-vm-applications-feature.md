---
title: "Did you know about Azure VM Applications feature?"
date: 2021-11-16
categories: 
  - "azure"
tags: 
  - "azure-compute-gallery"
  - "azurevm"
  - "azurevmapplication"
  - "sharedimagegallary"
---

## What is VM Applications

Azure Compute Gallery now includes the existing Shared Image Gallery (SIG) service and the new VM Applications features and additional capabilities. 

With VM Applications, you can now define application packages, replicate, share and deploy them automatically to your VMs and Virtual Machine Scale Sets using ARM templates, the portal, CLI, or PowerShell. Add an application to a VM or VMSS at creation, or add, remove, and update applications on existing resources.

This feature provides flexibility and simplicity in managing, sharing, and deploying applications. Some features include:

- Provides custom configuration of applications at deployment time
- Require applications or specific versions through DeployIfNotExist policies
- Create multiple replicas per region for reliability
- Limit which VMs and VM scale sets can install an application

And this does not charge you anything extra for the service. Its only charge you for the storage. Even though this is sounds interesting for you, keep in mind this feature a is still in preview and not production ready yet. Also, there are heaps of other limitations. I’m pretty sure MS Engineering team will come back with solutions in future for sure

**_Some limitations_**

- No more than 3 replicas per region: When creating a VM Application version, the maximum number of replicas per region is three.
- Retrying failed installations: Currently, the only way to retry a failed installation is to remove the application from the profile, then add it back.
- Only 5 applications per VM: No more than 5 applications may be deployed to a VM at any point.
- 1GB application size: The maximum file size of an application version is 1GB.
- No guarantees on reboots in your script: If your script requires a reboot, the recommendation is to place that application last during deployment. While the code attempts to handle reboots, it may fail.
- Requires a VM Agent: The VM agent must exist on the VM and be able to receive goal states.
- Multiple versions of same application on the same VM: You can't have multiple versions of the same application on a VM.

## _Let see **How to** deploy this feature._

To get on with this solution you need an Azure Compute Gallery present (previously known as shared image gallery). If you already have one you are good to go. If not create one as per [this](https://docs.microsoft.com/en-gb/azure/virtual-machines/create-gallery?tabs=cli)

**Step 1**

First Step is to create an Application Definition (VM application definitions are created within a gallery and carry information about the application and requirements for using it internally. This includes the operating system type for the VM application versions contained within the application definition.)

_**Using GUI**_

<figure>

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image.png)

<figcaption>

New VM Application Definition

</figcaption>

</figure>

[![](images/image-8.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image-8.png)

<figure>

[![](images/image-2.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image-2.png)

<figcaption>

Optional Attributes

</figcaption>

</figure>

**_Using PowerShell_**

Use the below code to create application image definition

```powershell
$applicationName = myApp
New-AzGalleryApplication `
  -ResourceGroupName $rgName `
  -GalleryName $galleryName `
  -Name $applicationName `
  -SupportedOSType Linux `
  -Description "Backend Linux application for finance."
```

**Step** 2

**_Using GUI_**

Browse the image definition you created above and create a version of the image.

Few things to highlight in here

1. **Image exe/msi file need to be saved in a storage account which can be accessed via both VM and image gallery**
2. When writing the install script you need to consider the package location in the VM as below

The download location of the application package and the configuration files are:  

- _Linux: `/var/lib/waagent/Microsoft.CPlat.Core.VMApplicationManagerLinux/<appname>/<app version>`_
- _Windows: `C:\Packages\Plugins\Microsoft.CPlat.Core.VMApplicationManagerWindows\1.0.4\Downloads\<appname>\<app version>`_

The install/update/remove commands should be written assuming the application package and the configuration file are in the current directory.

You can all add a custom configuration file with the application. But in my case I'm doing a basic installation of the application

[![](images/image-4.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image-4.png)

<figure>

[![](images/image-5.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image-5.png)

<figcaption>

During this demo I'm only going keep the application in one region. But if you need you can replicate up to 3 regions as of now.

</figcaption>

</figure>

And then just hit Create.

**_Using Powershell_**

use the below code and update it with your own parameters.

```powershell
$version = 1.0.0
New-AzGalleryApplicationVersion `
   -ResourceGroupName $rgName `
   -GalleryName $galleryName `
   -GalleryApplicationName $applicationName `
   -Name $version `
   -PackageFileLink "https://<storage account name>.blob.core.windows.net/<containder name>/<filename>" `
   -Location "East US" `
   -Install myApp.exe /silent `
   -Remove myApp.exe /uninstall `
```

Once the deployment is complete

[![](images/image-6.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image-6.png)

## _Let see **How to** Apply to a Virtual Machine_

You can attach this application either to a new VM or to a Existing Virtual Machine

_**New VM**_

Simply try to create a new virtual machine in the advance section you can select this preview feature

[![](images/image-7.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image-7.png)

[![](images/image-9.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2021/11/image-9.png)

**_Existing VM_**

As of now there is no option for us to install the application to a existing VM using GUI. Instead you can use below powershell to add the application

```powershell
$vm = Get-AzVM -ResourceGroupName $rgname -Name myVM
$vmapp = Get-AzGalleryApplicationVersion `
   -ResourceGroupName $rgname `
   -GalleryName $galleryname `
   -ApplicationName $applicationname `
   -Version $version

$vm = Add-AzVmGalleryApplication `
   -VM $vm `
   -Id $vmapp.Id

Update-AzVm -ResourceGroupName $rgname -VM $vm
```

## My Views on this new feature

To be honest. this feature is not yet ready to be used. and also there are other methods to install application in a VM ( Easy and Proven methods) Seems to me this feature is some what replication is one component of SCCM.

This will bring the same complexity of managing application versions. In the other had if you are trying to move away from your on prem infrastructure this feature will come in very handy when this goes live.

For more details and updates

https://docs.microsoft.com/en-gb/azure/virtual-machines/vm-applications
