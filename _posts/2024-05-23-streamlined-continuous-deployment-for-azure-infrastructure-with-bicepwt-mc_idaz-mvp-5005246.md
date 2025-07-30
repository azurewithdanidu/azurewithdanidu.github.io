---
title: "Streamlined Continuous Deployment for Azure Infrastructure with Bicep"
date: 2024-05-23
categories: 
  - "azure"
  - "azure-devops"
  - "github-actions"
tags: 
  - "azurebiceo"
  - "bicep"
  - "cloud"
  - "devops"
  - "git"
  - "github"
  - "infrastructure"
---

### Description

I wanted to develop this solution because I have been contemplating how to minimize the effort required by IT teams to adopt DevOps practices, especially when it comes to infrastructure code. One of the main hurdles I've identified is that IT teams often need to manage YAML pipelines in addition to their new infrastructure components.

For many IT professionals, the world of DevOps and continuous integration/continuous deployment (CI/CD) can be daunting. They are typically well-versed in infrastructure management but may not have extensive experience with pipeline development. This gap in knowledge can lead to a variety of challenges:

- **Steep Learning Curve**: Learning the intricacies of YAML syntax and pipeline configuration can be time-consuming and frustrating.

- **Increased Workload**: Balancing the demands of maintaining infrastructure while also managing complex deployment pipelines adds significant workload.

- **Error-Prone Processes**: Without a strong foundation in pipeline development, there is a higher risk of errors, which can lead to deployment failures and downtime.

- **Slower Deployment Cycles**: The additional time required to manage and troubleshoot pipelines can slow down the overall deployment process, impacting agility and responsiveness.

My goal with this solution is to simplify the process as much as possible. By creating a single, streamlined pipeline for continuous deployments of Azure Infrastructure templates, we can reduce the burden on IT teams, allowing them to focus more on their core responsibilities and less on the complexities of pipeline management. This approach not only enhances efficiency but also accelerates the adoption of DevOps practices within the organization.

**Additionally, with this streamlined approach, the IT team only needs to worry about managing their Bicep templates and `bicepparam` files.** This significantly reduces the overhead involved in pipeline maintenance, as the deployment process is handled automatically by the pipeline. This simplicity enables IT teams to be more productive and responsive to changes, ensuring that infrastructure deployments are both reliable and efficient. And also, this pipeline created using Github Actions, Azure DevOps is coming soon.......

### Implementation Overview

[![](images/image-2.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2024/05/image-2.png)

For this solution to work, we will be using Azure Bicep templates along with `bicepparam` files. Bicep is a domain-specific language (DSL) for deploying Azure resources declaratively, which makes it easier to manage your infrastructure as code.

Once this pipeline is set up, the process for IT teams becomes significantly streamlined. Here’s how it works:

1. **Create Bicep Templates**: The IT team needs to create a Bicep template for their specific solution or workload. Bicep templates are modular, readable, and reusable, which simplifies the process of defining Azure resources.

3. **Configure Bicep Parameters**: Alongside the Bicep template, `bicepparam` files are used to define parameters that can be customized for different environments or deployments. This separation of template and parameters enhances flexibility and reusability.

5. **Push or Pull to Main Branch**: Once the Bicep template and `bicepparam` files are ready, the IT team simply pushes these files to the main branch of the repository. This action triggers the CI/CD pipeline.

7. **Automated Deployment**: The pipeline automatically handles the deployment of the infrastructure defined in the Bicep template using the parameters specified in the `bicepparam` files. This reduces manual intervention and ensures a consistent deployment process.

This approach not only simplifies the deployment process but also enforces best practices in infrastructure management and CI/CD. By automating the deployment of Azure infrastructure through a single pipeline, IT teams can focus more on developing solutions rather than managing complex deployment configurations.

### Pipeline Steps

The pipeline consists of several key steps, each designed to ensure a smooth and efficient deployment process. Here’s a detailed explanation of each step:

**Initialize Variables**: This step sets up the environment variables required for the pipeline. It also outputs these variables for use in subsequent steps.

```
 initialise_vars:
    runs-on: windows-latest
    outputs:
      service_tier: ${{ env.service_tier }}
      test_subscription_id: ${{ env.test_subscription_id }}
      location: ${{ env.location }}
      oidc_app_reg_client_id: ${{ env.oidc_app_reg_client_id }}
      azure_tenant_id: ${{ env.azure_tenant_id }}
      environment: ${{ env.environment }}
      workloadTier: ${{ env.workloadTier }}
```

**Login to Azure**: This step authenticates the pipeline with Azure using a service principal. This authentication is necessary for performing any actions against Azure resources.

```
- name: Login to Azure
        uses: azure/login@v1.4.6
        with:
          client-id: ${{ needs.initialise_vars.outputs.oidc_app_reg_client_id }}
          tenant-id: ${{ needs.initialise_vars.outputs.azure_tenant_id }}
          allow-no-subscriptions: true
          enable-AzPSSession: true
```

**Identify Changed Files**: The pipeline uses `tj-actions/changed-files@v44` to detect which `bicepparam` files have changed since the last commit. This helps the pipeline focus only on the files that need to be deployed.

`tj-actions/changed-files` plays a critical part by identifying the changed files and filtering them based on the extension of the file. Thats the steppingstone for this automation i would say. And what we can do is we can use this look at a particular folder instead of looking at the entire repo too. Have look at the below link about the full-on capabilities

**[https://github.com/tj-actions/changed-files](https://github.com/tj-actions/changed-files)**

```
- name: Get all changed param files
        id: changed-markdown-files
        uses: tj-actions/changed-files@v44
        with:
          # Avoid using single or double quotes for multiline patterns
          files: |
             **.bicepparam
```

**List Changed Files**: This step prints the list of changed files to the console for verification. It’s useful for debugging and ensuring that the correct files are being processed.

```
  - name: List all changed files markdown files
        env:
          ALL_CHANGED_FILES: ${{ steps.changed-markdown-files.outputs.all_changed_files }}
        run: |
          for file in ${ALL_CHANGED_FILES}; do
            echo "$file was changed"
            echo ${{ steps.changed-markdown-files.outputs.all_changed_files }}
          done          
          
```

**Set Environment Variables**: In this step, where most of the critical thing happens  
This step processes the changed `bicepparam` files, extracts necessary information, and exports it to a JSON file for use in subsequent pipeline steps. Here’s a concise breakdown:

1. **Setup Environment Variable**:
    - Initializes the `ALL_CHANGED_FILES` environment variable with paths to the changed `bicepparam` files.

3. **Initialize Results Array**:
    - Creates an empty array `$Results` to store the extracted data.

5. **Process Each File**:
    - Splits the file paths into an array.
    
    - For each file:
        - Reads the file content.
        
        - Searches for lines containing the `using` pattern to find the Bicep template path.
        
        - Extracts the template path, the file’s directory, and the file name.
        
        - Creates an object with this data and adds it to the `$Results` array.

7. **Convert to JSON**:
    - Converts the `$Results` array into a JSON string.
    
    - Writes the JSON string to `objectArray.json`.

#### Purpose and Benefits

- **Complex Data Handling**: Uses JSON to handle complex data structures, which are not supported by GitHub Actions environment variables.

- **Modularity**: Makes pipeline steps more modular and reusable.

- **Clarity and Debugging**: Facilitates debugging and ensures correct information flow.

This step ensures the necessary information is accurately captured and made available for the subsequent deployment steps, enhancing the efficiency and reliability of the deployment process.

```
  - name: Sets Environment Variables
        env:
          ALL_CHANGED_FILES: ${{ steps.changed-markdown-files.outputs.all_changed_files }}
        uses: azure/powershell@v1
        with:
          inlineScript: |
                $Results = @()
                $filePaths= "${{ env.ALL_CHANGED_FILES }}"
                $splitFilePaths =$filePaths.Split(" ")
                if ($splitFilePaths) {
                  foreach ($filePath in $splitFilePaths){
                      $fileContent = Get-Content -Path $filePath
                      $searchPattern = "using"
                      $templateFilePath = $fileContent | ForEach-Object {
                          # Check if the line contains the search pattern
                          if ($_ -match $searchPattern) {
                              # Capture the part between single quotes
                              if ($_ -match "'([^']*)'") {
                                  $capturedText = $matches[1]
                                  Write-Output $capturedText
                              }
                          }
                      } 
                      $templateFilePath
                      $paramRootPath = Split-Path -parent $filePath
                      $paramFileName = Split-Path -leaf $filePath
                      $obj = New-Object -TypeName psobject 
                      $obj | Add-member -name 'templateFilePath' -Membertype "Noteproperty" -Value $templateFilePath
                      $obj | Add-member -name 'paramRootPath' -Membertype "Noteproperty" -Value $paramRootPath
                      $obj | Add-member -name 'paramFileName' -Membertype "Noteproperty" -Value $paramFileName
                      $Results += $obj
                    }
                  }  
                else {
                    Write-Host "A line starting with 'using '<space>' was not found in the file."
                }
                $jsonString = $Results | ConvertTo-Json
                $jsonString | Out-File -FilePath objectArray.json
                # echo "paramFileArray="$jsonString"" >> $env:GITHUB_ENV
                
          azPSVersion: latest    
```

**Preview a Resource**: This step performs a "what-if" deployment, which previews the changes that will be made without actually applying them. This is useful for validation and ensuring that the deployment will proceed as expected.

```
 - name: Preview a Resource
        uses: azure/powershell@v1
        with:
          inlineScript: |
            $params = Get-Content objectArray.json
            $objectArrayFromJson = $params | ConvertFrom-Json
            write-output $objectArrayFromJson
            foreach ($param in $objectArrayFromJson){
                  push-location $param.paramRootPath
                  az account set --subscription  ${{ env.test_subscription_id }}
                  az deployment sub what-if `
                    --name 'deploy_project_resourcegroup' `
                    --location '${{ env.location }}' `
                    --subscription ${{ env.test_subscription_id }} `
                    --template-file $param.templateFilePath `
                    --parameters $param.paramFileName                
                  pop-location
                  write-output "Current directory: $(Get-Location)"
            }
          azPSVersion: latest     
```

**Deploy a Resource** (Commented Out): This step, currently commented out, would perform the actual deployment using the Azure CLI. It reads the JSON file to get the necessary parameters and then deploys the resources defined in the Bicep templates.

```
      - name: Deploy a Resource
        uses: azure/powershell@v1
        with:
          inlineScript: |
            $params = Get-Content objectArray.json
            $objectArrayFromJson = $params | ConvertFrom-Json
            write-output $objectArrayFromJson
              foreach ($param in $objectArrayFromJson){
                    set-location -path $param.paramRootPath
                    az account set --subscription  ${{ env.test_subscription_id }}
                    az deployment sub create `
                      --name 'deploy_project_resourcegroup' `
                      --location '${{ env.location }}' `
                      --subscription ${{ env.test_subscription_id }} `
                      --template-file $param.templateFile `
                      --parameters $param.paramFileName
              }
          azPSVersion: latest 
```

To further improve the pipeline, I'm thinking of adding few more things into the pipeline later down the line:

#### 1\. Store Tenant ID and App ID in Environment Secrets

- Store sensitive information like the Tenant ID and App ID in GitHub Secrets for enhanced security.

- Update the pipeline to reference these secrets.

#### 2\. Add Subscription ID and Location in the Parameter File

- Include the subscription ID and location within the parameter files for greater flexibility.

- Update the Bicep templates to reference these parameters.

#### 3\. Move Inline Scripting to PS1 Scripts

- Move the inline PowerShell scripting into `.ps1` script files.

- Call these scripts from within the pipeline for better maintainability and readability.

#### 4\. Build and Deploy Bicep Templates

- Add steps to build and validate Bicep templates before deployment.

- Ensure that the deployment process is streamlined and automated.

You can get the full pipeline file from the below link

[https://github.com/DaniduWeerasinghe911/azure-bicep-param-pipeline](https://github.com/DaniduWeerasinghe911/azure-bicep-param-pipeline)

### Conclusion

These enhancements improve security, flexibility, and maintainability of your CI/CD pipeline. Feel free to further modify and expand this setup to fit your specific needs and to enhance your infrastructure deployment processes.
