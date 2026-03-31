---
title: "Azure Weekly Updates - Week of March 30, 2026"
date: 2026-03-30
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "bicep"
  - "cloud-news"
  - "aks"
  - "postgresql"
  - "opentelemetry"
---

Howdy Folks,

Let me tell you about a week where the Azure Kubernetes Service team apparently decided to ship everything they'd been working on all at once. If you're running containers on Azure, you might want to sit down for this one - we've got new networking features, observability upgrades, GPU metrics, a container networking AI agent, and an entirely new application networking layer. Oh, and the PostgreSQL team wasn't sitting idle either, opening the migration doors to Google AlloyDB and EDB workloads.

This was a week that screamed "Kubernetes-first" from every angle, with a side helping of database goodness. Let's dig in.

## AKS Networking Gets a Complete Overhaul

Here's the thing about Kubernetes networking - it's already complicated enough without having to manage it across multiple clusters, debug it without proper tooling, and explain it to your team without a whiteboard. Microsoft apparently agreed, because this week they dropped a whole suite of networking features for AKS.

**Container network metrics filtering** is now [generally available](https://azure.microsoft.com/updates?id=557902). If you've been running ACNS (Advanced Container Networking Services) and drowning in metrics you don't care about, you can now filter what gets collected. Network observability generates a lot of data, and not all of it is operationally relevant. This lets operators focus on what matters instead of paying to store metrics for traffic patterns nobody looks at.

**Container network logs** also hit [general availability](https://azure.microsoft.com/updates?id=557892). Diagnosing networking issues in Kubernetes has always been painful because of limited visibility into traffic flows. Now you get proper connection-level logs that show what's happening with your pod-to-pod and pod-to-external traffic. When something breaks at 2am, you'll actually have the data to figure out why.

And if you want someone - or rather, something - to help you diagnose those network issues, there's a new [AI Agent for container networking troubleshooting](https://azure.microsoft.com/updates?id=557887) in preview. It provides a lightweight web-based interface that correlates logs and metrics scattered across multiple tools, so you don't have to manually piece together signals during an incident. Think of it as an SRE assistant that never gets tired of looking at packet traces.

## Cross-Cluster and Application-Layer Networking

The networking updates didn't stop at individual clusters. **Cross-cluster networking in Azure Kubernetes Fleet Manager** is now in [public preview](https://azure.microsoft.com/updates?id=557877). If you're running applications across multiple Kubernetes clusters - and at scale, you probably are - this tackles the challenges around performance, global service discovery, and observability in distributed microservice environments.

**Microsoft Azure Kubernetes Application Network** also entered [public preview](https://azure.microsoft.com/updates?id=557922). Here's where it gets interesting - as Kubernetes environments scale across regions and clusters, IP-based networking becomes a management nightmare with limited application-level visibility and security controls. Application Network introduces application-layer abstractions that give you visibility and control at the level that actually matters - your services, not your IP addresses.

And for teams looking to move away from ingress-nginx (which is being deprecated upstream), **Application Routing with Meshless Istio** is in [public preview](https://azure.microsoft.com/updates?id=557927). This enables adoption of the Kubernetes Gateway API without the complexity of deploying a full service mesh. You get the standards alignment and routing capabilities without the operational overhead. If you've been dreading the nginx migration conversation, this might be your answer.

## AKS GPU Metrics and Blue-Green Upgrades

Two more AKS updates worth calling out individually.

**AKS managed GPU metrics in Azure Monitor** hit [public preview](https://azure.microsoft.com/updates?id=557882). If you're running GPU-backed workloads for ML training or inference, you've probably been frustrated by the lack of integrated GPU visibility alongside your Kubernetes metrics. This automatically exposes performance and utilization data from NVIDIA GPU-enabled node pools into managed Prometheus. No more cobbling together custom exporters or running third-party agents just to see if your expensive GPUs are being properly utilized.

**Blue-green agent pool upgrades** are in [public preview](https://azure.microsoft.com/updates?id=557862). In-place node pool upgrades have always carried risk because you're applying changes directly to your running environment. The blue-green approach creates a parallel node pool with the new configuration, lets you validate everything works, and then shifts workloads over. If something goes wrong, you still have the original pool. This is the kind of safety net that makes upgrades from "hold your breath" moments into routine operations.

## PostgreSQL Migration Opens the Doors Wide

The PostgreSQL team had a productive week focused on making it easier to move your databases to Azure, regardless of where they're currently running.

**Google AlloyDB** is now a [supported migration source](https://azure.microsoft.com/updates?id=558851). If you're running AlloyDB on GCP and looking to consolidate to Azure, the PostgreSQL migration service can now handle that directly. Secure, reliable workflows designed to minimize downtime during the move.

**EDB PostgreSQL workloads** are also now [supported](https://azure.microsoft.com/updates?id=558865). Running EDB Postgres Extended Server? You can migrate to Azure Database for PostgreSQL using the same migration service. This matters for enterprises that standardized on EDB and are now looking at cloud consolidation.

**Online migration now uses the pgoutput plugin** and it's [generally available](https://azure.microsoft.com/updates?id=558846). This aligns with PostgreSQL's native logical replication framework, improving ecosystem compatibility and making online migrations more reliable. The practical benefit? Less downtime, better performance, and fewer edge cases during migration.

And a small but handy one - **custom time zone support for pg_cron via cron.timezone** is [generally available](https://azure.microsoft.com/updates?id=558870). If you've ever had scheduled jobs firing at the wrong time because pg_cron was using a different timezone than your application, this fixes that. Configure `cron.timezone` and your scheduled jobs run when you actually want them to.

## Azure SQL Gets Its Late-March Update

The [Azure SQL late-March update](https://azure.microsoft.com/updates?id=558879) bundle landed with some practical improvements. You can now configure built-in SQL code analysis rules and severity settings without editing project XML directly. There are also new Fabric connectivity and provisioning options. These are the kind of quality-of-life improvements that add up over time - less XML wrestling, more actual work.

## Cosmos DB Mirroring Gets Private Endpoints

**Cosmos DB Mirroring in Microsoft Fabric with private endpoints** is [generally available](https://azure.microsoft.com/updates?id=558836). The ability to mirror your operational Cosmos DB data into Fabric for analytics was already useful, but now you can do it while keeping your enhanced network security posture intact. Private endpoints mean your data stays on the private network during replication.

For organizations that held off on Cosmos DB mirroring because of network security requirements, that blocker is gone. Unlock analytics on your operational data without compromising your security posture.

## Azure SQL Managed Instance Change Event Streaming

Here's one for the event-driven architecture fans. **Azure SQL Managed Instance change event streaming** is in [public preview](https://azure.microsoft.com/updates?id=558884). You can now stream row-level data changes - inserts, updates, and deletes - from SQL Managed Instance to Azure Event Hubs in near real time.

SQL publishes changes as transactions commit, reducing latency while minimizing the load on your database. If you've been building CDC pipelines with custom solutions or third-party tools, this native capability could simplify your architecture significantly.

## Fabric Mirroring for MySQL

**Fabric Mirroring integration for Azure Database for MySQL** entered [public preview](https://azure.microsoft.com/updates?id=558841). You can now replicate MySQL operational data into Microsoft Fabric in near real time without building or maintaining ETL pipelines. If your analytics team needs access to MySQL data in Fabric, this removes the need for custom data movement solutions.

## OpenTelemetry Gets Native Azure Monitor Support

**Ingesting OTLP data into Azure Monitor with the OpenTelemetry Collector** is in [public preview](https://azure.microsoft.com/updates?id=559273). Azure Monitor now supports native ingestion of OpenTelemetry Protocol signals, enabling you to send telemetry data directly from OpenTelemetry-instrumented applications and platforms to Azure Monitor.

This is a big deal for teams that have standardized on OpenTelemetry. Instead of converting signals or running Azure-specific exporters, you can now send OTLP data straight to Azure Monitor. Configure your OpenTelemetry Collector to point at Azure Monitor, and you're done. Less middleware, fewer conversion layers, better signal fidelity.

## Azure Monitor Gets Arc-Enabled Kubernetes Alerts

**Azure Monitor Prometheus community recommended alerts for Azure Arc-enabled Kubernetes** is [generally available](https://azure.microsoft.com/updates?id=558825). One-click enablement of Prometheus recommended alerts directly in the Azure Portal for your Arc-enabled clusters. These are based on enhanced Prometheus community rules and provide comprehensive coverage across your cluster health metrics. If you're running hybrid Kubernetes through Arc, this removes the manual work of configuring alert rules yourself.

## Azure Container Storage v2.1.0

**Azure Container Storage v2.1.0** is [generally available](https://azure.microsoft.com/updates?id=557912) with Elastic SAN integration and on-demand installation. Containerized workloads that need higher and more consistent storage performance can now consume storage from a shared Elastic SAN pool. The on-demand installation model simplifies deployment - you don't need to pre-install the storage stack on every cluster, just enable it when you need it.

## Bicep Corner: Still Cruising on v0.41.2

No new Bicep releases this week - we're still on v0.41.2 from late February. That said, if you haven't tried the snapshot command yet, there's no better time.

```bash
az bicep upgrade
```

The snapshot command, the `@nullIfNotFound()` decorator for existing resources, and the Visualizer V2 experiment are all worth exploring. Sometimes a quiet release week is the best time to catch up on features you missed.

## Wrapping Up

This week was unmistakably a Kubernetes networking week. Between metrics filtering, network logs, cross-cluster networking, application-layer abstractions, and an AI troubleshooting agent, the AKS team delivered a comprehensive upgrade to how you observe, manage, and debug container networking on Azure. If you've been struggling with Kubernetes networking visibility, several of these features directly address that pain.

The PostgreSQL migration story also got significantly stronger with AlloyDB and EDB support. Microsoft is clearly making it as easy as possible to consolidate PostgreSQL workloads onto Azure, regardless of where they're currently running.

And the OpenTelemetry native support in Azure Monitor is one of those updates that quietly changes how teams think about observability. Less vendor lock-in, more standards-based telemetry, and a simpler collection pipeline.

What are you most excited about this week? Planning to try the blue-green agent pool upgrades, or is the OpenTelemetry native ingestion more your speed? Let me know what lands in your environment first.

Until next week - keep building, keep shipping, and may your Kubernetes networking always resolve on the first try.

---

**Useful Links:**
- [Azure Updates Portal](https://azure.microsoft.com/en-au/updates)
- [Bicep v0.41.2 Release Notes](https://github.com/Azure/bicep/releases/tag/v0.41.2)
