---
title: "Azure Application Gateway Now Supports TCP and TLS Termination - A Game Changer?"
date: 2025-11-28
categories:
  - azure
  - azure-infrastructure
  - networking
  - security
tags:
  - application-gateway
  - tcp
  - tls
  - load-balancing
  - bicep
  - networking
---
![Application Gateway Architecture Before TCP/TLS](/images/2025-12-01-headerduplicate.png)


Howdy Folks,

Big news from Microsoft! Azure Application Gateway has achieved general availability (GA) for **TCP and TLS protocol termination**. This is a significant enhancement that many of us have been waiting for. But what does this really mean, and is it the game changer we've been hoping for?

Let's dive in!

## What's New?

Azure Application Gateway has traditionally been a **Layer 7** (application layer) load balancer, handling HTTP, HTTPS, WebSockets, and HTTP/2 traffic. Now, with the GA release of TCP and TLS termination, Application Gateway can also function as a **Layer 4** (transport layer) proxy.

In simple terms, **Application Gateway can now support non-HTTP/HTTPS traffic!**

### What Does "Termination" Mean?

Application Gateway operates as a **terminating proxy**. Here's how it works:

1. **Client Connection**: A client establishes a TCP or TLS connection directly with Application Gateway using its frontend listener's IP address and port
2. **Gateway Termination**: Application Gateway terminates this incoming connection at the proxy
3. **New Backend Connection**: The gateway establishes a **separate new connection** with one of the backend servers selected by its distribution algorithm
4. **Request Forwarding**: The client's request is forwarded to the backend server through this new connection
5. **Response Handling**: The backend response is sent back to the client via Application Gateway

This differs from Azure Load Balancer, which is a **pass-through load balancer** where clients establish direct connections with backend servers. With Application Gateway, you get that extra layer of control and management capabilities.

## Architecture: Before and After

### Before: Limited to HTTP(S) Only

Previously, if you wanted to load balance non-HTTP traffic (like databases, custom TCP applications, or other protocols), you had to use:
- Azure Load Balancer for Layer 4 traffic
- Application Gateway for Layer 7 HTTP(S) traffic
- Separate firewall solutions for security

This meant multiple entry points and more complex architectures. Not ideal!

![Application Gateway Architecture Before TCP/TLS Support - Separate Load Balancers for HTTP and Non-HTTP Traffic](/images/2025-11-28-appgw-architecture-before-tcp-support.png)

### Now: Unified Gateway for All Traffic

Now, Application Gateway can serve as a **single endpoint** for:
- HTTP/HTTPS traffic (Layer 7)
- TCP traffic (Layer 4)
- TLS traffic (Layer 4)
- WebSockets
- HTTP/2

All through the **same frontend IP address**!

![Application Gateway Architecture After TCP/TLS Support - Unified Gateway for All Traffic Types](/images/2025-11-28-appgw-architecture-after-tcp-support.png)

## Key Capabilities

Let's talk about what this new feature brings to the table.

### 1. Hybrid Mode Support

You can now use a single Application Gateway instance to handle both HTTP and non-HTTP workloads simultaneously. Configure different listeners for different protocols, all using the same gateway resource.

**Use cases:**
- Front-end web traffic (HTTPS) + backend database connections (TCP/TLS)
- API Gateway (HTTPS) + message queue connections (TCP)
- Multiple services with different protocols behind one entry point

### 2. Flexible Backend Options

Your backends can be located anywhere:
- **Azure Resources**: VMs, VM Scale Sets, App Services, Event Hubs, SFTP services
- **On-Premises Servers**: Accessible via FQDN or IP addresses
- **Remote Services**: Any accessible TCP/TLS endpoint

This is huge for hybrid cloud scenarios!

### 3. Centralized TLS Certificate Management

With TLS termination support, you can:
- Offload TLS processing from backend servers
- Manage certificates centrally through Application Gateway
- Integrate with **Azure Key Vault** for secure certificate storage
- Use custom domains with your own certificates (even from private CAs!)
- Simplify compliance by managing certificates in one place

No more certificate sprawl across multiple servers.

### 4. Autoscaling

Application Gateway supports autoscaling up to **125 instances** for both Layer 7 and Layer 4 traffic, ensuring your infrastructure scales with demand.

### 5. Private Gateway Support

TCP and TLS proxy works with private-only Application Gateway deployments, enabling isolated environments with enhanced security for sensitive workloads.

## Is This a Game Changer?

### The Good News

**Yes, in many ways!** This feature allows you to:

1. **Simplify Architecture**: Use Application Gateway as the **single entry point** for all external traffic (both HTTP and non-HTTP)
2. **Reduce Costs**: Potentially consolidate multiple load balancers into one solution
3. **Centralize Management**: One place for routing, certificates, and backend health monitoring
4. **Hybrid Workloads**: Support modern and legacy applications through the same gateway
5. **Custom Domains**: Front any backend service with your custom domain name

### The Reality Check

**But here's the important caveat**: The WAF doesn't inspect TCP/TLS traffic.

> **Critical Limitation**: "A WAF v2 SKU gateway allows the creation of TLS or TCP listeners and backends to support HTTP and non-HTTP traffic through the same resource. However, it does not inspect traffic on TLS and TCP listeners for exploits and vulnerabilities."

**What this means:**
- WAF (Web Application Firewall) rules **only** protect HTTP(S) traffic
- TCP and TLS traffic passes through **without WAF inspection**
- Application Gateway provides routing and load balancing for TCP/TLS, not security inspection

**Security Options for TCP/TLS Traffic:**

Now, does this mean you **must** have Azure Firewall? Not necessarily! You have options:

1. **Network Security Groups (NSGs)**: You can use NSGs for basic Layer 3/Layer 4 security (IP-based filtering, port restrictions). This is often sufficient for many scenarios and is much more cost-effective.

2. **Azure Firewall**: Provides advanced features like threat intelligence, FQDN filtering, and centralized logging. You get more capabilities, but it comes at a higher cost.

3. **No Additional Firewall**: In some controlled environments (like private-only gateways with strict network segmentation), you might rely solely on Application Gateway + NSGs.

**The Trade-off:**
- NSGs give you basic Layer 3/4 protection (IP filtering, port control) - similar to what you'd get with traditional firewall rules
- Azure Firewall gives you advanced threat detection, deep packet inspection, and more sophisticated filtering
- You get **less features** with just NSGs compared to Azure Firewall, but for many workloads, that's perfectly fine!

So even though we can pass traffic through Application Gateway, it will only process the HTTP/HTTPS traffic using its WAF. The TCP/TLS traffic? It just goes through without any inspection. Choose your additional security layer based on your requirements and budget!

## Important Considerations

Before you jump in and start configuring TCP/TLS listeners, here are some things you need to know:

### 1. Connection Draining

- Default draining timeout: **30 seconds** (not user-configurable)
- Any configuration update (PUT operation) will terminate active connections after this timeout
- Plan your maintenance windows accordingly!

This is important - every time you make a configuration change, those active TCP connections will be dropped after 30 seconds. So be mindful when making changes in production.

### 2. AGIC Not Supported

Application Gateway Ingress Controller (AGIC) for Kubernetes **does not support** TCP/TLS proxy. AGIC works only with Layer 7 HTTP(S) listeners.

If you're running Kubernetes and using AGIC, this feature won't help you for non-HTTP workloads. Stick with HTTP(S) for AGIC scenarios.

### 3. SKU Requirements

TCP/TLS proxy is available only on:
- **Standard v2** SKU
- **WAF v2** SKU

Remember: On WAF v2, the firewall only protects HTTP(S) traffic, not TCP/TLS. You can use a WAF v2 SKU for this, but don't expect WAF protection on your TCP/TLS traffic.

## Configuration Overview

Let's look at how to configure TCP/TLS proxy on Application Gateway. I'll walk you through the components you need.

### Required Components

1. **Frontend Listener**
   - Protocol: TCP or TLS
   - Frontend IP: Public or private IPv4
   - Port: Application-specific (e.g., 22 for SFTP)
   - Priority: Required for routing rules

2. **Backend Pool**
   - Target type: IP address or FQDN
   - Backend servers: Azure VMs, on-premises servers, or any accessible endpoint

3. **Backend Settings**
   - Backend protocol: TCP or TLS
   - Backend port: Application-specific
   - Timeout: Configurable in seconds

4. **Routing Rule**
   - Links listener to backend pool
   - Connects backend settings
   - Requires priority value

### Example: SFTP Service Configuration

Here's a real-world scenario: load balancing SFTP traffic for secure file transfers. Let's say you have multiple SFTP servers and you want to load balance them using Application Gateway for high availability and centralized access.

**Listener Configuration:**
- Protocol: TCP
- Port: 22 (standard SFTP/SSH port)
- Frontend IP: Public or private

![Application Gateway TCP Listener Configuration for SFTP Port 22](/assets/img/2025-11-28-appgw-tcp-listener-config-port-22.png)

**Backend Settings:**
- Protocol: TCP
- Port: 22
- Timeout: 20 seconds

![Application Gateway Backend Setting Configuration for TCP SFTP Service](/assets/img/2025-11-28-appgw-backend-setting-tcp-sftp-config.png)

**Backend Pool:**
- SFTP Server VM IP addresses or FQDNs

**Routing Rule:**
- Priority: 100
- Links all components together

![Application Gateway Routing Rule Configuration for TCP Traffic](/images/2025-11-28-appgw-routing-rule-configuration.png)

NOTE -  YOU NEED TO SELECT TCP/TLS in the listener settings to get the settings enabled in the backend settings


For detailed step-by-step GUI configuration, refer to the [official Microsoft documentation](https://learn.microsoft.com/en-us/azure/application-gateway/how-to-tcp-tls-proxy).

## Infrastructure as Code: Bicep Template

Alright, now for the fun part! If you prefer to automate your deployments using infrastructure as code (and you should!), here's a working Bicep template to create an Application Gateway with TCP proxy support.

**Important Note**: This example uses native Bicep resources rather than Azure Verified Modules (AVM). Since the TCP/TLS proxy feature just reached GA, AVM support may still be maturing. Once you verify the latest AVM module version supports these new properties, you can migrate to AVM for cleaner, more maintainable code. Check the [AVM Application Gateway module](https://aka.ms/avm/res/network/applicationgateway) for updates.

This template creates an Application Gateway specifically configured for TCP traffic - perfect for scenarios like SFTP service load balancing.

```bicep

// Application Gateway with TCP proxy support
resource applicationGateway 'Microsoft.Network/applicationGateways@2023-11-01' = {
  name: applicationGatewayName
  location: location
  tags: {
    Environment: environment
    Purpose: 'TCP Proxy Gateway'
  }
  properties: {
    // SKU - Must be Standard_v2 or WAF_v2 for TCP/TLS support
    sku: {
      name: 'Standard_v2'
      tier: 'Standard_v2'
    }

    // Autoscaling configuration
    autoscaleConfiguration: {
      minCapacity: 2
      maxCapacity: 10
    }

    // Gateway IP configuration - connects Application Gateway to subnet
    gatewayIPConfigurations: [
      {
        name: 'appGatewayIpConfig'
        properties: {
          subnet: {
            id: subnet.id
          }
        }
      }
    ]

    // Frontend IP configuration - the public IP clients connect to
    frontendIPConfigurations: [
      {
        name: 'appGatewayFrontendIP'
        properties: {
          publicIPAddress: {
            id: publicIp.id
          }
        }
      }
    ]

    // Frontend port - the port clients connect to
    frontendPorts: [
      {
        name: 'tcpPort'
        properties: {
          port: tcpListenerPort
        }
      }
    ]

    // Backend address pool - your actual backend servers
    backendAddressPools: [
      {
        name: 'tcpBackendPool'
        properties: {
          backendAddresses: [for ip in backendServerIPs: {
            ipAddress: ip
          }]
        }
      }
    ]

    // NEW: Backend settings for TCP traffic
    // This is where you configure the TCP protocol and backend port
    backendSettingsCollection: [
      {
        name: 'tcpBackendSettings'
        properties: {
          port: backendTcpPort
          protocol: 'Tcp'  // This is the key! Use 'Tcp' or 'Tls'
          timeout: 60      // Connection timeout in seconds
        }
      }
    ]

    // NEW: TCP listener (Layer 4)
    // This replaces httpListeners for TCP/TLS traffic
    listeners: [
      {
        name: 'tcpListener'
        properties: {
          frontendIPConfiguration: {
            id: resourceId('Microsoft.Network/applicationGateways/frontendIPConfigurations', applicationGatewayName, 'appGatewayFrontendIP')
          }
          frontendPort: {
            id: resourceId('Microsoft.Network/applicationGateways/frontendPorts', applicationGatewayName, 'tcpPort')
          }
          protocol: 'Tcp'  // TCP or TLS protocol
        }
      }
    ]

    // NEW: Routing rules for TCP traffic
    // This replaces requestRoutingRules for TCP/TLS traffic
    routingRules: [
      {
        name: 'tcpRoutingRule'
        properties: {
          ruleType: 'Basic'
          priority: 100  // Priority is required for routing rules
          listener: {
            id: resourceId('Microsoft.Network/applicationGateways/listeners', applicationGatewayName, 'tcpListener')
          }
          backendAddressPool: {
            id: resourceId('Microsoft.Network/applicationGateways/backendAddressPools', applicationGatewayName, 'tcpBackendPool')
          }
          backendSettings: {
            id: resourceId('Microsoft.Network/applicationGateways/backendSettingsCollection', applicationGatewayName, 'tcpBackendSettings')
          }
        }
      }
    ]
  }
}

```

### Understanding the New TCP/TLS Properties

Let me highlight the key differences from traditional HTTP configuration:

**1. Backend Settings Collection** (new)
- Replaces `backendHttpSettingsCollection` for TCP/TLS traffic
- Uses `protocol: 'Tcp'` or `protocol: 'Tls'` instead of HTTP/HTTPS
- Simpler configuration - no cookie affinity, no request timeout (uses connection timeout instead)

**2. Listeners** (new)
- Replaces `httpListeners` for TCP/TLS traffic
- Protocol field accepts `Tcp` or `Tls`
- No hostname or requireServerNameIndication settings needed

**3. Routing Rules** (new)
- Replaces `requestRoutingRules` for TCP/TLS traffic
- Links TCP listeners to backend pools and settings
- Must include priority value (100-20000)

### Hybrid Mode: HTTP + TCP Together

Want to handle both HTTP and TCP traffic? You can combine both in one gateway:

```bicep
// Add HTTP-specific components alongside TCP
properties: {
  // ... existing TCP configuration ...

  // Add HTTP backend settings
      frontendPorts: [
      {
        name: 'port_22'
        properties: {
          port: 22
        }
      }
    ]
    backendAddressPools: [
      {
        name: applicationGateways_appgw_name
        properties: {
          backendAddresses: []
        }
      }
      {
        name: 'sftp'
        properties: {
          backendAddresses: []
        }
      }
    ]
    loadDistributionPolicies: []
    backendHttpSettingsCollection: []
    backendSettingsCollection: [
      {
        name: 'sftpSettings'
        properties: {
          port: 22
          protocol: 'Tcp'
          timeout: 20
        }
      }
    ]
    httpListeners: []
    listeners: [
      {
        name: 'test'
        id: '${applicationGateways_appgw_name_resource.id}/listeners/test'
        properties: {
          frontendIPConfiguration: {
            id: '${applicationGateways_appgw_name_resource.id}/frontendIPConfigurations/appGwPublicFrontendIpIPv4'
          }
          frontendPort: {
            id: '${applicationGateways_appgw_name_resource.id}/frontendPorts/port_22'
          }
          protocol: 'Tcp'
          hostNames: []
        }
      }
    ]
    urlPathMaps: []
    requestRoutingRules: []
    routingRules: [
      {
        name: 'test'
        properties: {
          ruleType: 'Basic'
          priority: 100
          listener: {
            id: '${applicationGateways_appgw_name_resource.id}/listeners/test'
          }
          backendAddressPool: {
            id: '${applicationGateways_appgw_name_resource.id}/backendAddressPools/sftp'
          }
          backendSettings: {
            id: '${applicationGateways_appgw_name_resource.id}/backendSettingsCollection/sftpSettings'
          }
        }
      }
    ]
```

Notice how HTTP uses `httpListeners` and `requestRoutingRules`, while TCP uses `listeners` and `routingRules`. They coexist peacefully in the same gateway!

### Testing Your TCP Gateway

Once deployed, test connectivity to your TCP service:

```bash
# Get the public IP
PUBLIC_IP=$(az network public-ip show \
  --resource-group rg-appgw-tcp \
  --name appgw-sftp-prod-pip \
  --query ipAddress \
  --output tsv)

# For SFTP, test with sftp client
sftp -P 22 username@$PUBLIC_IP

# For generic TCP testing, use telnet or nc
telnet $PUBLIC_IP 22
# or
nc -zv $PUBLIC_IP 22
```

### About Azure Verified Modules (AVM)

As TCP/TLS proxy support matures, the [Azure Verified Modules for Application Gateway](https://aka.ms/avm/res/network/applicationgateway) will likely add native support for these new properties. Check the module's GitHub repository for the latest version and TCP/TLS support status. Once available, you can refactor this template to use AVM for cleaner, more maintainable infrastructure as code.

## Use Cases and Scenarios

Let's talk about some real-world scenarios where this feature shines:

### 1. Secure File Transfer Services
Load balance SFTP servers for secure file transfers while maintaining centralized certificate management and high availability. This is ideal for enterprise file transfer solutions where multiple SFTP servers provide redundancy and scalability for external partners and customers.

### 2. Hybrid Application Architecture
Modern web applications (HTTPS) combined with legacy TCP-based services through a single gateway. This is perfect for those scenarios where you're modernizing but still need to support that old legacy app that runs on TCP.

### 3. Custom Protocol Applications
Applications using proprietary TCP or TLS protocols that previously couldn't leverage Application Gateway. Now you can bring them under the same umbrella.

### 4. Multi-Tier Applications
Front-end APIs (HTTP/HTTPS) and backend message queues, cache servers, or FTP/SFTP services (TCP/TLS) all accessible through one entry point, simplifying your overall architecture.

### 5. Cross-Premises Connectivity
Load balance traffic to on-premises servers or remote services using FQDN or IP addressing. Great for hybrid cloud scenarios.

## Comparison: Application Gateway vs. Load Balancer

Now you might be wondering, "Should I use Application Gateway or Azure Load Balancer for my TCP traffic?" Let me break it down:

| Feature | Application Gateway (TCP/TLS) | Azure Load Balancer |
|---------|------------------------------|---------------------|
| **Type** | Terminating Proxy | Pass-through |
| **Layer** | Layer 4 & Layer 7 | Layer 4 only |
| **Connection** | Separate frontend/backend connections | Direct client-to-backend |
| **Latency** | Moderate (proxy overhead) | Microsecond-level |
| **Throughput** | High (125 instances max) | Millions of flows |
| **Certificate Management** | Centralized, Key Vault integration | On backend servers |
| **Autoscaling** | Yes (2-125 instances) | N/A (always available) |
| **Custom Domains** | Yes | No |
| **Use Case** | Versatility, centralized management | Performance, simplicity |

**When to use Application Gateway:**
- You need centralized certificate management
- You want a single entry point for HTTP and non-HTTP traffic
- You need custom domain support
- You want autoscaling capabilities
- Management and versatility are priorities

**When to use Azure Load Balancer:**
- You need microsecond-level latency
- You need to handle millions of flows
- You want the simplest possible setup
- Performance is the top priority
- You don't need certificate management

## Best Practices

Based on my experience and the documentation, here are some best practices to follow:

### 1. Plan for Connection Draining
- Be aware of the 30-second default timeout
- Schedule configuration changes during maintenance windows
- Test connection handling before production deployment
- Consider the impact on long-running connections

### 2. Use Autoscaling
- Configure appropriate min/max instance counts
- Monitor metrics to tune autoscaling thresholds
- Start with at least 2 instances for high availability
- Be mindful of max instances to control costs

### 3. Leverage Azure Key Vault
- Store TLS certificates in Key Vault
- Use managed identities for Application Gateway to access certificates
- Implement certificate rotation policies
- Maintain proper certificate security practices

### 4. Implement Proper Monitoring
- Enable diagnostic logs
- Configure Azure Monitor alerts for health probe failures
- Track connection metrics and backend response times
- Set up dashboards for visibility

### 5. Security Considerations
- Remember: WAF does **not** protect TCP/TLS traffic (I can't stress this enough!)
- At minimum, use **Network Security Groups (NSGs)** for Layer 3/4 IP-based filtering
- Consider **Azure Firewall** if you need advanced threat protection, FQDN filtering, or centralized logging
- Implement proper network segmentation regardless of your firewall choice
- Use private endpoints where appropriate
- Don't assume Application Gateway gives you complete security - it's a load balancer, not a firewall!

### 6. Hybrid Mode Design
- Separate HTTP(S) and TCP/TLS workloads into different backend pools
- Use priority-based routing for complex scenarios
- Document your listener and routing rule configurations thoroughly
- Maintain organized configurations as hybrid mode can become complex

## Conclusion

The general availability of TCP and TLS termination on Azure Application Gateway is indeed a significant enhancement that brings several benefits to the table.

**Key Advantages:**
- Single entry point for all traffic types
- Centralized certificate and configuration management
- Support for hybrid workloads (HTTP + non-HTTP)
- Flexible backend options (Azure, on-premises, remote)
- Autoscaling for both Layer 4 and Layer 7 traffic

**Important Limitations:**
-  WAF protection applies only to HTTP(S) traffic
-  You need additional security for TCP/TLS traffic (NSGs at minimum, Azure Firewall for advanced features)
-  AGIC (Kubernetes Ingress) not supported for TCP/TLS
-  Fixed 30-second connection draining timeout

**So, is it a game changer?** 

For many scenarios, **yes**! This feature significantly simplifies architectures where you need to support both HTTP and non-HTTP workloads. However, it's not a complete replacement for Azure Firewall or other security solutions. Think of it as a **powerful addition to your toolbox** rather than a silver bullet.

The ability to use a single Application Gateway instance as a unified entry point for diverse protocols is valuable for:
- Cost optimization (consolidating multiple load balancers)
- Simplified management (one place for routing and certificates)
- Architectural flexibility (supporting legacy and modern apps together)

Just remember to complement it with appropriate security controls for comprehensive protection.

Overall, this is a welcome addition to Azure's networking capabilities, and I'm excited to see how it evolves. The fact that we can now front non-HTTP services with Application Gateway opens up a lot of interesting architectural possibilities.

## Additional Resources

Want to learn more? Check out these resources:

- [Azure Application Gateway TCP/TLS Proxy Overview](https://learn.microsoft.com/en-us/azure/application-gateway/tcp-tls-proxy-overview)
- [How to Configure TCP/TLS Proxy](https://learn.microsoft.com/en-us/azure/application-gateway/how-to-tcp-tls-proxy)
- [Azure Verified Modules for Application Gateway](https://aka.ms/avm/res/network/applicationgateway)
- [Application Gateway Documentation](https://learn.microsoft.com/en-us/azure/application-gateway/)

---

Have you started using TCP/TLS termination on Application Gateway? I'd love to hear about your use cases and experiences! Drop a comment or reach out - I'm always curious to see how folks are using these new features in the real world.
