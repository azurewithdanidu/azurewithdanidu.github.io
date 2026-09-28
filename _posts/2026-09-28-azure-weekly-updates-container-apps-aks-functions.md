---
title: "Azure Weekly Updates - Week of September 28, 2026"
date: 2026-09-28
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "bicep"
  - "cloud-news"
  - "container-apps"
  - "aks"
  - "azure-functions"
---

Howdy Folks,

It has been a little while since I sat down to round up the Azure news, so naturally Azure chose this week to hand us a fairly packed release train. You know the feeling: you return from a short break, open the backlog, and discover that the platform has quietly shipped new ways to run agent code, stretch Kubernetes beyond the cloud, and remind every Functions owner that runtime support dates are very much a real thing.

The big pattern this week is operational choice. Container Apps gets more room for safely running untrusted code, AKS gets a new hybrid deployment shape, and the Functions announcements make the upgrade path unusually clear. Let's get into it.

## Highlight of the Week: Container Apps Sandboxes Are Now GA

If you have ever built an agent that can execute code, run a build, or process customer-supplied content, you have probably reached the uncomfortable part of the architecture diagram. The box labelled "run untrusted stuff safely" tends to grow tentacles very quickly.

**[Azure Container Apps Sandboxes are now generally available](https://azure.microsoft.com/updates?id=561262)**, giving teams an isolated place to run workloads such as agent actions, multi-tenant jobs, dev environments, and CI/CD tasks without assembling the isolation machinery themselves.

The important bit is not simply that another compute option exists. This means you can preserve per-session state, deal with bursty demand, and put a stronger boundary around workloads that should not share a process, filesystem, or a very awkward incident call. For teams building agentic applications, this is a much more practical foundation than treating a general-purpose container runtime as a sandbox and hoping the word is doing all the security work.

Azure Container Apps also shipped **[Container Apps Express](https://azure.microsoft.com/updates?id=559242)** as generally available. That is the other end of the spectrum: a faster path from an application idea to a scaled service, with fewer early infrastructure decisions. Sandboxes give you control where you need isolation; Express gives you momentum where you need to get moving. A useful pairing.

## AKS Takes a Step Toward the Edge

Here is a preview that is worth watching closely: **[Flex Nodes for AKS](https://azure.microsoft.com/updates?id=571919)**.

Flex Nodes let application and platform teams connect hybrid and edge infrastructure as worker nodes to an AKS control plane in Azure. If you have ever tried to give factory, retail, branch, or on-premises workloads a Kubernetes experience consistent with cloud workloads, you know the usual compromise: separate control planes, separate tooling, separate operational habits, and an expanding collection of "special" cases.

The cool part is that this preview aims to keep the control plane consistent while letting the worker nodes live closer to where the workloads and data actually are. That does not make hybrid Kubernetes magically simple, because nothing does, but it can reduce the number of different operating models your team has to carry around in its head.

## PostgreSQL 18 Shows Up in Two Different Flavours

Database news was quietly interesting this week too. **[Azure HorizonDB now supports PostgreSQL 18 in public preview](https://azure.microsoft.com/updates?id=573048)**, bringing the latest PostgreSQL version to Microsoft's fully managed, PostgreSQL-compatible cloud-native database service.

At the same time, **[PostgreSQL 18 support for Azure Database for PostgreSQL elastic clusters is generally available](https://azure.microsoft.com/updates?id=571047)**. That matters for teams with distributed PostgreSQL workloads that want current database capabilities without turning a version upgrade into a mini-project every time.

This is one of those updates where I would resist the urge to upgrade production on Friday afternoon. But if PostgreSQL 18 is already on your roadmap, you now have two Azure database paths worth evaluating based on whether you need a cloud-native service preview or the distributed scale model of elastic clusters.

## Developer Workflow Gets a Guided Copilot Lane

The **[Guided Copilot experience for building Azure apps in VS Code](https://azure.microsoft.com/updates?id=572214)** has entered public preview.

Free-form chat is great until you need to get from an idea to a deployed application and realise the missing pieces are not glamorous: project structure, provisioning choices, configuration, deployment, and verification. This preview introduces a more structured workflow in VS Code that walks through that journey with GitHub Copilot.

For newer Azure developers, the value is obvious. For experienced teams, it could be a useful way to make the first-mile experience more predictable and less dependent on the one person who remembers every bootstrap command. I will be watching how well it holds up when an app is not a cheerful demo and has networking, identity, and existing infrastructure in the mix.

## Functions Gets PowerShell 7.6, Plus Three Dates to Put on the Calendar

Azure Functions now has **[general availability support for PowerShell 7.6](https://azure.microsoft.com/updates?id=572219)**. You can develop PowerShell 7.6 apps locally and deploy them to Functions plans, which is exactly what you want before a support deadline turns your upgrade into a calendar emergency.

And Azure was not subtle about the deadlines:

- **[PowerShell 7.4 support ends November 10, 2026](https://azure.microsoft.com/updates?id=572770)**. Function apps will keep running, but security updates and customer support stop.
- **[.NET 8 and .NET 9 support ends November 10, 2026](https://azure.microsoft.com/updates?id=572838)**. Plan the move to .NET 10 now, while you can test it on your terms.
- **[Node.js 22 support ends April 30, 2027](https://azure.microsoft.com/updates?id=572771)**. Node.js 24 is the target runtime.

This is the practical call to action from the week. Inventory your Functions apps, identify their runtime versions, and make the upgrade work visible. "The app still works" is not the same as "the app is still supported," and those two statements have caused enough trouble over the years already.

## A Couple More Changes Worth Knowing

Two more announcements round out the week:

- **[Instant Access for VM restore points is generally available](https://azure.microsoft.com/updates?id=572573)** for application-consistent restore points on VMs with Premium SSD v2 or Ultra disks. You can begin restoring a disk as soon as the snapshot is created, rather than waiting for background replication to finish. In a recovery situation, minutes matter more than any slide deck says they do.
- **[Azure Sphere OS 26.09 is generally available](https://azure.microsoft.com/updates?id=572579)** in the Retail feed. It updates the operating system only, so connected devices will receive it from the cloud without an SDK update. The less exciting a device fleet update is, the better, frankly.

There is also a long-range retirement notice for **[Azure Communication Services standalone services](https://azure.microsoft.com/updates?id=557117)**, scheduled for September 30, 2028. Two years is plenty of time, until it somehow becomes two months, so affected teams should identify the services in use and add a migration conversation to the roadmap now.

## Bicep Corner: Catching Up with v0.47.16

There was no Bicep release in this specific seven-day window, but since this roundup has been away for a bit, the latest **[Bicep v0.47.16 release](https://github.com/Azure/bicep/releases/tag/v0.47.16)** is worth a look.

The headline I like most is the experimental `bicep docs generate` command. You can generate Markdown documentation for modules, including across a pattern of modules:

```bash
bicep docs generate --pattern '.\modules\**\main.bicep'
```

If your infrastructure repository has excellent modules and documentation that is "coming soon" since last quarter, this may be your gentle nudge. The release also adds configuration inheritance through `extends` in `bicepconfig.json`, new optional linter rules for missing descriptions, and startup performance improvements for the CLI.

The configuration inheritance piece is especially useful for platform teams: keep organisation-wide guardrails in one base configuration, then allow individual repositories to add the few rules that genuinely differ. Less duplicated JSON, fewer linter debates, and a better chance that standards remain standards after the first week.

## What I Am Watching Next

I will be keeping an eye on three threads: whether Container Apps Sandboxes become the obvious execution home for production agents, how Flex Nodes behaves in real hybrid operations, and whether teams use the Functions runtime notices as a reason to clean up runtime inventories before the deadlines start looming.

## Wrapping Up

This week was not about one flashy platform feature. It was about making choices that hold up in production: isolate risky code paths, bring a consistent Kubernetes model to the edge, and upgrade runtimes before support ends rather than after someone forwards an alarming email.

If you only pick one thing to act on this week, check your Azure Functions runtimes. It is simple, concrete, and a future incident you can avoid before it has a chance to become interesting.

What are you looking at first: Container Apps Sandboxes, Flex Nodes, or a runtime upgrade backlog that has been quietly judging you from the corner?
