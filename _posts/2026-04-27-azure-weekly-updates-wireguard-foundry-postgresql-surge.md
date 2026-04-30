---
title: "Azure Weekly Updates - Week of April 27, 2026"
date: 2026-04-27
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "bicep"
  - "cloud-news"
  - "aks"
  - "foundry"
  - "postgresql"
---

Howdy Folks,

Let me set the scene. It is Friday afternoon, your coffee is cold, and you are trying to decide whether this is the week you finally clean up that backlog of "we should really modernize this" tasks. Then Azure drops a wave of updates that basically says, "Cool, we already started for you." AKS encryption gets stronger, Foundry gets more practical, PostgreSQL gets a serious scaling glow-up, and monitoring keeps marching toward cleaner, more standard pipelines.

This week was one of those weeks where the individual updates look small on paper, but together they quietly change how fast you can ship.

## Highlight of the Week: AKS WireGuard Is Now GA

If you have ever had to explain east-west traffic encryption in Kubernetes to a security reviewer, you know the pain. It usually starts technical and ends with a whiteboard that looks like modern art.

The big headline this week is that **WireGuard in-transit encryption for AKS is generally available**.

- [Generally Available: WireGuard In-Transit Encryption for AKS](https://azure.microsoft.com/updates?id=560015)

This means AKS clusters using Azure CNI powered by Cilium and ACNS can now get node-level in-transit encryption with WireGuard in a first-class way. The cool part is not just security posture. It is operational confidence. You can now raise your network security baseline without inventing your own encryption story on top.

If you run sensitive workloads or deal with strict compliance controls, this one is immediately actionable.

## New Services and Features Worth Your Attention

### Foundry steps into daily developer workflow

I really liked this pair because it moves Foundry from "interesting" to "I can actually use this in my day-to-day tooling."

- [Generally Available: Foundry Toolkit for Visual Studio Code](https://azure.microsoft.com/updates?id=560987)
- [Public Preview: Hosted Agents in Foundry Agent Service](https://azure.microsoft.com/updates?id=560997)

The Toolkit GA gives you a cleaner path to create and debug agent apps directly in VS Code. The hosted agents preview gives you isolated execution sandboxes per session, which is exactly what you want when you start saying phrases like "production agents" with a straight face.

This means you can now prototype and operationalize with less glue code and fewer "we will secure that later" compromises.

### PostgreSQL got a stacked release week

Honestly, PostgreSQL teams got spoiled this week.

- [Generally Available: Cascading read replicas in Azure Database for PostgreSQL](https://azure.microsoft.com/updates?id=560939)
- [Generally Available: Premium SSD v2 for Azure Database for PostgreSQL](https://azure.microsoft.com/updates?id=560336)
- [Generally Available: Enhanced Mirroring for Azure Database for PostgreSQL in Microsoft Fabric](https://azure.microsoft.com/updates?id=560293)
- [Generally Available: Azure Database for PostgreSQL flexible server in Denmark East](https://azure.microsoft.com/updates?id=560288)

If you have ever struggled with read-heavy traffic patterns, replica topology limitations, or balancing cost versus IOPS, this is the kind of week that gives you options.

Cascading replicas gives you more flexibility for read scale strategy. Premium SSD v2 gives you better performance tuning headroom. Enhanced mirroring to Fabric helps analytics teams stop asking for nightly exports like it is 2014. And a new region availability is always meaningful when your architecture includes residency, latency, or both.

### Azure Monitor pipeline is now GA

This one deserves more love than it gets in announcements.

- [Generally Available: Azure Monitor pipeline](https://azure.microsoft.com/updates?id=559886)

Centralized telemetry ingestion and transformation sounds boring until you are the one managing ten different data paths, three compliance requirements, and two teams arguing about schema consistency.

This means you can now build a cleaner observability backbone without duct-taping ingest logic in five places.

### Arc-enabled Kubernetes monitoring for OpenShift and ARO

Hybrid and multicloud Kubernetes teams got a practical win too.

- [Generally Available: Azure Monitor for Azure Arc-enabled Kubernetes with OpenShift and Azure Red Hat OpenShift](https://azure.microsoft.com/updates?id=560358)

If you run mixed estates, consistency matters more than flashy dashboards. This update makes it easier to monitor OpenShift and ARO environments through a more unified Azure Monitor story.

Translation: less dashboard juggling, faster troubleshooting.

## Preview Updates That Could Become Big Deals

### Backup and storage: quietly important improvements

- [Public Preview: Azure Backup for Elastic SAN](https://azure.microsoft.com/updates?id=560904)
- [Generally Available: CRC Protection for Azure Elastic SAN](https://azure.microsoft.com/updates?id=560889)
- [Generally Available: Capacity Autoscaling for Azure Elastic SAN](https://azure.microsoft.com/updates?id=560919)

If your storage footprint keeps growing, these are exactly the quality-of-life updates you want. Backup support improves recoverability posture. CRC protection improves integrity controls. Autoscaling reduces overprovisioning guesswork.

No hype needed. This is practical platform maturity.

### Azure Arc migration and PostgreSQL networking flexibility

- [Public Preview: Azure Arc adds SQL Server on Azure Virtual Machines as a migration target](https://azure.microsoft.com/updates?id=560805)
- [Public Preview: Migrating from virtual network-integrated to Private Endpoint-capable network configuration for Azure Database for PostgreSQL](https://azure.microsoft.com/updates?id=560298)
- [Public Preview: Logical replication slot sync status metric for Azure Database for PostgreSQL Flexible Server](https://azure.microsoft.com/updates?id=513249)

Here is where it gets interesting. These updates reduce migration friction and improve operational visibility, which is usually where migrations get messy.

If you have ever been blocked by network model choices made two years ago, this PostgreSQL networking preview could save you a lot of unpleasant architecture meetings.

### Security and governance picks

- [Generally Available: Dynamic data masking with Azure Cosmos DB](https://azure.microsoft.com/updates?id=559633)
- [Generally Available: Azure NetApp Files advanced ransomware protection](https://azure.microsoft.com/updates?id=560188)
- [Public Preview: Azure Monitor supports native OTLP ingestion using the Azure Monitor Agent](https://azure.microsoft.com/updates?id=560530)

Dynamic masking is one of those controls teams ask for after an audit finding, so having it GA in Cosmos DB is a solid step. ANF ransomware protection being GA is good timing for anyone hardening storage. And OTLP ingestion preview signals the standards-based observability path is getting stronger.

If your stack is already OpenTelemetry-heavy, watch that OTLP update closely.

## Breaking Changes and Deprecations You Should Not Ignore

One announcement this week is a future-dated event, but you should still plan now.

- [Retirement: Support for .NET 8 (LTS) ends on November 10, 2026 - upgrade your apps to .NET 10 (LTS)](https://azure.microsoft.com/updates?id=558033)

This is the classic "future me problem" that becomes current-you pain if you ignore it. If you have App Service workloads pinned to .NET 8, put the upgrade motion on your roadmap now while you can do it calmly.

## Bicep Corner

No new Bicep release landed in this specific weekly window, so we are still riding the latest stable release:

- [Bicep v0.42.1 release notes](https://github.com/Azure/bicep/releases/tag/v0.42.1)

If you skipped it earlier this month, it is worth catching up for:

- `bicep console` now being GA
- The new `roleDefinitions()` helper for cleaner RBAC templates

If you have ever hardcoded role GUIDs and felt slightly ashamed, this release was made for you.

## What Is Coming Next

If this week is any indicator, next week will likely continue three themes:

1. More practical AI platform hardening around Foundry and agent runtime safety.
2. Continued PostgreSQL velocity around performance, migration, and enterprise operations.
3. More standardization in observability with Azure Monitor and OTLP-centered workflows.

I will be watching those three closely, especially anything that reduces platform complexity for teams running hybrid estates.

## Wrapping Up

This week felt like Azure engineering teams were in "remove friction" mode, and I am all for it. We got stronger AKS network security, more usable Foundry building blocks, a very healthy PostgreSQL batch, and observability improvements that move us closer to sane, standardized telemetry pipelines.

If you only pick one thing to test this week, make it WireGuard on AKS if security is your concern, or cascading replicas in PostgreSQL if your bottleneck is reads.

Which one are you planning to try first in your environment?
