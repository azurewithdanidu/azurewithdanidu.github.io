---
title: "Azure Weekly Updates - Week of April 13, 2026"
date: 2026-04-13
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "bicep"
  - "cloud-news"
  - "azure-functions"
  - "aks"
  - "mcp"
---

Howdy Folks,

Let me paint you a picture. You've just built a brilliant MCP server on Azure Functions. Your tools are sharp, your handlers are clean, and you're feeling good about yourself. But then someone asks "can you expose resources through MCP too?" and you quietly stare at the screen knowing Functions only supported _tools_, not _resources_. That gap just closed this week. Between that, some genuinely useful AKS fixes, Bicep's console hitting GA, and a new Role Definitions function that's going to simplify your RBAC templates considerably, this was a week worth talking about.

Let's get into it.

## Azure Functions Finally Speaks Full MCP

Here's the thing about the Model Context Protocol - it has two primary building blocks that matter: tools and resources. Tools are the actions your server can perform. Resources are the data your server exposes. Azure Functions had been great for MCP tools for a while now, but if you needed to expose resources from your MCP server, you were on your own.

Not anymore. **Azure Functions now supports MCP resource triggers**, and it's [generally available](https://azure.microsoft.com/updates?id=559981). This means you can now build a fully spec-compliant MCP server hosted entirely on Azure Functions - tools, resources, the whole package. If you've been building AI agent backends or Copilot integrations and hit the wall of "resources aren't supported," this is your green light to move forward.

The practical impact is that your Functions-based MCP server can now expose context data - think configuration, documentation, structured data, file contents - to AI agents without requiring a separate hosting layer. One deployment, complete MCP compliance. That's the kind of simplification that actually matters when you're trying to get something into production.

## AKS Fixes the IP Address Problem You've Definitely Hit

If you've been running AKS clusters long enough, you've probably felt this pain at least once. You plan your networking, pick a pod CIDR range, deploy everything, and then months later the cluster keeps growing and suddenly you're running out of pod IP addresses. Your options? Historically, rebuild the cluster. Not great.

**Pod CIDR expansion in AKS is now generally available**, which changes the conversation entirely. You can now [expand your pod IP range in place](https://azure.microsoft.com/updates?id=557907) for overlay-based AKS clusters without the rebuild drama. Growing clusters that have exhausted their IP space can breathe again without the operational disruption of tearing down and recreating environments. If you've been putting off cluster expansion because of networking constraints, that blocker is gone.

And in the "small but satisfying" category, **disabling HTTP proxy in AKS is now GA** as well. If you've had HTTP proxies configured for outbound traffic control and need to change or remove those settings, you can now do it [without cluster disruption](https://azure.microsoft.com/updates?id=557857). Previously, changing proxy settings on a running cluster was the kind of thing that made ops engineers nervous. Now it's just a configuration change.

## AKS Gets Better Eyes with Built-in Observability

Here's where it gets interesting for anyone running AKS workloads at scale. **Observability in AKS Namespace and Workload Views is now generally available**.

Azure Monitor managed service for Prometheus data now [surfaces directly within Namespace and Workload views](https://azure.microsoft.com/updates?id=560039) in the AKS portal experience. This means you can see cluster health, workload status, pending or failed pods, and resource utilization without leaving the AKS blade and jumping into a separate monitoring dashboard.

If you've ever had to open three browser tabs to correlate a failing workload against its resource utilization against its namespace-level health, that workflow just got simpler. The data is now right where the context is. Troubleshoot faster, correlate more naturally, and keep your sanity intact when something goes sideways at 2am.

## Azure Red Hat OpenShift Goes Big with NVIDIA H100 and H200

AI infrastructure on Azure OpenShift just got a significant upgrade. **Azure Red Hat OpenShift now supports NVIDIA H100 and H200 GPU-based VM SKUs**, and it's [generally available](https://azure.microsoft.com/updates?id=559547).

If you're running large-scale AI training, ML inference, or high-performance computing workloads on a fully managed OpenShift service, you can now access the flagship NVIDIA accelerator SKUs without leaving the managed OpenShift experience. This closes a gap for teams who standardized on Red Hat OpenShift but needed access to the latest GPU horsepower - they no longer have to choose between their preferred platform and the best available hardware.

For organizations that have been building out serious AI workloads and kept bumping into the "but we're on OpenShift" constraint, this is a meaningful unlock.

## Service Bus Gets Network Security Perimeter

Security teams rejoice. **Network Security Perimeter for Azure Service Bus is now generally available**.

What NSP does is create a [logical network boundary around your Service Bus namespaces](https://azure.microsoft.com/updates?id=559899) and other Azure PaaS resources, blocking unauthorized public access while still letting you control which identities and resources can communicate across that boundary. If your organization has been waiting to move message-heavy workloads to Service Bus because of network isolation requirements, this removes that concern.

The combination of PaaS convenience - no VMs, no infrastructure to manage - with proper network isolation is exactly the pattern modern security policies are pushing toward. One less exception to write in your network architecture documents, and one less reason for the security review to come back with questions.

## Event Grid Gets a Stripe Connection

Here's a preview that caught my attention if you work in payments or fintech. **Event Grid is now a destination for Stripe events**, and it's in [public preview](https://azure.microsoft.com/updates?id=559836).

The cool part is what this removes. Previously, if you wanted to act on Stripe webhooks in a scalable, event-driven way, you were either building custom webhook receivers or managing infrastructure to bridge Stripe's push model into your event processing pipelines. Now, Stripe events can route directly into Azure Event Grid, and from there into your entire Azure event processing ecosystem - Event Hubs, Functions, Logic Apps, whatever your architecture calls for.

No custom broker code, no webhook receivers to manage. This is the kind of integration that makes Stripe workloads on Azure a much simpler conversation at the architecture whiteboard.

## PostgreSQL Gets Quality-of-Life Improvements

Two PostgreSQL updates hit GA this week, both on the "your life just quietly got easier" end of the spectrum.

**PgBouncer 1.25.1 is now generally available** in Azure Database for PostgreSQL. If connection pooling is part of your scaling strategy - and at any meaningful load, it should be - you're now on a modern, supported version. Scale to thousands of connections with lower overhead, efficiently managing the idle and short-lived connections that otherwise eat up your database server capacity. The built-in nature of PgBouncer in the managed service means you get the pooling benefits without standing up and maintaining a separate pgBouncer tier.

**Maintenance notification enhancements** in Azure Service Health are also [generally available](https://azure.microsoft.com/updates?id=559628). Instead of receiving one notification per server when maintenance is planned across your PostgreSQL fleet, you now get a single consolidated notification per region. If you're running multiple PostgreSQL servers and have been drowning in maintenance notification emails, this is a straightforward improvement that reduces noise without losing the information you actually need. Small change, surprisingly noticeable improvement in your inbox.

## Azure Migrate Adds File Share Assessments

Planning a migration from on-premises file shares to Azure Files? **Azure Files assessments are now available in Azure Migrate**, and they're in [public preview](https://azure.microsoft.com/updates?id=560025).

This is the discovery and planning piece that fills a real gap. Previously, Azure Migrate could help you assess VMs and databases, but SMB and NFS file shares were a more manual exercise. Now you can run assessments against your Windows and Linux file shares, understand what's there, size your Azure Files targets, and figure out your migration approach before you start moving data. Discovery, visibility, and migration planning in one workflow rather than a spreadsheet someone built three years ago.

## Bicep Corner: The Console Graduates, and RBAC Gets Smarter

Big week for Bicep. **Bicep v0.42.1** dropped with two highlights worth properly celebrating.

**Bicep console is now generally available**. If you haven't played with `bicep console`, think of it as a REPL for Bicep expressions. You can evaluate Bicep functions interactively, test string manipulations, experiment with `parseCidr`, `dateTimeAdd`, and a hundred other functions without writing a full template and running a deployment just to check your output. As an authoring tool, it shaves real time off the "test this expression" loop.

```bash
echo "parseCidr('10.144.0.0/20')" | bicep console
```

You get the result immediately without touching a deployment. If you've ever written a complex string composition, deployed a template to check the output, realized something was wrong, and repeated that cycle - you know exactly why this matters.

The other headline is the [**Bicep Role Definitions Function**](https://github.com/Azure/bicep/releases/tag/v0.42.1). This is genuinely useful for anyone writing RBAC assignments in Bicep. Instead of hardcoding role definition IDs (those long GUID strings that nobody has memorized and everyone copies from the docs), you can now reference them by display name:

```bicep
properties: {
  roleDefinitionId: roleDefinitions('Data Factory Contributor').id
  principalId: scriptIdentity.principalId
}
```

Readable. Maintainable. Self-documenting. If you've ever searched the Azure docs mid-template to find the GUID for a built-in role because you forgot to save it somewhere, or worse had a typo in a GUID that caused an hours-long debugging session, you know why this feature matters. Your Bicep templates will be cleaner and your future self will thank you when you revisit them later.

The release also includes an **experimental Bicep Visualizer upgrade** that runs side-by-side with the existing one. The new visualizer has better UI styling, accessibility improvements including accent color support and a light high-contrast theme, and you can now export the dependency graph as a PNG image. Useful for documentation, architecture reviews, or just understanding a complex template you inherited with no documentation attached.

## Conclusion

A solid week, honestly. The MCP resource triggers for Azure Functions feels like a meaningful enabler for teams building AI infrastructure on Azure - that was a real gap and it's now closed. The AKS Pod CIDR expansion solves a problem that has historically been very disruptive to work around, and Bicep's console hitting GA with the Role Definitions function is the kind of developer quality-of-life update that compounds over time.

If you're running AI or GPU workloads on Red Hat OpenShift, now is a good time to look at H100/H200 availability. And if you haven't looked at Network Security Perimeter for your Service Bus namespaces yet, your security team will probably appreciate you raising it.

What stood out to you this week? Any of these updates immediately applicable in your environment? Let me know in the comments.
