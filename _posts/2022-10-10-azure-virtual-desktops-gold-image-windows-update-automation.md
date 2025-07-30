---
title: "Azure Virtual Desktops Gold Image Windows Update Automation"
date: 2022-10-10
categories: 
  - "azure"
---

Howdy Folks

During a recent customer engagement, I had to deploy Azure Virtual Desktop solutios via DevOps pipelines. Due to some reasons we decided to go down the gold image option for the shared hostpools. So I ended up creating compute galleries and and saved gold image files for the diffrent hostpools

This lead me thinking of a way to update these gold images without spending much time and deploy to hostpools. And found a way to do it.

There may be other way to do it but, I think based on the scenario and the services I used int this solution, this method is the ideal one

As usaul below diagram explains the flow of my pipeline.

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/10/image.png)

For this process other than azure pipelines, the main component that I will be **using is packer template.**

For those who are new to packer...

"Packer is **HashiCorp's open-source tool for creating machine images from source configuration**. You can configure Packer images with an operating system and software for your specific use-case. Terraform configuration for a compute instance can use a Packer image to provision your instance without manual configuration."

[more details](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjf5tLmw9X6AhV65XMBHY88AnQQFnoECAoQAw&url=https%3A%2F%2Flearn.hashicorp.com%2Ftutorials%2Fterraform%2Fpacker%23%3A~%3Atext%3DPacker%2520is%2520HashiCorp%27s%2520open%252Dsource%2Cyour%2520instance%2520without%2520manual%2520configuration.&usg=AOvVaw3LYu4COxSX8k5LTOSwo71C)

I'm combining packer templates with bicep to complete the tasks that I need

## Explanation

### Azure Pipeline

**Stage 1** \- In stage 1 Im constructing the image version details including the current and new version details, reason for this is I'm using these for grabbing and saving the new image version. And also when Im deploying virtual machines, I tag the VM name with image version as an example

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2022/10/image-1.png)

Tagging the VM name with image version is helpfull identify new and old vms when it comes to when we put them on to drain mode etc

```
    - task: AzurePowerShell@5
      displayName: 'Generate Image Version Details' 
      inputs: 
        azureSubscription: ${{ variables.azureServiceConnection }}
        ScriptType: 'inlineScript'  
        Inline: | 
            Select-AzSubscription -SubscriptionId ${{ variables.extAccSubID }}

            $source_imageVerions = Get-AzGalleryImageVersion -ResourceGroupName $(extaccimageGRgName) -GalleryName ${{ variables.extaccimageGName }} -GalleryImageDefinitionName $(imageDefinitionName) `
            | where-object {$_.PublishingProfile.excludeFromLatest -eq $False} | Select-object Name -ExpandProperty Name -Last 1 | Sort-Object Name

            $source_image = [decimal]$source_imageVerions.replace('.','')
            $startingCount = $source_image | Measure-Object -Character
            $target_imageVerions = $source_image + 1
            $endCount = [string]$target_imageVerions| Measure-Object -Character

            for ( [int]$endCount.Characters -eq [int]$startingCount.Characters){
              if ([int]$endCount.Characters -ge [int]$startingCount.Characters) {
                break;
                $target_imageVerions = "0" + $target_imageVerions
                $endCount = [string]$target_imageVerions| Measure-Object -Character
              }
            }

            $target_imageVerions_array = $target_imageVerions -split ""
            $target_imageVerions = $target_imageVerions_array[1] + '.' + $target_imageVerions_array[2] + '.'+ $target_imageVerions_array[3]

            Write-Host "##vso[task.setvariable variable=target_imageVerions;]$target_imageVerions"
            Write-Host "##vso[task.setvariable variable=source_imageVerions;]$source_imageVerions"
        FailOnStandardError: false
        azurePowerShellVersion: LatestVersion
        pwsh: true
```

Stage 2 - In my second stage I'm performing the tasks required for the packer image build. Tasks are as per below

1. Create tempory resource group

3. Permission delegations to perform the changes

5. Policy exclusions

7. Create a packer image and save in image galary

```
    - task: AzurePowerShell@5
      displayName: Create Temporary Resource Group
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        ScriptType: InlineScript
        Inline: |
            Select-AzSubscription -SubscriptionId ${{ variables.extAccSubID }}
            $tempname = 'rg-pkr-'+(new-guid).ToString().Substring(0,10)
            New-AzResourceGroup -Name $tempname -Location ${{ variables.Location }}
            write-output ("##vso[task.setvariable variable=TempResourceGroup;]$tempname")
        FailOnStandardError: false
        azurePowerShellVersion: LatestVersion
        pwsh: true

    - task: AzureCLI@2
      displayName: Role Base Access Controls
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        scriptType: 'pscore'  
        scriptLocation: 'inlineScript'  
        inlineScript: |
            az role assignment create --assignee 2a44b716-f6b8-4d21-90b5-a89e23734bad --role Contributor --scope /subscriptions/<sub Id>

    - task: AzurePowerShell@5
      displayName: Set temporary policy exemption on Build resource group
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        ScriptType: InlineScript
        Inline: |
            Set-AzContext "${{ variables.extAccSubID }}"
            $ResourceGroup = Get-AzResourceGroup -Name "$(TempResourceGroup)"
            $policies = "${{ variables.policyExemption }}" -split ','
            $assignment = Get-AzPolicyAssignment -Id '/providers/Microsoft.Management/managementGroups/ExtAccess/providers/Microsoft.Authorization/policyAssignments/SecGovAssign'
            New-AzPolicyExemption -Name "AvdBuildExemption-$($policy)" -PolicyAssignment $Assignment -Scope $ResourceGroup.ResourceId -ExemptionCategory Mitigated
  
            $assignment = Get-AzPolicyAssignment -Id '/providers/Microsoft.Management/managementGroups/Symal/providers/Microsoft.Authorization/policyAssignments/SecGovAssign'
            New-AzPolicyExemption -Name "AvdBuildExemption-RootPolicy" -PolicyAssignment $Assignment -Scope $ResourceGroup.ResourceId -ExemptionCategory Mitigated
  
        FailOnStandardError: false
        azurePowerShellVersion: LatestVersion
        pwsh: true

    - task: PackerBuild@1
      displayName: 'Build packer image'
      timeoutInMinutes: 120
      inputs:
        templateType: 'custom'
        customTemplateLocation: 'bicep/main/data-platform/extacc/image-build/packer.json'
        customTemplateParameters: '{"client_id":"$(packerBuildClientID)","client_secret":"$(packerClientSecret)","subscription_id":"$(extAccSubID)","tenant_id":"$(tenantID)","gallery_subscription_id":"$(extAccSubID)","build_resource_group_name":"$(TempResourceGroup)","gallery_resource_group_name":"$(extaccimageGRgName)","gallery_name":"$(extaccimageGName)","image_name":"$(imageDefinitionName)","source_image_version":"$(source_imageVerions)","target_image_version":"$(target_imageVerions)"}'
        packerVersion: 1.8.2
        imageId: 'managedImageID'
```

For packer Im using the native task packerbuild to deploy

**Packer Template**

packer tempalate has 3 sections

1. Variables - variable required for packer image build.

3. Builders - Configuration settings for the builder image

5. Provisioners - Tasks to perform ontop of the build vm

```
{
  "variables": {
    "client_id": "",
    "client_secret": "",
    "tenant_id": "",
    "subscription_id": "",
    "gallery_subscription_id": "",
    "resource_group_name": "",
    "build_resource_group_name": "",
    "gallery_resource_group_name": "",
    "gallery_name": "",
    "image_name": "",
    "source_image_version": "",
    "target_image_version": "",   
    "WorkingDirectory": "c:\\users\\packer",
    "buildartifactsCont": "build",
    "admin_user": "packer"
  
  },
  "builders": [
    {
      "type": "azure-arm",
      "client_id": "{{user `client_id`}}",
      "client_secret": "{{user `client_secret`}}",
      "tenant_id": "{{user `tenant_id`}}",
      "subscription_id": "{{user `subscription_id`}}",
      "managed_image_resource_group_name": "{{user `build_resource_group_name`}}",
      "managed_image_name": "packer-image",
      "build_resource_group_name": "{{user `build_resource_group_name`}}",
      "os_type": "Windows",
      "shared_image_gallery": {
        "subscription": "{{user `gallery_subscription_id`}}",
        "resource_group": "{{user `gallery_resource_group_name`}}",
        "gallery_name": "{{user `gallery_name`}}",
        "image_name": "{{user `image_name`}}",
        "image_version": "{{user `source_image_version`}}"
      },
      "shared_image_gallery_destination": {
        "subscription": "{{user `gallery_subscription_id`}}",
        "resource_group": "{{user `gallery_resource_group_name`}}",
        "gallery_name": "{{user `gallery_name`}}",
        "image_name": "{{user `image_name`}}",
        "image_version": "{{user `target_image_version`}}",
        "replication_regions": [
          "australiaeast"
        ],
        "storage_account_type": "Standard_LRS"
      },
      "communicator": "winrm",
      "winrm_use_ssl": true,
      "winrm_insecure": true,
      "winrm_timeout": "60m",
      "winrm_username": "{{user `admin_user`}}",
      "vm_size": "Standard_D2_v2",
      "async_resourcegroup_delete": true
    }
  ],
  "provisioners": [
    {
      "type": "windows-restart",
      "restart_timeout": "15m",
      "max_retries": 3
    },
    {
      "type": "powershell",
      "inline": [
        "$ErrorActionPreference='Stop'",
        "Write-Host \"[UPDATES]:: Install updates - PASS 1!\"",
        "Write-Host \"Installing Required Powershell Modules\"",
        "Get-PackageProvider -name nuget -force",
        "Install-Module -Name PSWindowsUpdate -Force -Confirm:$false",
        "$Updates = Get-WindowsUpdate",
        "Write-Host \"[UPDATES]:: Found $($Updates.count) updates to install - PASS 1!\"",
        "if( $Updates.count -gt 0 ){ Install-WindowsUpdate -AcceptAll -Install -AutoReboot }"
      ],
      "elevated_user": "{{user `admin_user`}}",
      "elevated_password": "{{.WinRMPassword}}"
    },
    {
      "type": "powershell",
      "pause_before": "3m",
      "inline": [
        "$ErrorActionPreference='Stop'",
        "Write-Host \"[UPDATES]:: Install updates - PASS 2!\"",
        "$Updates = Get-WindowsUpdate",
        "Write-Host \"[UPDATES]:: Found $($Updates.count) updates to install - PASS 2!\"",
        "if( $Updates.count -gt 0 ){ Install-WindowsUpdate -AcceptAll -Install -AutoReboot }"
      ],
      "elevated_user": "{{user `admin_user`}}",
      "elevated_password": "{{.WinRMPassword}}"
    },
    {
      "type": "windows-restart",
      "restart_timeout": "15m",
      "max_retries": 3
    },
    {
      "type": "powershell",
      "inline": [
        "& $env:SystemRoot\\System32\\Sysprep\\Sysprep.exe /oobe /generalize /quiet /quit",
        "while($true) { $imageState = Get-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Setup\\State | Select ImageState; if($imageState.ImageState -ne 'IMAGE_STATE_GENERALIZE_RESEAL_TO_OOBE') { Write-Output $imageState.ImageState; Start-Sleep -s 10  } else { break } }"
      ]
    }
  ]
}
```

In my above packer json template I use 3 passes to install the windows update and restart the image vm automatically. And generalize the VM template before it save in the azure compute gallary.

Once the packer template completed, I have another tasks to deploy the new set of AVD hosts to the same pool. And enable old ones. When deploying the all I do is pointing the VM image location to be the compute gallery

Conclusion

There are few key points to this solution.

1. Tagging the VM name with Image version details (which helps to identify and keep track of serves and also have old and new VM is the same host pool incase if we want to roll back after an update)

3. Running Windows update functio 3 time in packer image, which will slim the chance of missing out VM updates

5. Using packer version 1.8.2 or above

I'm sure there are other ways to perform this. But for me this pipeline fit the solution. For this pipeline to complete it will take around 45min but, all we got to do is run the pipeline. Again make the lives easy and make things efficient.

Hope this helps someone

As alwasy comment if you have any questions or reach out to me. Happy to help anyway I can

Untill next time...........
