---
title: "Pipeline to start new projects in an organization"
date: 2024-08-29
categories: 
  - "azure"
  - "github-actions"
tags: 
  - "gitactions"
  - "github"
---

Howdy Folks

This time I'm here with some what a unique situation. I wanted to create a process/ pipeline to onboard new projects to a newly built environment. Following are the initial requirements

New Projects are based on

- Github Actions

- Contains both IAC and App code deployments

- Must leverage the existing subscription pattern

- Need a OICD to run deployments via Git actions

- Needs a new resource group

- Full action required at the resource group level.

Here is what I came up with,

Based on these requirements, I came up with the following process:

1. **Create a New Resource Group:** The first step is to create a new resource group in the existing subscription pattern. This resource group will serve as the dedicated environment for the new project.

3. **Configure OIDC for GitHub Actions:** Next, I configured an OIDC identity for GitHub Actions, allowing for secure authentication and authorization to the new resource group.

5. **Create GitHub Actions Workflows:** With the new resource group and OIDC identity in place, I created GitHub Actions workflows for both IAC and app code deployments. These workflows will automate the deployment process and ensure consistent and reliable deployments.

7. **Test and Validate:** Finally, I tested and validated the new pipeline, ensuring that it meets all the initial requirements and deploys the new project successfully.

By following this process, I was able to successfully onboard a new project to a newly built environment, ensuring a streamlined and efficient deployment process.

The provided YAML code is a GitHub Actions workflow named `Global Solution - Deployment`. This workflow can be triggered manually from the GitHub Actions tab in the repository and accepts several inputs, such as the environment, location, solution short name, and Git repository name.

The workflow defines several environment variables, including the Azure subscription IDs, Azure tenant ID, and the OIDC app registration client ID. It also defines the name of the service principal that will be created for the "dev" environment.

The workflow consists of two jobs: `initialise_vars` and `post_configuration`.

The `initialise_vars` job sets up the environment variables and outputs them for use in the subsequent job. It runs on the `windows-latest` operating system and does not have any specific requirements for permissions.

The `post_configuration` job depends on the `initialise_vars` job and performs the following tasks:

- Checks out the repository code using the `actions/checkout` action.

- Logs in to Azure using the OIDC app registration client ID and Azure tenant ID with the `azure/login` action.

- Creates a service principal for the "dev" environment if the environment is set to "test" using an inline PowerShell script.

- Previews the deployment of a resource group for the "dev" environment if the environment is set to "test" using the `az deployment sub what-if` command.

- Creates the deployment of a resource group for the "dev" environment if the environment is set to "test" using the `az deployment sub create` command.

The `post_configuration` job uses PowerShell to perform the Azure tasks and sets the Azure subscription based on the subscription ID output from the `initialise_vars` job. The job also uses the `what-if` parameter to preview the deployment before creating it, which allows for a dry run of the deployment to check for any issues.

The workflow also includes several conditional statements to check for the environment variable and perform the appropriate tasks. For example, the `Creating a Service Principal Dev` step only runs if the environment is set to "test".

Overall, this GitHub Actions workflow provides a structured approach to deploying a global solution to Azure, with the ability to preview the deployment and create a service principal for the "dev" environment and "prod" environment. By using environment variables and outputs, the workflow can be easily customized and reused for different environments and solutions.

## Line by Line Explanation

### Parameters and Variable

```
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Production Or Test"
        type: choice
        required: True
        options: 
            - "prod"
            - "test"
      location:
        description: "azure resources deployment location"
        type: choice
        required: True
        options:
            - australiaeast
            - westeurope
            - westus
          
      solutionShortName:
            description: "short name for the solution better to have not more that 6 charactors"
            type: string
            required: True
            default: ""

      gitRepoName:
            description: "Git Repo Name for Permission Delegations"
            type: string
            required: True
            default: ""    
```

The `on` section at the beginning of the YAML code specifies the events that will trigger the workflow. In this case, the workflow is triggered by a manual dispatch event, which is specified by `workflow_dispatch`.

The `inputs` section under `workflow_dispatch` defines the input parameters that can be provided when manually triggering the workflow. There are four input parameters defined:

- `environment`: This is a required input with a type of `choice`. The `choice` type allows for a limited set of options to be provided, in this case, either "prod" or "test". The `description` field provides a brief description of the input parameter.

- `location`: This is another required input with a type of `choice`. The options for this input parameter are the Azure resource deployment locations: "australiaeast", "westeurope", and "westus".

- `solutionShortName`: This is a required input with a type of `string`. It has a default value of an empty string. The `description` field provides a brief description of the input parameter.

- `gitRepoName`: This is a required input with a type of `string`. It has a default value of an empty string. The `description` field provides a brief description of the input parameter.

By defining these input parameters, the workflow can be customized for different environments, Azure resource deployment locations, and solution names. The input parameters can be accessed in the workflow using the `${{ inputs.parameter_name }}` syntax.

### Section 1

```
   - name: Creating a Service Principal Dev
        if: inputs.environment == 'test'
        uses: azure/powershell@v1
        with:
          inlineScript: |
            # Install-Module Microsoft.Graph -Force -verbose
            # Get-Module Microsoft.Graph
            # Import-Module Microsoft.Graph -Force
            $AccessToken = (Get-AzAccessToken -ResourceUrl "https://graph.microsoft.com").Token
            (Get-AzAccessToken -ResourceUrl "https://graph.microsoft.com").Token
            $sec = ConvertTo-SecureString $AccessToken -AsPlainText -Force
            Connect-MgGraph -AccessToken $sec
            Import-Module Microsoft.Graph.Applications
            $appName = "${{ env.spDevName }}"
            $myApp = Get-MgApplication -Filter "DisplayName eq '$appName'" -ErrorAction SilentlyContinue        
            if ($myApp) {
                Write-Output "Application $appName already exists. Skipping creation..."
            } else {
                $myApp = New-MgApplication -DisplayName "$appName"
                Write-Output "Application $appName created successfully."
            }
            $myApp 
            start-sleep -Seconds 300
            $subscriptionId = (Get-AzContext).Subscription.Id
            $tenantId = (Get-AzContext).Subscription.TenantId
            $githubOrganisation = "orgName"
            $githubRepo = "${{ inputs.gitRepoName}}"
            $gitBranch = "main"
            $gitFederationName = "grp-azure-${{ env.solutionShortName }}-actions"
            $clientId = $myApp.id
            $policy = "repo:$githubOrganisation/$($githubRepo):ref:refs/heads/$gitBranch"
            $creds = get-MgApplicationFederatedIdentityCredential -ApplicationId $myApp.id | where-object {$_.Subject -eq $policy}
            if($creds){
              Write-Output "Policy details $policy already exists. Skipping creation..."
            } else {
              $federatedApp = New-MgApplicationFederatedIdentityCredential -ApplicationId $clientId `
              -Audiences api://AzureADTokenExchange -Issuer "https://token.actions.githubusercontent.com" -Name $gitFederationName -Subject $policy
            }
            echo "devObjectId=$myApp.ObjectId" >> $env:GITHUB_ENV
          
          azPSVersion: latest
```

This is a step in the GitHub Actions workflow that creates a service principal for the development environment if the `environment` input is set to `test`. Here's a breakdown of the step:

- `name`: The name of the step is "Creating a Service Principal Dev".

- `if`: This is a conditional statement that checks if the `environment` input is equal to `test`. If true, the step will be executed.

- `uses`: This specifies the GitHub Marketplace action to be used, which is `azure/powershell@v1` in this case.

- `with`: This specifies the input parameters for the `azure/powershell@v1` action.
    - `inlineScript`: This is a PowerShell script that performs the following tasks:
        - Gets an access token for Microsoft Graph API.
        
        - Connects to Microsoft Graph API using the access token.
        
        - Imports the `Microsoft.Graph.Applications` module.
        
        - Checks if an application with the name `${{ env.spDevName }}` already exists. If it does, the step skips the creation of the application. If not, the step creates a new application.
        
        - Creates a new federated identity credential for the application using the GitHub Actions OIDC provider.
        
        - Sets the `devObjectId` environment variable to the object ID of the created application.

The PowerShell script performs the following tasks:

- Authenticates to Microsoft Graph API using the access token.

- Imports the `Microsoft.Graph.Applications` module.

- Checks if an application with the name `${{ env.spDevName }}` already exists. If it does, the step skips the creation of the application. If not, the step creates a new application.

- Creates a new federated identity credential for the application using the GitHub Actions OIDC provider.

- Sets the `devObjectId` environment variable to the object ID of the created application.

The step also sets the `azPSVersion` input parameter to `latest`, which specifies the version of Azure PowerShell to be used.

In summary, this step creates a service principal for the development environment if the `environment` input is set to `test`. It uses Microsoft Graph API to create a new application and a new federated identity credential for the application using the GitHub Actions OIDC provider. The step also sets the `devObjectId` environment variable to the object ID of the created application.

### Section 2

```
    - name: Create a ResourceGroup Dev
        if: inputs.environment == 'test'
        run: |
            az account set --subscription  ${{ env.test_subscription_id }}
            az deployment sub create `
            --name 'deploy_project_resourcegroup' `
            --location '${{ inputs.location }}' `
            --subscription ${{ env.test_subscription_id }} `
            --template-file bicep/operations/resource-group/main.bicep `
            --parameters `
            location="${{ needs.initialise_vars.outputs.location }}" `
            workloadTier="${{ needs.initialise_vars.outputs.workloadTier }}" `
            deploymentEnvironment="${{ needs.initialise_vars.outputs.environment }}" `
            solutionShortName="${{ needs.initialise_vars.outputs.solutionShortName }}" `
            principalId="${{ env.devObjectId }}"

        shell: pwsh
```

This is a step in the GitHub Actions workflow that creates a resource group in the test subscription if the `environment` input is set to `test`. Here's a breakdown of the step:

- `name`: The name of the step is "Create a ResourceGroup Dev".

- `if`: This is a conditional statement that checks if the `environment` input is equal to `test`. If true, the step will be executed.

- `run`: This specifies the commands to be executed in the step. The commands are written in PowerShell and are executed in the `pwsh` shell.

```
az account set --subscription ${{ env.test_subscription_id }}: This sets the Azure subscription to the test subscription ID.
az deployment sub create --name 'deploy_project_resourcegroup' --location '${{ inputs.location }}' --subscription ${{ env.test_subscription_id }} --template-file bicep/operations/resource-group/main.bicep --parameters location="${{ needs.initialise_vars.outputs.location }}" workloadTier="${{ needs.initialise_vars.outputs.workloadTier }}" deploymentEnvironment="${{ needs.initialise_vars.outputs.environment }}" solutionShortName="${{ needs.initialise_vars.outputs.solutionShortName }}" principalId="${{ env.devObjectId }}"
```

In summary, this step creates a resource group in the test subscription if the `environment` input is set to `test`. It uses the Azure CLI to set the subscription and create the resource group using a Bicep template. The input parameters for the Bicep template are passed using the `--parameters` flag.

Section 1 and Section 2 repeats for Prod environment selections as well.

Summary

To summarize, we have discussed a basic GitHub Actions workflow for deploying a global solution to Azure. This workflow includes creating a service principal, initializing variables, and creating a resource group in the test environment. We have also reviewed the different parts of the YAML code, including the `on`, `env`, `jobs`, and `steps` sections.

The pipeline we have discussed is a basic one, and there is always room for improvement depending on the specific requirements of the project. For example, additional steps can be added to deploy infrastructure or applications, or to perform testing and validation. Additionally, more advanced features such as parallelism, matrix builds, and dependencies can be added to further optimize the workflow.

Complete Pipeline

[https://github.com/DaniduWeerasinghe911/Azure-New-Project-Onboarding](https://github.com/DaniduWeerasinghe911/Azure-New-Project-Onboarding)
