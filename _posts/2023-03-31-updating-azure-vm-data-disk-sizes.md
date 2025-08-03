---
title: "Updating Azure VM Data Disk Sizes"
date: 2023-03-31
categories: 
  - "azure"
---

## Summary

Hope you are doing great, this time I came up with a simple azure DevOps solution for updating VM disk sizes. The current project that I'm in has a bunch of virtual machines. So, we need a way to update the VM disk with minimal administrative effort and changes. 

In this scenario, we have used.

1. Bicep as the IAC language

3. Azure DevOps pipelines

5. YAML variable files 

Here is the high-level workflow for a particular VM in the solution.

[![](images/Untitled%20Diagram.jpg)](https://www.blogger.com/blog/post/edit/3493680135498724763/6045070247294416741?hl=en#)

YAML Pipeline file got two workflows, firstly the VM build pipeline, and the second is the disk update one.  
If you focus on the green arrow and the purple arrow, basically I'm modifying the same bicep module file and passing the same set of variables. You may wonder **why we cannot use the same flow to build the VM and update the disk later, that's because for the disk updates VM needs to be in a shutdown state, and other components in the 1st flow need the VM up and running especially the extension modules**

### YAML Variable Files

I have decided to use YML variable files for my bicep modules mainly for one reason, that is because a given parameter needs to be defined only once, we can reuse the variable values anywhere by defining the variable files in the YML pipeline file.  
So, our related variable is the disk defines as below

*[Image showing YAML variable definitions - currently unavailable]*

[](https://www.blogger.com/blog/post/edit/3493680135498724763/6045070247294416741?hl=en#)

disk definition details are separated using pipes and multiple disks are separated using "commas"

**PowerShell Task**  
One of my colleagues came up with the PowerShell script to convert this particular YAML variable to JSON format as below, we are calling the given PowerShell as part of the pipeline

```
condition: eq('${{ parameters.isVMDiskUpdate }}', 'true')
    strategy:
      runOnce:
        deploy:
          steps:
          - checkout: self

          - powershell: |
              $dataDiskDefinitions = scripts\Init-DiskArray.ps1 -vmDisks "$(apAppDMZVmDisks)"
              Write-Host "##vso[task.setvariable variable=dataDiskDefinitions]$dataDiskDefinitions"
```

**PowerShell Script**

```
param (
    # format: comma separated list of: diskType|diskSizeGB|caching|createOption
    # ex: 'Premium_LRS|128|ReadOnly|Empty,Premium_LRS|3128|ReadOnly|Empty'
    [string] $vmDisks   
)
    
$diskArray = New-Object System.Collections.ArrayList

foreach($disk in $vmDisks.Split(',')) {
    $diskConfig = $disk.Split('|')
    [void]$diskArray.Add(
        [PSCustomObject]@{
            diskType = $diskConfig[0]
            diskSize = $diskConfig[1]
            caching = $diskConfig[2]
            createOption = $diskConfig[3]
        }
    )
}

$json = ConvertTo-Json -Compress -InputObject @($diskArray)
$json = $json -replace "`t|`n|`r","" -replace '"',@"
\"
"@

return $json
```

### YAML Pipeline

YAML pipeline contains both flows and is separated using a pipeline variable. During the pipeline run, we need to specify whether the run is a disk update or not. If it's a disk update it will only run a particular deployment task which is carried out below

1. shutting down the VM

3. Update the disk using the bicep template

5. Start the VM backup

```
- deployment: 'Deploy_VM_Disk_Updates'
    displayName: 'Deploy_VM_Disk_Updates'
    environment: Azure-IAC
    condition: eq('${{ parameters.isVMDiskUpdate }}', 'true')
    strategy:
      runOnce:
        deploy:
          steps:
          - checkout: self

          - powershell: |
              $dataDiskDefinitions = scripts\Init-DiskArray.ps1 -vmDisks "$(apAppDMZVmDisks)"
              Write-Host "##vso[task.setvariable variable=dataDiskDefinitions]$dataDiskDefinitions"

              # $tags = scripts\Init-Tags.ps1 -tags "$(apAppDmzTags)"
              # Write-Host "##vso[task.setvariable variable=tags]$tags"
      
          - task: AzureCLI@2
            inputs:
              azureSubscription: ${{ variables.azureServiceConnection }}
              scriptType: ps
              scriptLocation: inlineScript
              inlineScript: |
                az --version
                az account set -s ${{ variables.apSubscriptionId }}
                az vm stop --name $(apprefix) --resource-group $(apRgName)
                az vm deallocate --name $(apprefix) --resource-group $(apRgName)

                az group deployment create -g $(apRgName) `
                --template-file 'bicep/modules/v2/virtual-machine/virtual-machine-datadisk-update.bicep' `
                --parameters `
                vmNameSuffix=$(apprefix) `
                dataDisksDefinition='$(dataDiskDefinitions)'

                az vm start --name $(apprefix) --resource-group $(apRgName)
```

### Bicep Module Template

The next thing is the bicep module, the key highlight is I'm using the same bicep module to update the disks, and I'm passing the same set of parameters to it compared to the mail build bicep file.  
below is the disk module

```
@description('Virtual machine name. Do not include numerical identifier.')
@maxLength(14)
param vmNameSuffix string

@description('Virtual machine location.')
param location string = resourceGroup().location

@description('Array of objects defining data disks, including diskType and size')
@metadata({
  note: 'Sample input'
  dataDisksDefinition: [
    {
      diskType: 'StandardSSD_LRS'
      diskSize: 64
      caching: 'none'
    } 
  ]
})
param dataDisksDefinition array

resource dataDisk 'Microsoft.Compute/disks@2020-12-01' = [for (item, j) in dataDisksDefinition: {
  name: '${vmNameSuffix}_datadisk_${j}'
  location: location
  properties: {
    creationData: {
      createOption: item.createOption
    }
    diskSizeGB: item.diskSize
  }
  sku: {
    name: item.diskType
  }
}]

//${format('{0:D2}', 1)}
```

### Conclusion

The reason for this approach is  
I need a way to update the VM disk using the same variables that I used for VM build or other updates If not I won't be able to run the build/update workflow unless I do manual modifications. Now I can run VM build pipeline also at any point in time after a disk update. You now may be able to realize this is become pretty much seamless because of using the same variable for both workflows. This also means we can get the VM configurations right out of the variable files at any given point in time  
Also, I wanted a way to do it using a pipeline. This means good news for the administrators too. they only need to update the single location to update the disk configuration (Lesser administration effort)  
As always there may be many ways to do but I think this particular method suits this environment and scenario better.
