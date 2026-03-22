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
  - "cloud-news"
---

![Azure Weekly Updates - Bicep Snapshot GA and Infrastructure Enhancements](/images/2026-03-08-azure-weekly-updates.png)

Howdy Folks,

Let me tell you about the Bicep snapshot command that just hit GA. If you've ever been in that awkward position where you're about to deploy infrastructure changes and someone asks "so... what exactly will this create?" - you know the pain. You squint at your Bicep code, mentally parse the conditionals, and hope your answer is correct. Well, those days are over.

This week's Azure updates bring some genuinely useful improvements that solve real problems. We've got Bicep snapshot going GA (finally!), Azure Firewall getting a much-needed draft mode, and a bunch of security and infrastructure updates that actually matter. Let's break it down.

## The Star of the Show: Bicep Snapshot Command is GA

Here's the thing - previewing what your infrastructure deployment will actually create has been a pain point forever. The Bicep team heard us, and with v0.41.2, the snapshot command has reached general availability.

What does this mean for you? You can now capture a complete deployment snapshot from your `.bicepparam` file before anything touches Azure. The command compiles and pre-expands your ARM template, showing you exactly what resources will be created, modified, or deleted.

What does this mean for you? You can now capture a complete deployment snapshot from your `.bicepparam` file before anything touches Azure. The command compiles and pre-expands your ARM template, showing you exactly what resources will be created, modified, or deleted.

```bash
# Basic snapshot capture
bicep snapshot main.bicepparam

# Validate against what's already in Azure
bicep snapshot main.bicepparam --mode validate

# Full context with subscription and resource group
bicep snapshot main.bicepparam --subscription-id <your-sub-id> --resource-group myRg --location westus --mode overwrite
```

The cool part is this solves multiple problems at once. Doing infrastructure reviews? Export the snapshot and show exactly what changes. Need approval before deployment? Generate a snapshot and send it for review. Trying to debug why something isn't deploying right? Compare snapshots between versions.

## Azure Firewall Finally Gets Draft Mode

If you've ever had to modify firewall rules in production and felt that little knot of anxiety in your stomach, [Azure Firewall's new Draft & Deploy feature](https://azure.microsoft.com/en-au/updates/generally-available-azure-firewall-draft-deploy/) is for you.

The feature is exactly what you'd hope - work on your firewall rule changes in a draft state, test them, validate them, and only then push them live. No more "test in prod" moments with your firewall configuration. This reached GA this week, so it's ready for production use right now.

The feature is exactly what you'd hope - work on your firewall rule changes in a draft state, test them, validate them, and only then push them live. No more "test in prod" moments with your firewall configuration. This reached GA this week, so it's ready for production use right now.

## Databricks Gets Some Love

Two updates hit GA for Azure Databricks this week. First up is [Databricks Lakebase](https://azure.microsoft.com/en-au/updates/generally-available-azure-databricks-lakebase/), which brings new capabilities for managing your lakehouse architecture. If you're running a data lakehouse on Databricks, this gives you better control over how you organize and govern your data.

The second is the ability to [update workspace network configuration](https://azure.microsoft.com/en-au/updates/generally-available-azure-databricks-update-workspace-network-configuration/). This might sound boring, but if you've ever tried to modify network settings on an existing Databricks workspace and hit limitations, you'll appreciate this one. More flexibility in how you configure networking after the fact is always welcome.

## .NET 10 Comes to Azure Functions

[Azure Functions now supports .NET 10](https://azure.microsoft.com/en-au/updates/generally-available-azure-functions-net-10-support/), which is great news if you're running serverless .NET workloads. You get all the performance improvements and language features from .NET 10, plus Microsoft released [troubleshooting tools for Flex Consumption](https://azure.microsoft.com/en-au/updates/generally-available-quota-and-deployment-troubleshooting-tools-for-azure-functions-flex-consumption/) alongside it.

These troubleshooting tools are actually pretty useful - they help you diagnose quota issues and deployment problems faster, which means less time staring at cryptic error messages wondering what went wrong.

## Confidential Computing Expands

Four new confidential VM series are now widely available - [DCesv6, DCedsv6, ECesv6, and ECedsv6](https://azure.microsoft.com/en-au/updates/generally-available-dcesv6-dcedsv6-ecesv6-and-eces/). These VMs provide hardware-based encryption for data in use, not just at rest or in transit.

The practical impact? If you're handling sensitive workloads - healthcare data, financial transactions, anything covered by strict compliance requirements - these VMs give you hardware-level protection that doesn't require you to trust the hypervisor. The DCe series uses AMD tech, the ECe series uses Intel. Pick whichever fits your requirements.

The practical impact? If you're handling sensitive workloads - healthcare data, financial transactions, anything covered by strict compliance requirements - these VMs give you hardware-level protection that doesn't require you to trust the hypervisor. The DCe series uses AMD tech, the ECe series uses Intel. Pick whichever fits your requirements.

## Storage Security Gets Tighter

Azure Blob Storage has a new preview feature that lets you [restrict user delegation SAS tokens to specific Entra ID identities](https://azure.microsoft.com/en-au/updates/public-preview-restrict-usage-of-user-delegation-sas-to-an-entra-id-identity/). Here's where this gets interesting - it's not just about creating a SAS token anymore. You can now ensure that token can only be used by the exact identity you specify.

This closes a security gap where a SAS token could theoretically be used by anyone who got their hands on it. Now you can tie it to a specific Entra ID identity, adding another layer of protection.

## Premium SSD v2 Global Expansion

If you're using Premium SSD v2 (and you should be for high-performance workloads), it's now available in more regions:
- [Third availability zone in New Zealand North](https://azure.microsoft.com/en-au/updates/generally-available-azure-premium-ssd-v2-disk-storage-is-now-available-in-a-third-availability-zone-in-new-zealand-north/)
- [Brazil Southeast](https://azure.microsoft.com/en-au/updates/generally-available-azure-premium-ssd-v2-disk-is-now-available-in-brazil-southeast-and-in-a-third-availability-zone-in-malaysia-west-and-indonesia-central/)
- [Third availability zone in Malaysia West and Indonesia Central](https://azure.microsoft.com/en-au/updates/generally-available-azure-premium-ssd-v2-disk-is-now-available-in-brazil-southeast-and-in-a-third-availability-zone-in-malaysia-west-and-indonesia-central/)

Premium SSD v2 is the real deal for demanding database and analytics workloads - low latency, high IOPS, and you can adjust performance without downtime.

Speaking of databases, Azure Database for PostgreSQL now offers [geo-redundant backups for Premium SSD v2 in preview](https://azure.microsoft.com/en-au/updates/public-preview-georedundant-backups-for-premium-ssd-v2-in-azure-database-for-postgresql/). Your backups get replicated to a secondary region automatically, which is exactly what you want for disaster recovery scenarios.

Speaking of databases, Azure Database for PostgreSQL now offers [geo-redundant backups for Premium SSD v2 in preview](https://azure.microsoft.com/en-au/updates/public-preview-georedundant-backups-for-premium-ssd-v2-in-azure-database-for-postgresql/). Your backups get replicated to a secondary region automatically, which is exactly what you want for disaster recovery scenarios.

## AKS Gets AI-Powered Assistance

Two preview features landed for Azure Kubernetes Service that lean into the AI tooling trend. First is [cluster mode for the agentic CLI](https://azure.microsoft.com/en-au/updates/public-preview-cluster-mode-for-the-agentic-cli-for-aks/), which brings AI-powered assistance to cluster management. Second is [unified tooling in the AKS MCP server](https://azure.microsoft.com/en-au/updates/public-preview-unified-tooling-in-the-aks-mcp-server/), adding enhanced management capabilities through the Model Context Protocol.

These are both preview features, so treat them as experimental. But if you're managing Kubernetes clusters and want to see where AI-assisted operations are heading, worth checking out.

## Heads Up: NGINX Ingress Is Going Away

If you're using the [Managed NGINX Ingress with Application Routing Add-on, it's being retired in November 2026](https://azure.microsoft.com/en-au/updates/retirement-managed-nginx-ingress-with-application-routing-addon-retiring-november-2026/). You've got time, but start planning your migration to alternative ingress solutions. Don't be that person scrambling in October.

## Monitoring and WAF Updates

Application Gateway got a new preview feature - [WAF Insights](https://azure.microsoft.com/en-au/updates/public-preview-waf-insights-for-application-gateway/). This gives you deeper visibility into what your Web Application Firewall is actually seeing and blocking. Threat patterns, security events, the works. If you're running Application Gateway WAF, this helps you understand what's happening at the edge.

Azure Monitor also has a [preview for secure ingestion and pod placement](https://azure.microsoft.com/en-au/updates/public-preview-secure-ingestion-and-pod-placement-for-azure-monitor-pipeline/). More control over where and how monitoring data gets collected and transmitted, which matters if you've got strict security or compliance requirements around telemetry data.

Azure Monitor also has a [preview for secure ingestion and pod placement](https://azure.microsoft.com/en-au/updates/public-preview-secure-ingestion-and-pod-placement-for-azure-monitor-pipeline/). More control over where and how monitoring data gets collected and transmitted, which matters if you've got strict security or compliance requirements around telemetry data.

## Deep Dive: Bicep v0.41.2

Let's talk more about what's in this Bicep release, because there's more than just the snapshot command.

The snapshot feature is the headline act, but the release also adds MCP server metadata to the NuGet package. If you're building tooling around Bicep, this makes integration easier. They've also added extension namespace functions, opening up new capabilities for Bicep extensions.

There's an experimental Visualizer V2 in the works too. It's experimental, so don't rely on it for production workflows yet, but it shows where the team is heading with visual representation of infrastructure.

On the bug fix side, they sorted out an issue with nested extendable params spread - inherited spread expressions now bind correctly. Array splat completion in type syntax got better. Completions for `#disable-diagnostics` and `#restore-diagnostics` work properly now.

Community shoutout to [@verschaevesiebe](https://github.com/verschaevesiebe) and [@gerbermarco](https://github.com/gerbermarco) for contributions to the snapshot command docs. Open source contributions matter, especially for documentation.

**Why you should try the snapshot command:**

If you're doing infrastructure reviews, this is a game-changer. Generate a snapshot, export it, and show exactly what will change. Need approval before deploying to production? Snapshot makes that conversation much easier.

Troubleshooting deployment issues? Compare snapshots between different versions of your code. See exactly what changed and why your deployment might be failing.

Upgrade to Bicep v0.41.2:
```bash
az bicep upgrade
```

Upgrade to Bicep v0.41.2:
```bash
az bicep upgrade
```

## Regional Expansion News

[Azure Red Hat OpenShift is now available in Malaysia West, New Zealand North, and Mexico Central](https://azure.microsoft.com/en-au/updates/generally-available-azure-red-hat-openshift-is-now-available-in-malaysia-west-new-zealand-north-and-mexico-central/). If you're running OpenShift workloads and need coverage in APAC or Latin America, these new regions give you options closer to your users.

## Retirements to Watch

A few things are being retired that you should know about:

**April 2026:** [Azure Policy faster enforcement and login/logout workaround](https://azure.microsoft.com/en-au/updates/retirement-azure-policy-faster-enforcement-and-retirement-of-loginlogout-workaround/) - The temporary workaround is going away as the proper implementation is now in place.

**May 2026:** [Windows Server Annual Channel (preview)](https://azure.microsoft.com/en-au/updates/retirement-windows-server-annual-channel-preview/) - If you're using this, plan your migration.

**November 2026:** Managed NGINX Ingress with Application Routing Add-on (mentioned earlier, but worth repeating).

## What's Next

The trend lines are pretty clear from this week's updates. Confidential computing is expanding - expect more VM series and regions. MCP (Model Context Protocol) is showing up in multiple services, which suggests Microsoft is committed to that integration pattern. Bicep continues to mature with features that solve real operational problems.

Security capabilities keep getting more granular - the SAS token restrictions for Blob Storage are a good example of making security controls more precise rather than just adding more checkboxes.

## Wrapping Up

The Bicep snapshot command going GA is genuinely useful - it solves a real problem that everyone doing infrastructure as code has faced. Azure Firewall's draft mode is another example of adding features that match how people actually work.

Not every update is sexy, but the Premium SSD v2 expansion, .NET 10 support for Functions, and security improvements are the kind of steady progress that makes the platform better to work with.

Are you planning to use the Bicep snapshot command? Have you been waiting for Azure Firewall draft mode? Let me know what you think about this week's updates.

Until next week, happy building!

---

**Useful Links:**
- [Azure Updates Portal](https://azure.microsoft.com/en-au/updates)
- [Bicep v0.41.2 Release Notes](https://github.com/Azure/bicep/releases/tag/v0.41.2)