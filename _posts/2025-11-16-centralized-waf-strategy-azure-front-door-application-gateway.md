---
title: "Building a Centralized WAF Strategy with Azure Front Door Premium and Application Gateway v2"
date: 2025-11-16
categories:
  - "azure"
  - "security"
  - "networking"
tags:
  - "waf"
  - "azure-front-door"
  - "application-gateway"
  - "bicep"
  - "private-link"
  - "infrastructure"
---

Howdy Folks,

If you're managing multiple web applications across Azure regions, you've probably felt the pain of scattered security policies, inconsistent WAF configurations, and the headache of monitoring threats across different services. What if you could create a single, centralized entry point for all your web traffic with unified WAF protection at the edge? That's exactly what we're going to build today.

In this post, I'll walk you through implementing a cost-effective, centralized Web Application Firewall (WAF) strategy using Azure Front Door Premium as your single global security perimeter, backed by Application Gateway Standard_v2 for regional load balancing. This architecture is particularly valuable for organizations with hybrid environments, legacy infrastructure, or multi-region deployments that need comprehensive edge protection without the overhead of managing multiple WAF layers.

But here's the thing - this isn't a silver bullet. Every architecture has trade-offs, and I'll be completely honest about them. The key trade-off here: we're protecting all external traffic at the Front Door edge, but internal traffic (VNet-to-VNet or on-premises-to-Azure) only gets network-level protection from Azure Firewall, not application-level WAF inspection. For most organizations, this is an acceptable compromise that saves significant cost and complexity.

## The Challenge: Fragmented WAF Management

Let's paint a realistic picture. You've got:

- Legacy IaaS web servers running in multiple Azure regions
- Modern Azure PaaS services (App Services, Container Apps, APIs)
- On-premises applications being migrated to the cloud
- Multiple development teams managing their own applications
- Inconsistent security policies across different services
- No unified view of threats and attacks

Each team configures their own WAF rules, manages their own SSL certificates, and monitors their own logs. Your security team is drowning in alerts from different sources, and compliance audits are a nightmare.

Sound familiar? This is where a centralized WAF strategy becomes not just nice to have, but essential.

## The Architecture: Edge Protection with Regional Load Balancing

Here's the high-level architecture we're building:

```
Internet Traffic (External)
       |
       v
[Azure Front Door Premium WAF] <-- Global, Anycast (ONLY WAF Layer)
       |
       +-- Private Link --> [Application Gateway Standard_v2] <-- Regional Load Balancer
       |                            |
       |                            +-- IaaS VMs
       |                            +-- Legacy Web Servers
       |                            +-- On-prem Services (via ExpressRoute)
       |
       +-- Private Link --> [App Service]
       |
       +-- Private Link --> [Container Apps]
       |
       +-- Private Link --> [Azure Storage]

Internal Traffic (VNet-to-VNet, On-Prem-to-Azure)
       |
       v
[Azure Firewall] <-- Layer 3/4 Protection Only
       |
       v
[Application Gateway Standard_v2] <-- Regional Load Balancer
       |
       +-- IaaS VMs
       +-- Legacy Web Servers
```

### Key Components Explained

**Azure Front Door Premium** serves as your ONLY WAF layer and global entry point:
- Single public IP/endpoint for all your applications worldwide
- Comprehensive WAF protection for ALL external traffic before it reaches Azure
- Anycast routing ensures users connect to the nearest Microsoft edge location
- Built-in DDoS protection (Layer 7)
- Bot protection and managed rule sets
- Rate limiting at the edge
- Private Link support for secure backend connections
- Since this is your only WAF, it must be comprehensive and well-tuned

**Application Gateway Standard_v2** handles regional load balancing and routing ONLY:
- Regional load balancing within your virtual networks
- NO WAF capabilities (cost optimization)
- SSL offloading and end-to-end TLS
- Path-based routing for complex applications
- Integration with virtual network NSGs and route tables
- Backend health monitoring
- Autoscaling based on traffic patterns
- ~$100/month cheaper per instance compared to WAF_v2

**Azure Firewall** protects internal traffic:
- Layer 3/4 protection for VNet-to-VNet and on-premises-to-Azure traffic
- IP filtering, port filtering, protocol filtering
- Application FQDN filtering
- Threat intelligence-based filtering
- No application-level WAF inspection (SQL injection, XSS, etc.)

### Why This Approach Works

**Cost-Effective**: Using Application Gateway Standard_v2 instead of WAF_v2 saves approximately $100/month per gateway. For organizations with multiple Application Gateways, this adds up quickly.

**Performance Optimized**: Traffic is inspected by WAF only once at the Front Door edge, avoiding the performance overhead of double-WAF inspection. No redundant TLS termination and re-encryption cycles between WAF layers.

**Simplified Management**: Security teams manage a single, comprehensive WAF policy at Front Door. No policy conflicts, no rule duplication, no confusion about which layer blocked a request.

**Global + Regional Coverage**: Front Door handles global distribution and edge security, while Application Gateway provides deep integration with your Azure virtual networks and on-premises connectivity.

**Hybrid Support**: Application Gateway connects to legacy IaaS VMs, on-premises applications via ExpressRoute/VPN, and services that can't use Private Link directly.

### The Key Trade-Off: Internal Traffic Protection

Here's what you need to understand: **Internal traffic (VNet-to-VNet and on-premises-to-Azure) does NOT go through WAF inspection**. This traffic is protected by Azure Firewall at Layer 3/4 (IP addresses, ports, protocols) but not at Layer 7 (application-level attacks like SQL injection, XSS, etc.).

**What this means**:
- External internet traffic: Fully protected by Front Door Premium WAF
- Internal VNet-to-VNet traffic: Protected by Azure Firewall (network level only)
- On-premises-to-Azure traffic: Protected by Azure Firewall (network level only)
- Internal traffic has NO protection against SQL injection, XSS, or other application-layer attacks

**Why this is usually acceptable**:
- Internal traffic typically originates from trusted sources (your own VNets, your own on-premises network)
- Azure Firewall still provides robust network-level protection
- Most application-layer attacks originate from the public internet, which IS protected by WAF
- The cost savings and performance benefits often outweigh the reduced internal protection

**When you might want WAF on Application Gateway anyway**:
- Zero-trust security requirements where even internal traffic must be inspected
- Highly regulated industries (finance, healthcare) with strict compliance mandates
- Multi-tenant environments where different VNets may not fully trust each other
- Known internal threat vectors or insider risk concerns

If these scenarios apply to you, consider using Application Gateway WAF_v2 instead, accepting the higher cost and performance overhead for the added security.

## When to Use This Pattern

This architecture shines in these scenarios:

### 1. Multi-Region Deployments with Legacy Infrastructure

You have applications running across multiple Azure regions AND legacy IaaS servers that can't be easily migrated to PaaS.

**Example**: A global e-commerce platform with legacy .NET Framework applications on Windows VMs in East US, Europe North, and Southeast Asia, plus new microservices on Container Apps.

### 2. Hybrid Cloud Environments

Your applications span Azure and on-premises data centers, and you need consistent security policies for external traffic.

**Example**: A financial services company migrating to Azure but maintaining critical on-premises systems that integrate with cloud-based customer portals.

### 3. Cost-Conscious Organizations

You need centralized WAF protection but want to minimize costs by avoiding redundant WAF layers.

**Example**: Mid-sized enterprises with 5-10 web applications that need comprehensive edge protection but have limited security budgets.

### 4. Performance-Sensitive Applications

Your applications require low latency and can't afford the overhead of multiple WAF inspection layers.

**Example**: Gaming platforms or real-time trading applications where every millisecond counts.

### 5. Large Enterprise Organizations

Multiple business units or development teams deploying applications independently, but security needs to be centrally managed at the edge.

**Example**: A multinational corporation with 20+ development teams, each running their own applications, but the CISO needs unified threat visibility.

### When NOT to Use This Pattern

Let's be real - this architecture isn't always the right choice:

**Pure PaaS Deployments**: If all your applications are modern PaaS services (App Services, Container Apps, Functions), you probably don't need Application Gateway at all. Front Door with Private Link directly to your PaaS services is simpler and cheaper.

**Single Region, Simple Workloads**: If you're running a simple web application in one region with no compliance requirements, this is overkill. Application Gateway Standard_v2 alone (without Front Door) might be sufficient.

**Extreme Security Requirements**: If you have zero-trust requirements where even internal traffic must have full application-level WAF protection, use Application Gateway WAF_v2 instead of Standard_v2.

**Startups and MVPs**: If you're building an MVP or startup product, start simple. Add complexity when you need it, not before.

## Implementation Guide: Step-by-Step

Let's build this thing. I'll show you the Bicep templates and walk through the deployment process.

### Prerequisites

Before we start, make sure you have:

- An Azure subscription with appropriate permissions
- Azure CLI installed (version 2.40.0 or higher)
- Basic understanding of Azure networking (VNets, subnets, NSGs)
- A custom domain (optional but recommended for production)

### Step 1: Deploy Application Gateway Standard_v2

Now let's deploy the Application Gateway for regional load balancing.

#### Create the Bicep Template

Create a file named `appgateway-standard.bicep`:

```bicep
@description('The name of the Application Gateway')
param appGatewayName string = 'appgw-standard-${uniqueString(resourceGroup().id)}'

@description('The location for all resources')
param location string = resourceGroup().location

@description('Virtual Network name for Application Gateway')
param vnetName string = 'vnet-appgw'

@description('Address prefix for the VNet')
param vnetAddressPrefix string = '10.0.0.0/16'

@description('Subnet prefix for Application Gateway')
param appGatewaySubnetPrefix string = '10.0.1.0/24'

@description('Subnet prefix for backend servers')
param backendSubnetPrefix string = '10.0.2.0/24'

@description('Backend server IP addresses')
param backendIpAddresses array = []

@description('Minimum instance count for autoscaling')
@minValue(0)
@maxValue(10)
param minCapacity int = 2

@description('Maximum instance count for autoscaling')
@minValue(1)
@maxValue(125)
param maxCapacity int = 10

@description('Enable Private Link configuration')
param enablePrivateLink bool = true

@description('The environment name (dev, staging, prod)')
param environment string = 'dev'

// Deploy Virtual Network
module vnet 'br/public:avm/res/network/virtual-network:0.5.2' = {
  name: 'vnetDeployment'
  params: {
    name: vnetName
    location: location
    addressPrefixes: [
      vnetAddressPrefix
    ]
    subnets: [
      {
        name: 'appgw-subnet'
        addressPrefix: appGatewaySubnetPrefix
        privateEndpointNetworkPolicies: 'Disabled'
      }
      {
        name: 'backend-subnet'
        addressPrefix: backendSubnetPrefix
      }
    ]
    tags: {
      Environment: environment
      Purpose: 'Application Gateway Network'
    }
  }
}

// Deploy Public IP
module publicIP 'br/public:avm/res/network/public-ip-address:0.6.0' = {
  name: 'publicIpDeployment'
  params: {
    name: '${appGatewayName}-pip'
    location: location
    skuName: 'Standard'
    publicIPAllocationMethod: 'Static'
    dnsSettings: {
      domainNameLabel: toLower(appGatewayName)
    }
    tags: {
      Environment: environment
      Purpose: 'Application Gateway Public IP'
    }
  }
}

// Deploy Application Gateway Standard_v2
module appGateway 'br/public:avm/res/network/application-gateway:0.4.0' = {
  name: 'appGatewayDeployment'
  params: {
    name: appGatewayName
    location: location

    // SKU Configuration - Standard_v2 for cost optimization
    sku: 'Standard_v2'
    tier: 'Standard_v2'

    // Autoscaling Configuration
    autoscaleMinCapacity: minCapacity
    autoscaleMaxCapacity: maxCapacity

    // Gateway IP Configuration
    gatewayIPConfigurations: [
      {
        name: 'appGatewayIpConfig'
        properties: {
          subnet: {
            id: vnet.outputs.subnetResourceIds[0]  // appgw-subnet
          }
        }
      }
    ]

    // Frontend IP Configurations
    frontendIPConfigurations: [
      {
        name: 'appGwPublicFrontendIp'
        properties: {
          publicIPAddress: {
            id: publicIP.outputs.resourceId
          }
        }
      }
      // Private Frontend IP for Private Link
      {
        name: 'appGwPrivateFrontendIp'
        properties: {
          privateIPAddress: cidrHost(appGatewaySubnetPrefix, 10)
          privateIPAllocationMethod: 'Static'
          subnet: {
            id: vnet.outputs.subnetResourceIds[0]
          }
        }
      }
    ]

    // Frontend Ports
    frontendPorts: [
      {
        name: 'port_80'
        properties: {
          port: 80
        }
      }
      {
        name: 'port_443'
        properties: {
          port: 443
        }
      }
    ]

    // Backend Address Pools
    backendAddressPools: [
      {
        name: 'defaultBackendPool'
        properties: {
          backendAddresses: [for ip in backendIpAddresses: {
            ipAddress: ip
          }]
        }
      }
    ]

    // Backend HTTP Settings
    backendHttpSettingsCollection: [
      {
        name: 'defaultHttpSettings'
        properties: {
          port: 80
          protocol: 'Http'
          cookieBasedAffinity: 'Disabled'
          requestTimeout: 30
          pickHostNameFromBackendAddress: false
          probe: {
            id: resourceId('Microsoft.Network/applicationGateways/probes', appGatewayName, 'defaultHealthProbe')
          }
        }
      }
    ]

    // HTTP Listeners
    httpListeners: [
      {
        name: 'defaultHttpListener'
        properties: {
          frontendIPConfiguration: {
            id: resourceId('Microsoft.Network/applicationGateways/frontendIPConfigurations', appGatewayName, 'appGwPublicFrontendIp')
          }
          frontendPort: {
            id: resourceId('Microsoft.Network/applicationGateways/frontendPorts', appGatewayName, 'port_80')
          }
          protocol: 'Http'
        }
      }
    ]

    // Request Routing Rules
    requestRoutingRules: [
      {
        name: 'defaultRoutingRule'
        properties: {
          ruleType: 'Basic'
          priority: 100
          httpListener: {
            id: resourceId('Microsoft.Network/applicationGateways/httpListeners', appGatewayName, 'defaultHttpListener')
          }
          backendAddressPool: {
            id: resourceId('Microsoft.Network/applicationGateways/backendAddressPools', appGatewayName, 'defaultBackendPool')
          }
          backendHttpSettings: {
            id: resourceId('Microsoft.Network/applicationGateways/backendHttpSettingsCollection', appGatewayName, 'defaultHttpSettings')
          }
        }
      }
    ]

    // Health Probes
    probes: [
      {
        name: 'defaultHealthProbe'
        properties: {
          protocol: 'Http'
          path: '/'
          interval: 30
          timeout: 30
          unhealthyThreshold: 3
          pickHostNameFromBackendHttpSettings: true
          minServers: 0
        }
      }
    ]

    // Private Link Configuration
    privateLinkConfigurations: enablePrivateLink ? [
      {
        name: 'appgw-privatelink-config'
        properties: {
          ipConfigurations: [
            {
              name: 'privatelink-ipconfig'
              properties: {
                privateIPAllocationMethod: 'Dynamic'
                subnet: {
                  id: vnet.outputs.subnetResourceIds[0]
                }
                primary: true
              }
            }
          ]
        }
      }
    ] : []

    // Tags
    tags: {
      Environment: environment
      Purpose: 'Regional Load Balancer - NO WAF (cost optimization)'
      Tier: 'Standard_v2'
    }
  }
}

// Outputs
output appGatewayId string = appGateway.outputs.resourceId
output appGatewayName string = appGateway.outputs.name
output publicIpAddress string = publicIP.outputs.ipAddress
output publicFQDN string = publicIP.outputs.fqdn
output privateLinkConfigurationName string = enablePrivateLink ? 'appgw-privatelink-config' : ''
output privateFrontendIpConfigName string = enablePrivateLink ? 'appGwPrivateFrontendIp' : ''
output vnetId string = vnet.outputs.resourceId
```

Deploy this with:

```bash
az deployment group create \
  --resource-group rg-centralized-waf \
  --template-file appgateway-standard.bicep \
  --parameters environment=prod \
               minCapacity=2 \
               maxCapacity=10 \
               enablePrivateLink=true
```

### Step 2: Deploy Azure Front Door Premium with WAF

Now let's create Front Door with a comprehensive WAF policy.

#### Create the Bicep Template

Create a file named `frontdoor-premium.bicep`:

```bicep
@description('The name of the Azure Front Door profile')
param frontDoorName string = 'afd-${uniqueString(resourceGroup().id)}'

@description('The name of the Front Door endpoint')
param endpointName string = 'ep-${uniqueString(resourceGroup().id)}'

@description('The location for Front Door metadata')
param location string = 'global'

@description('The environment name (dev, staging, prod)')
param environment string = 'dev'

@description('Application Gateway resource ID for Private Link origin')
param appGatewayResourceId string

@description('Application Gateway Private Link Configuration Name')
param appGatewayPrivateLinkConfigName string

@description('Application Gateway Frontend IP Configuration Name')
param appGatewayFrontendIpConfigName string

@description('Application Gateway region')
param appGatewayRegion string

@description('Application Gateway hostname')
param appGatewayHostname string

@description('Additional PaaS origins (App Services, Container Apps, etc)')
param paasOrigins array = []

// Deploy Front Door WAF Policy
module wafPolicy 'br/public:avm/res/network/front-door-web-application-firewall-policy:0.3.0' = {
  name: 'wafPolicyDeployment'
  params: {
    name: '${frontDoorName}wafpolicy'
    location: location
    sku: 'Premium_AzureFrontDoor'

    // Policy Settings - Comprehensive protection
    policySettings: {
      enabledState: 'Enabled'
      mode: 'Prevention'  // Start with Detection, move to Prevention after testing
      requestBodyCheck: 'Enabled'
      customBlockResponseStatusCode: 403
      customBlockResponseBody: base64('<html><head><title>Access Denied</title></head><body><h1>Access Denied</h1><p>Your access has been blocked by our Web Application Firewall.</p></body></html>')
    }

    // Custom Rules - Edge Protection
    customRules: [
      {
        name: 'RateLimitRule'
        priority: 10
        ruleType: 'RateLimitRule'
        rateLimitThreshold: 1000
        rateLimitDurationInMinutes: 1
        action: 'Block'
        matchConditions: [
          {
            matchVariable: 'RemoteAddr'
            operator: 'IPMatch'
            matchValue: [
              '0.0.0.0/0'
              '::/0'
            ]
          }
        ]
      }
      {
        name: 'BlockSpecificUserAgents'
        priority: 20
        ruleType: 'MatchRule'
        action: 'Block'
        matchConditions: [
          {
            matchVariable: 'RequestHeader'
            selector: 'User-Agent'
            operator: 'Contains'
            matchValue: [
              'BadBot'
              'Scrapy'
              'curl'
            ]
          }
        ]
      }
      {
        name: 'GeoBlockHighRiskCountries'
        priority: 30
        ruleType: 'MatchRule'
        action: 'Block'
        matchConditions: [
          {
            matchVariable: 'RemoteAddr'
            operator: 'GeoMatch'
            matchValue: [
              'CN'
              'RU'
              'KP'
            ]
          }
        ]
      }
    ]

    // Managed Rules - Complete OWASP Coverage
    managedRuleSets: [
      {
        ruleSetType: 'Microsoft_DefaultRuleSet'
        ruleSetVersion: '2.1'
        ruleSetAction: 'Block'
      }
      {
        ruleSetType: 'Microsoft_BotManagerRuleSet'
        ruleSetVersion: '1.0'
      }
    ]

    tags: {
      Environment: environment
      Purpose: 'Centralized WAF - Single Layer Protection'
    }
  }
}

// Deploy Front Door Profile
module frontDoor 'br/public:avm/res/cdn/profile:0.8.0' = {
  name: 'frontDoorDeployment'
  params: {
    name: frontDoorName
    location: location
    sku: 'Premium_AzureFrontDoor'

    // Origin Response Timeout
    originResponseTimeoutSeconds: 60

    // Endpoints
    endpoints: [
      {
        name: endpointName
        enabledState: 'Enabled'
        tags: {
          Environment: environment
        }
      }
    ]

    // Origin Groups
    originGroups: [
      // Application Gateway Origin Group (Private Link)
      {
        name: 'og-appgateway'
        loadBalancingSettings: {
          sampleSize: 4
          successfulSamplesRequired: 3
          additionalLatencyInMilliseconds: 50
        }
        healthProbeSettings: {
          probePath: '/'
          probeRequestType: 'GET'
          probeProtocol: 'Http'
          probeIntervalInSeconds: 30
        }
        sessionAffinityState: 'Disabled'

        // Origins in this group
        origins: [
          {
            name: 'origin-appgateway'
            hostName: appGatewayHostname
            httpPort: 80
            httpsPort: 443
            originHostHeader: appGatewayHostname
            priority: 1
            weight: 1000
            enabledState: 'Enabled'

            // Private Link Configuration
            sharedPrivateLinkResource: {
              privateLink: {
                id: appGatewayResourceId
              }
              privateLinkLocation: appGatewayRegion
              groupId: appGatewayPrivateLinkConfigName
              requestMessage: 'Front Door Premium Private Link to Application Gateway'
            }
          }
        ]
      }
    ]

    // Routes
    routes: [
      {
        name: 'route-appgateway'
        enabledState: 'Enabled'
        endpointName: endpointName
        forwardingProtocol: 'MatchRequest'
        httpsRedirect: 'Enabled'
        linkToDefaultDomain: 'Enabled'

        originGroupName: 'og-appgateway'

        patternsToMatch: [
          '/legacy/*'
          '/iaas/*'
        ]

        supportedProtocols: [
          'Http'
          'Https'
        ]
      }
    ]

    // Security Policies - Link WAF to Endpoints
    securityPolicies: [
      {
        name: 'sec-policy-global'
        policyType: 'WebApplicationFirewall'
        wafPolicyResourceId: wafPolicy.outputs.resourceId

        associations: [
          {
            domains: [
              {
                id: resourceId('Microsoft.Cdn/profiles/afdEndpoints', frontDoorName, endpointName)
              }
            ]
            patternsToMatch: [
              '/*'
            ]
          }
        ]
      }
    ]

    tags: {
      Environment: environment
      Purpose: 'Global Edge Security and Distribution'
      WAFLayer: 'Single Comprehensive Layer'
    }
  }
  dependsOn: [
    wafPolicy
  ]
}

// Outputs
output frontDoorId string = frontDoor.outputs.resourceId
output frontDoorName string = frontDoor.outputs.name
output endpointHostname string = frontDoor.outputs.endpoints[0].properties.hostName
output endpointUrl string = 'https://${frontDoor.outputs.endpoints[0].properties.hostName}'
output wafPolicyId string = wafPolicy.outputs.resourceId
output frontDoorProfileId string = frontDoor.outputs.frontDoorId
```

Deploy Front Door:

```bash
# First, get the Application Gateway details
APP_GW_ID=$(az network application-gateway show \
  --resource-group rg-centralized-waf \
  --name appgw-standard-xxxxx \
  --query id -o tsv)

APP_GW_HOSTNAME=$(az network public-ip show \
  --resource-group rg-centralized-waf \
  --name appgw-standard-xxxxx-pip \
  --query dnsSettings.fqdn -o tsv)

# Deploy Front Door
az deployment group create \
  --resource-group rg-centralized-waf \
  --template-file frontdoor-premium.bicep \
  --parameters environment=prod \
               appGatewayResourceId="$APP_GW_ID" \
               appGatewayPrivateLinkConfigName='appgw-privatelink-config' \
               appGatewayFrontendIpConfigName='appGwPrivateFrontendIp' \
               appGatewayRegion='eastus' \
               appGatewayHostname="$APP_GW_HOSTNAME"
```

### Step 3: Approve the Private Link Connection

After deploying Front Door, you need to approve the Private Endpoint connection at the Application Gateway:

```bash
# List pending private endpoint connections
az network application-gateway private-endpoint-connection list \
  --resource-group rg-centralized-waf \
  --gateway-name appgw-standard-xxxxx

# Approve the connection
az network application-gateway private-endpoint-connection approve \
  --resource-group rg-centralized-waf \
  --gateway-name appgw-standard-xxxxx \
  --name <connection-name-from-list> \
  --description "Approved for Front Door Premium integration"
```

Alternatively, through the Azure Portal:
1. Navigate to your Application Gateway
2. Select **Private endpoint connections** under Settings
3. Find the pending connection from Front Door
4. Click **Approve**
5. Wait 5-10 minutes for the connection to establish

### Step 4: Configure Logging and Monitoring

Centralized logging is critical for this architecture, especially since you have only one WAF layer.

Create a file named `monitoring.bicep`:

```bicep
@description('Log Analytics workspace name')
param logAnalyticsName string = 'law-centralized-waf'

@description('Location for Log Analytics')
param location string = resourceGroup().location

@description('Front Door resource ID')
param frontDoorResourceId string

@description('Application Gateway resource ID')
param appGatewayResourceId string

@description('Environment name')
param environment string = 'prod'

// Deploy Log Analytics Workspace
module logAnalytics 'br/public:avm/res/operational-insights/workspace:0.9.0' = {
  name: 'logAnalyticsDeployment'
  params: {
    name: logAnalyticsName
    location: location

    // Retention and SKU
    dataRetention: 90  // 90 days retention
    skuName: 'PerGB2018'

    // Solutions (optional, for advanced monitoring)
    gallerySolutions: [
      {
        name: 'SecurityInsights'  // Azure Sentinel
        product: 'OMSGallery/SecurityInsights'
        publisher: 'Microsoft'
      }
    ]

    tags: {
      Environment: environment
      Purpose: 'Centralized WAF Logging'
    }
  }
}

output logAnalyticsWorkspaceId string = logAnalytics.outputs.resourceId
output logAnalyticsWorkspaceName string = logAnalytics.outputs.name
```

**Best practice**: When deploying Application Gateway and Front Door, include diagnostic settings in the module parameters:

```bicep
module appGateway 'br/public:avm/res/network/application-gateway:0.4.0' = {
  params: {
    // ... other parameters

    // Diagnostic Settings
    diagnosticSettings: [
      {
        name: 'appgw-diagnostics'
        workspaceResourceId: logAnalyticsWorkspaceId
        logCategoriesAndGroups: [
          {
            categoryGroup: 'allLogs'
            enabled: true
          }
        ]
        metricCategories: [
          {
            category: 'AllMetrics'
            enabled: true
          }
        ]
      }
    ]
  }
}
```

## The Gotchas: What They Don't Tell You

Alright, let's talk about the elephants in the room. This architecture is powerful and cost-effective, but it comes with trade-offs and challenges you need to understand.

### 1. Internal Traffic Has No WAF Protection

**The Reality**: This is the biggest trade-off in this architecture. VNet-to-VNet traffic and on-premises-to-Azure traffic bypasses WAF inspection entirely.

**What you're missing**:
- No protection against SQL injection in internal traffic
- No XSS protection for internal requests
- No file upload validation at the application level
- No custom WAF rules for internal API calls

**What you still have**:
- Azure Firewall provides Layer 3/4 protection (IP, port, protocol filtering)
- Network Security Groups (NSGs) control access between subnets
- Application-level authentication and authorization still work
- Azure DDoS Protection (if enabled) protects the VNet

**When this is acceptable**:
- Internal traffic originates from trusted sources (your own VNets, your own data centers)
- You have strong network segmentation and least-privilege access controls
- Your applications implement proper input validation and secure coding practices
- Most of your threat surface is from the public internet (which IS protected)

**When you need WAF for internal traffic**:
- Zero-trust security model where no internal traffic is trusted by default
- Highly regulated industries (finance, healthcare, government)
- Multi-tenant environments where different VNets may be adversarial
- Known internal threat vectors or compliance requirements for internal inspection

**Mitigation options if you need internal WAF**:
1. Use Application Gateway WAF_v2 instead of Standard_v2 (accept the ~$100/month cost increase)
2. Deploy Azure Firewall Premium with TLS inspection for internal traffic
3. Implement application-level WAF libraries in your backend code
4. Use Azure API Management with WAF policies for internal APIs

### 2. Cost - But Much Better Than Double-WAF

**The Reality**: Running both Azure Front Door Premium and Application Gateway Standard_v2 is still not cheap, but significantly cheaper than using WAF_v2.

**Cost Breakdown (US East, approximate monthly costs)**:
- **Azure Front Door Premium**: $330/month base fee + $0.015 per 10,000 requests + data transfer costs
- **Application Gateway Standard_v2**: ~$125/month for 2 instances + $0.008 per GB processed + capacity unit costs
- **Private Link**: Included in Front Door Premium (no extra charge)
- **Total baseline**: ~$455/month BEFORE any traffic

**Compare this to the double-WAF approach**:
- Azure Front Door Premium: $330/month
- Application Gateway WAF_v2: ~$225/month
- Total baseline: ~$555/month
- **Savings with this approach: $100/month per Application Gateway**

**At Scale**:
- 10 million requests/month: Add ~$150
- 1 TB data transfer: Add ~$87 (data egress from Application Gateway)
- Multiple Application Gateways across regions: Multiply the savings ($100/month x number of gateways)

**Real savings example**:
- 3 Application Gateways (3 regions) = $300/month savings
- 5 Application Gateways (multi-region HA) = $500/month savings
- Over a year: $3,600 - $6,000 in savings

**Cost Optimization Tips**:
1. Use Front Door caching aggressively to reduce backend requests
2. Set Application Gateway autoscaling minimum to 0 for non-production environments
3. Monitor capacity unit usage and right-size your instances
4. Use Azure Cost Management alerts to monitor spending
5. Consider Azure Reservations for predictable workloads (up to 38% savings)

### 3. Latency - Optimized with Single WAF Inspection

**The Reality**: You're still adding hops, but fewer than the double-WAF approach.

Typical latency profile:
- User → Front Door Edge: 5-30ms (depending on user location)
- Front Door WAF Inspection: 5-15ms (ONLY one inspection)
- Front Door Edge → Front Door Backend: 10-50ms (routing overhead)
- Front Door → Application Gateway (Private Link): 2-10ms
- Application Gateway Routing (no WAF): 2-5ms
- Application Gateway → Backend: 5-20ms
- **Total added latency**: 29-130ms

**Compare to double-WAF approach**:
- Same as above PLUS Application Gateway WAF inspection: 10-30ms
- Total with double-WAF: 39-160ms
- **Latency savings: 10-30ms per request**

**Mitigations**:
1. Enable Front Door caching for static content (CDN capabilities)
2. Use HTTP/2 and connection pooling
3. Deploy Application Gateways in the same region as your backends
4. Monitor with Application Insights end-to-end transaction tracing
5. Optimize backend application response times

**Measurement**: Always establish baseline latency metrics BEFORE implementing this architecture, then measure the delta.

## Best Practices and Recommendations

After covering all the gotchas, here are my hard-won recommendations for this single-WAF architecture:

### 1. Start Simple, Add Complexity Gradually

Don't deploy this entire architecture on day one. Evolution path:

**Phase 1**: Application Gateway Standard_v2 only (2-4 weeks)
- Get comfortable with the infrastructure
- Establish baseline performance metrics
- Build operational runbooks
- No WAF protection yet (acceptable for internal testing)

**Phase 2**: Add Front Door without Private Link (2-4 weeks)
- Front Door → Application Gateway public endpoint
- Enable Front Door WAF (your first WAF layer)
- Restrict Application Gateway to accept only Front Door traffic via NSG
- Monitor costs and performance
- Tune WAF rules carefully

**Phase 3**: Enable Private Link (1-2 weeks)
- Convert to Private Link connections
- Remove public Application Gateway endpoints
- Validate security posture

### 2. Infrastructure as Code is Non-Negotiable

**Use**:
- Bicep/Terraform for infrastructure
- Azure DevOps/GitHub Actions for deployment pipelines
- Parameter files for environment-specific configurations
- Automated testing of deployments

**Version control structure**:
```
/infrastructure
  /bicep
    /modules          # Custom modules if needed
    /parameters
      parameters.dev.json
      parameters.staging.json
      parameters.prod.json
    appgateway-standard.bicep
    frontdoor-premium.bicep
    monitoring.bicep
    main.bicep       # Orchestration
  /scripts
    deploy-dev.sh
    deploy-prod.sh
  bicepconfig.json
```

### 3. Observability First

Before deploying to production:

**Must-have monitoring**:
1. Front Door WAF block rate and types (CRITICAL - only WAF layer)
2. Front Door WAF false positive detection
3. End-to-end latency tracking (user → backend)
4. Backend health status at both layers
5. Private Link connection status
6. Certificate expiration warnings
7. Cost tracking and budget alerts
8. Application Gateway routing health

**Recommended dashboards**:
```kusto
// WAF Protection Overview (Single Layer)
let timeRange = 1h;
AzureDiagnostics
| where TimeGenerated > ago(timeRange)
| where Category == "FrontdoorWebApplicationFirewallLog"
| summarize
    TotalRequests = count(),
    BlockedRequests = countif(action_s == "Block"),
    BlockRate = round(100.0 * countif(action_s == "Block") / count(), 2),
    TopBlockedRules = make_set_if(ruleName_s, action_s == "Block", 10)
  by bin(TimeGenerated, 5m)
| render timechart
```

### 4. Security Hardening Checklist

- [ ] Front Door WAF in Prevention mode (after thorough tuning)
- [ ] Front Door WAF policy includes all managed rule sets
- [ ] Custom WAF rules tested in Detection mode first
- [ ] Application Gateway accepts ONLY Front Door traffic (validate via NSG)
- [ ] Private Link enabled, public Application Gateway access disabled
- [ ] TLS 1.2 minimum enforced at all layers
- [ ] Managed identity used for Key Vault certificate access
- [ ] Diagnostic logs enabled for all resources
- [ ] Azure Policy enforcing Standard_v2 SKU on all Application Gateways
- [ ] Incident response runbook documented
- [ ] Emergency WAF bypass procedure documented
- [ ] Azure Firewall configured for internal traffic protection

### 5. WAF Policy Management for Single-Layer Architecture

**Critical best practices** (since this is your ONLY WAF):

1. **Comprehensive coverage is mandatory**:
   - Enable ALL relevant managed rule sets
   - Microsoft Default Rule Set 2.1 (OWASP)
   - Bot Manager Rule Set 1.0
   - Consider IP Reputation rule set if available

2. **Rigorous testing process**:
   - ALWAYS test new rules in Detection mode for 72 hours minimum
   - Analyze logs for false positives across all applications
   - Get sign-off from application teams before enabling Prevention mode
   - Have a rollback plan ready

3. **Application-specific exclusions**:
   - Document WHY each exclusion exists
   - Review exclusions quarterly (are they still needed?)
   - Minimize exclusions (each one reduces protection)

4. **Monitoring and alerting**:
   - Alert on WAF block rate > 10% (possible false positive)
   - Alert on WAF block rate < 0.1% (WAF might not be effective)
   - Weekly review of blocked requests (are they legitimate attacks?)
   - Monthly review of WAF effectiveness

5. **Emergency procedures**:
   ```bash
   # False positive storm - Switch to Detection mode
   az network front-door waf-policy update \
     --resource-group rg-centralized-waf \
     --name afd-xxxxwafpolicy \
     --mode Detection

   # Disable specific rule causing issues
   az network front-door waf-policy managed-rule-override add \
     --policy-name afd-xxxxwafpolicy \
     --resource-group rg-centralized-waf \
     --type Microsoft_DefaultRuleSet \
     --version 2.1 \
     --rule-id 942100 \
     --action Disabled
   ```

### 6. Internal Traffic Protection Strategy

Since internal traffic has no WAF protection, implement these compensating controls:

1. **Azure Firewall configuration**:
   - Enable threat intelligence-based filtering
   - Configure application FQDN rules
   - Implement strict network segmentation
   - Monitor and alert on unusual internal traffic patterns

2. **Application-level security**:
   - Implement input validation in all backend applications
   - Use parameterized queries (prevent SQL injection)
   - Enable CORS and validate origins
   - Implement rate limiting at the application level

3. **Network segmentation**:
   - Use NSGs to restrict traffic between subnets
   - Implement least-privilege access (only allow required ports/protocols)
   - Consider Azure Firewall Premium for TLS inspection if budget allows

4. **Monitoring**:
   - Monitor internal traffic patterns
   - Alert on unusual internal API calls
   - Regular security scanning of internal applications
   - Penetration testing of internal services

## Testing Your Implementation

Before declaring victory, run through these tests:

### Functional Testing

**1. Basic connectivity**:
```bash
# Test Front Door endpoint
curl -I https://your-frontdoor-endpoint.azurefd.net

# Should return 200 and route to backend via Application Gateway
```

**2. WAF blocking**:
```bash
# SQL injection attempt - should be blocked by Front Door WAF
curl "https://your-frontdoor-endpoint.azurefd.net/search?q=1' OR '1'='1"

# Expected: 403 Forbidden from Front Door WAF
```

**3. Geographic blocking**:
```bash
# Use a VPN/proxy from blocked country
# Expected: 403 Forbidden with custom block page
```

**4. Rate limiting**:
```bash
# Send requests exceeding rate limit
for i in {1..1100}; do curl -s https://your-frontdoor-endpoint.azurefd.net/ > /dev/null; done

# Expected: After threshold, 429 Too Many Requests
```

**5. Verify single WAF inspection** (performance test):
```bash
# Measure end-to-end latency
for i in {1..100}; do
  curl -w "Time: %{time_total}s\n" -o /dev/null -s https://your-frontdoor-endpoint.azurefd.net/
done | awk '{sum+=$2; count++} END {print "Average: " sum/count "s"}'

# Compare to baseline (should be faster than double-WAF)
```

## Real-World Example: E-Commerce Platform

Let me share a concrete example of how this architecture solved real problems for a fictional (but realistic) e-commerce company.

**Scenario**: GlobalRetail Corp
- Legacy .NET Framework web applications on Windows VMs (East US, West Europe)
- New microservices on Azure Container Apps (Southeast Asia)
- On-premises order management system (connected via ExpressRoute)
- 5 million requests/month
- Compliance requirements: PCI-DSS, GDPR
- Cost-conscious (mid-sized company)
- Small infrastructure team (2 people)

**Architecture**:
```
Azure Front Door Premium (ONLY WAF Layer)
├── Origin Group: Legacy Apps (via Private Link)
│   └── Application Gateway Standard_v2 East US
│       ├── VM Pool: Product Catalog (IIS on Windows Server 2019)
│       └── VM Pool: Customer Portal (.NET Framework 4.8)
│   └── Application Gateway Standard_v2 West Europe
│       └── VM Pool: Inventory Management
│
├── Origin Group: Modern Microservices
│   └── Container Apps: Checkout API
│   └── Container Apps: Recommendation Engine
│
└── Origin Group: Legacy Backend
    └── Application Gateway Standard_v2 East US
        └── ExpressRoute Connection
            └── On-prem Order Management System
```

**Results**:
1. **Security posture**:
   - All external traffic protected at Front Door edge
   - Single, centralized WAF policy for compliance audits
   - Consistent threat detection across all regions

2. **Cost savings**:
   - Using Standard_v2 instead of WAF_v2: $300/month (3 gateways)
   - Annual savings: $3,600
   - Reduced operational overhead with simplified management

3. **Performance**:
   - Single WAF inspection reduces latency by 10-30ms per request
   - Edge caching reduces backend load by 40%
   - Global Anycast routing improves user experience

4. **Operational efficiency**:
   - Small team can manage complex multi-region architecture
   - Infrastructure as Code enables rapid deployments
   - Centralized monitoring simplifies troubleshooting

## Alternative: When You SHOULD Use WAF on Application Gateway

This architecture isn't right for everyone. Consider using Application Gateway WAF_v2 instead of Standard_v2 if:

### Scenario 1: Zero-Trust Security Model

**Requirement**: No internal traffic should be trusted by default.

**Use Application Gateway WAF_v2** to inspect:
- VNet-to-VNet traffic between different business units
- On-premises-to-Azure traffic
- Internal API calls that handle sensitive data

**Cost impact**: +$100/month per Application Gateway
**Security benefit**: Full application-layer protection for all traffic

**Simple configuration change**:
```bicep
module appGateway 'br/public:avm/res/network/application-gateway:0.4.0' = {
  params: {
    sku: 'WAF_v2'  // Changed from Standard_v2
    tier: 'WAF_v2'
    // ... rest of config stays the same
  }
}
```

### Scenario 2: Highly Regulated Industries

**Industries**: Finance, healthcare, government, defense

**Compliance requirements** that may mandate internal WAF:
- PCI-DSS Level 1 (largest payment processors)
- HIPAA with strict interpretation
- FedRAMP High
- GDPR with internal personal data processing

**Use Application Gateway WAF_v2** to meet audit requirements.

### Scenario 3: Multi-Tenant Environments

**Requirement**: Different VNets or subscriptions serving different customers.

**Use Application Gateway WAF_v2** when:
- Different VNets may not trust each other
- Customer A's VNet should not have unfettered access to Customer B's services
- Internal traffic is essentially "untrusted"

### Scenario 4: Known Internal Threat Vectors

**Scenarios**:
- Previous insider threat incidents
- Contractors or third-parties with VNet access
- Shared development/production VNets (not recommended, but common)
- High-value targets (critical infrastructure)

**Use Application Gateway WAF_v2** for defense-in-depth.

## Wrapping Up

Building a centralized WAF strategy with Azure Front Door Premium as your single security layer, backed by Application Gateway Standard_v2 for regional load balancing, is a pragmatic, cost-effective pattern for many organizations.

**Key benefits of this architecture**:
- **Single WAF layer**: All external traffic protected at the edge with Front Door Premium
- **Cost savings**: $100/month per Application Gateway by using Standard_v2 instead of WAF_v2
- **Performance optimized**: Single WAF inspection reduces latency by 10-30ms per request
- **Centralized management**: One WAF policy to manage, monitor, and audit
- **Global + Regional**: Front Door handles global distribution, Application Gateway handles regional integration
- **Private Link security**: Secure backend connections without public exposure

**Deploy this architecture if**:
- You have multi-region deployments
- You're running hybrid IaaS + PaaS workloads
- You need centralized security management at the edge
- You want to optimize costs without compromising external security
- Your internal traffic originates from trusted sources

**Use Application Gateway WAF_v2 instead if**:
- Zero-trust security model (no internal traffic is trusted)
- Highly regulated industries with strict compliance requirements
- Multi-tenant environments with potentially adversarial internal traffic
- Known internal threat vectors or insider risk concerns

**Consider simpler alternatives if**:
- You're running pure PaaS applications (just use Front Door Premium with Private Link)
- You're single-region (Application Gateway Standard_v2 alone might be sufficient)
- Your team is very small and not familiar with Infrastructure as Code

The key is understanding your threat model, compliance requirements, and operational capacity. For most organizations, protecting all external traffic with a comprehensive Front Door WAF, while accepting network-level-only protection for internal traffic, is a sensible, defensible approach.

Remember: **Perfect security doesn't exist**. The goal is to implement security controls proportional to your actual risk. This architecture strikes that balance for many real-world scenarios.

Have you implemented a centralized WAF strategy in Azure? I'd love to hear about your experiences and lessons learned.

Stay secure, and may your infrastructure be as robust as your security posture!

---

**Additional Resources**:
- [Azure Front Door Premium Documentation](https://learn.microsoft.com/azure/frontdoor/)
- [Application Gateway v2 Best Practices](https://learn.microsoft.com/azure/well-architected/service-guides/azure-application-gateway)
- [Private Link with Application Gateway](https://learn.microsoft.com/azure/frontdoor/how-to-enable-private-link-application-gateway)
- [WAF Policy Management](https://learn.microsoft.com/azure/web-application-firewall/)
- [Azure Firewall vs WAF: When to Use Which](https://learn.microsoft.com/azure/architecture/guide/networking/firewall-application-gateway)
- [Application Gateway Standard_v2 vs WAF_v2 Comparison](https://learn.microsoft.com/azure/application-gateway/overview-v2)
