---
title: "Azure Weekly Updates - Week of March 8, 2026"
date: 2026-03-08
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "bicep"
  - "azure-friday"
  - "cloud-news"
---

![Azure Weekly Updates - Bicep Snapshot GA and Infrastructure Enhancements](/assets/img/posts/2026-03-08-azure-weekly-updates-bicep-snapshot-ga-azure-firewall-enhancements.jpg)

Howdy Folks,

Welcome to another exciting week of Azure updates! This week brings some fantastic news from the Azure ecosystem, with several general availability announcements and a major milestone for Bicep users. Let's dive into what's been happening in the Azure world this past week.

## Highlight of the Week: Bicep Snapshot Command Goes GA!

The big news this week is that the **Bicep snapshot command has officially reached General Availability** with the release of Bicep v0.41.2! If you've been testing infrastructure changes and wondering "what will actually get deployed?", this feature is about to become your new best friend.

The snapshot command captures a deployment snapshot from a `.bicepparam` file by compiling and pre-expanding the ARM template, allowing you to preview predicted resources and perform semantic diffs between Bicep implementations.

```bash
# Capture a snapshot
bicep snapshot main.bicepparam

# Validate a snapshot
bicep snapshot main.bicepparam --mode validate

# Capture with Azure context
bicep snapshot main.bicepparam --subscription-id <sub-id> --resource-group myRg --location westus --mode overwrite
```

This is huge for anyone doing infrastructure as code reviews or wanting to validate changes before deployment. Check out the [YouTube demo](https://www.youtube.com/watch?v=84jVnQI-0Ak) to see it in action!

## New Services & Features

### Azure Firewall Gets Draft & Deploy (GA)
Azure Firewall now supports **Draft & Deploy** capabilities in general availability. This feature lets you work on firewall rule changes in a draft state before pushing them live - perfect for testing and validation workflows without impacting production traffic.

[Learn more about Azure Firewall Draft & Deploy](https://azure.microsoft.com/en-au/updates)

### Azure Databricks Enhancements
Two significant updates hit GA this week for Azure Databricks:
- **Lakebase** - A new capability for managing your lakehouse architecture
- **Update workspace network configuration** - Enhanced networking controls for your Databricks workspaces

These updates give you more control and flexibility in managing your data analytics environments.

### Azure Functions .NET 10 Support (GA)
Azure Functions now officially supports **.NET 10**, bringing the latest .NET capabilities to your serverless functions. This includes improved performance, new language features, and enhanced developer experience.

Along with this, Microsoft released **quota and deployment troubleshooting tools for Azure Functions Flex Consumption** to help you diagnose and resolve deployment issues faster.

[Check out Azure Functions .NET 10 support](https://azure.microsoft.com/en-au/updates)

## Security & Confidential Computing

### New Confidential VM Series Available
Four new confidential VM series reached GA in February and are now widely available:
- **DCesv6** and **DCedsv6** (AMD-based)
- **ECesv6** and **ECedsv6** (Intel-based)

These VMs provide hardware-based encryption and isolation for your most sensitive workloads, protecting data in use, at rest, and in transit.

### Restrict User Delegation SAS to Entra ID Identity (Preview)
A new preview feature for Azure Blob Storage allows you to **restrict usage of user delegation SAS tokens to specific Entra ID identities**. This adds an extra layer of security by ensuring SAS tokens can only be used by authorized identities, reducing the risk of token misuse.

## Storage & Data Services

### Azure Premium SSD v2 Expansion
Azure Premium SSD v2 continues its global rollout:
- Now available in a **third Availability Zone in New Zealand North**
- Available in **Brazil Southeast**
- Available in a **third Availability Zone in Malaysia West and Indonesia Central**

Premium SSD v2 offers the highest performance Azure disk storage with low latency and high IOPS - perfect for demanding database and analytics workloads.

### Geo-Redundant Backups for Azure Database for PostgreSQL (Preview)
Azure Database for PostgreSQL now offers **geo-redundant backups for Premium SSD v2** in preview. This ensures your database backups are replicated to a secondary region for enhanced disaster recovery capabilities.

## Kubernetes & Container Updates

### AKS Gets Agentic CLI and MCP Server Tools (Preview)
Two exciting preview features for Azure Kubernetes Service:
- **Cluster mode for the agentic CLI** - Simplifies cluster management with AI-powered assistance
- **Unified tooling in the AKS MCP server** - Enhanced management capabilities through the Model Context Protocol

These features bring modern AI-assisted operations to your Kubernetes clusters.

### NGINX Ingress Retirement Notice
If you're using the Managed NGINX Ingress with Application Routing Add-on, take note: it's scheduled for retirement in **November 2026**. Start planning your migration to alternative ingress solutions.

## Monitoring & Security

### WAF Insights for Application Gateway (Preview)
A new preview feature brings **WAF Insights for Application Gateway**, providing deeper visibility into Web Application Firewall activity, threat patterns, and security events. This helps you better understand and respond to security threats targeting your applications.

### Secure Ingestion for Azure Monitor Pipeline (Preview)
Azure Monitor now offers **secure ingestion and pod placement for Azure Monitor pipeline** in preview, giving you more control over where and how monitoring data is collected and transmitted.

## Bicep Corner

### Bicep v0.41.2 - The Snapshot Release

As mentioned in our highlight, Bicep v0.41.2 landed last week with snapshot command GA and several other goodies:

**Key Features:**
- **Snapshot command is GA** - Preview deployments before they happen
- **MCP server metadata JSON file** added to NuGet package for better tooling integration
- **Extension namespace functions** - New capabilities for Bicep extensions
- **Experimental Visualizer V2** - Enhanced visual representation of your infrastructure

**Bug Fixes:**
- Fixed nested extendable params spread to ensure inherited spread expressions are bound correctly
- Added support for array splat completion in type syntax
- Improved completions for `#disable-diagnostics` and `#restore-diagnostics`
- Enhanced file handle URI in output

**Community Contributions:**
Special thanks to [@verschaevesiebe](https://github.com/verschaevesiebe) and [@gerbermarco](https://github.com/gerbermarco) for their contributions to snapshot command documentation and README improvements!

### Want to Try the Snapshot Command?

The snapshot command is perfect for:
- **Pre-deployment validation** - See what will be created before you deploy
- **Diff analysis** - Compare infrastructure changes between versions
- **Compliance reviews** - Export deployment plans for approval workflows
- **Troubleshooting** - Understand exactly what's being deployed

Get started by upgrading to Bicep v0.41.2:
```bash
az bicep upgrade
```

## Regional Expansion

### Azure Red Hat OpenShift Goes Global
Azure Red Hat OpenShift is now available in three new regions:
- **Malaysia West**
- **New Zealand North**  
- **Mexico Central**

This expansion brings enterprise-grade Kubernetes closer to customers in APAC and Latin America.

## Upcoming Retirements

Mark your calendars for these upcoming deprecations:

**April 2026:**
- Azure Policy faster enforcement and retirement of login/logout workaround

**May 2026:**
- Windows Server Annual Channel (preview)

**November 2026:**
- Managed NGINX Ingress with Application Routing Add-on

Make sure to review these and plan your migrations accordingly!

## Azure Friday Note

Unfortunately, we couldn't access the latest Azure Friday videos this week due to technical limitations, but you can always catch up on the latest episodes at the [Azure Friday playlist](https://www.youtube.com/playlist?list=PLlVtbbG169nGL0hj1CeL2Zjmr73SmXIpc). The Azure Friday team consistently delivers great content on the latest Azure features and best practices.

## What's Coming Next

Keep an eye on these developing trends:
- Continued expansion of confidential computing VMs
- More MCP server integrations across Azure services
- Enhanced Bicep debugging and visualization tools
- Security enhancements across the board with Entra ID integration

## Wrapping Up

This week showcased Microsoft's commitment to both innovation (new Bicep snapshot capabilities, agentic CLI tools) and operational excellence (enhanced security features, global expansion). The Bicep snapshot command going GA is particularly exciting for infrastructure teams who want better visibility and control over their deployments.

What update are you most excited about? Are you planning to use the new snapshot command? Let me know in the comments or reach out on social media!

Until next week, happy building in Azure!

---

*Want to stay updated on Azure news? Subscribe to this blog and get weekly Azure updates delivered straight to your inbox. Follow me on [Twitter/X](#) for real-time Azure tips and discussions.*

**Useful Links:**
- [Azure Updates Portal](https://azure.microsoft.com/en-au/updates)
- [Bicep Releases on GitHub](https://github.com/Azure/bicep/releases)
- [Azure Friday YouTube Playlist](https://www.youtube.com/playlist?list=PLlVtbbG169nGL0hj1CeL2Zjmr73SmXIpc)
- [Bicep Snapshot Command Documentation](https://github.com/Azure/bicep/blob/main/docs/experimental/snapshot-command.md)