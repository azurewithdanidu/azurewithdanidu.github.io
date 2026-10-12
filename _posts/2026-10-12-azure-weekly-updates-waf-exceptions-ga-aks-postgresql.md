---
title: "Azure Weekly Updates - Week of October 12, 2026"
date: 2026-10-12
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "bicep"
  - "cloud-news"
  - "waf"
  - "application-gateway"
  - "aks"
  - "postgresql"
---

Howdy Folks,

Some weeks Azure ships one headline feature and calls it a day. This was not one of those weeks. The past seven days gave us a genuine security milestone, a pile of PostgreSQL and AKS movement, a fresh Bicep release, and a retirement list long enough that you will want a coffee and a spreadsheet before you read it.

The theme I kept noticing was *tuning the edges*. A lot of this week's updates are about giving you finer control over things that used to be all-or-nothing: what your WAF inspects, how AKS reaches the internet, where your databases live, and which runtimes you are quietly still depending on. Let's get into it.

## Highlight of the Week: WAF Exceptions Go Generally Available

If you have ever run Azure WAF in Prevention mode, you know the specific flavour of pain where a legitimate request keeps tripping a single managed rule, and your only "fixes" are a sledgehammer or a bigger sledgehammer. That era is over.

**[Exceptions in WAF for Azure Application Gateway and Azure Front Door are now generally available](https://azure.microsoft.com/updates?id=574343)**. This lets you bypass WAF inspection for an entire request, but *only* against the specific rules, rule groups, or rulesets you nominate - while every other protection keeps running on that same traffic.

Here is why this matters. Before exceptions, if rule 942100 (a SQL injection signature) threw a false positive on your `/login` endpoint, you either disabled the rule everywhere, wrote a custom Allow rule that waved off *all* of DRS, CRS, and Bot Protection, or wrestled with an exclusion that only covers a single field. None of those are "skip just this rule for this traffic, keep the rest armed." Exceptions are exactly that missing middle ground, and they land at the perfect level of granularity for real-world tuning.

I liked this one so much I wrote a full deep-dive on it: [Azure Application Gateway WAF Exceptions List](/posts/azure-application-gateway-waf-exceptions-list/), covering the exclusions-vs-exceptions-vs-custom-rules distinction, the limits, and how to deploy it with Bicep, PowerShell, and the CLI. If you tune WAF for a living, start there.

## The Application Gateway WAF Team Has Been Busy

The exceptions GA was not the only WAF news. **[IPv6 support for Application Gateway WAF is now in public preview](https://azure.microsoft.com/updates?id=573861)**, bringing inspection and enforcement to IPv6 traffic for dual-stack environments.

If you have been putting off IPv6 because "the WAF does not fully speak it yet," that excuse is on its way out. As more client networks go dual-stack by default, having your web firewall actually inspect v6 traffic - rather than politely ignoring it - is the difference between real coverage and a comfortable illusion of it. Worth testing early if IPv6 is anywhere on your roadmap.

## AKS Gets a Beefier NAT Gateway and a Bare-Metal Option

Kubernetes had a solid week. First, **[Managed StandardV2 NAT Gateway for AKS is now generally available](https://azure.microsoft.com/updates?id=574430)**. StandardV2 becomes the default managed NAT Gateway SKU for new clusters in supported regions when you use the `managedNATGateway` outbound type, and it ships with zone redundancy by default plus higher bandwidth.

The quietly important part here is zone redundancy *by default*. Outbound connectivity is one of those things nobody thinks about until a zone has a bad day and suddenly every outbound call from your cluster is having a bad day too. Getting that resilience without hand-assembling it is a nice default to inherit.

On the more adventurous end, **[AKS on bare metal now runs on Ubuntu in public preview](https://azure.microsoft.com/updates?id=573782)**. Running Kubernetes on-premises has traditionally meant adding a virtualization layer or giving up control of your hardware - a real problem for AI workloads that want direct access to local data and compute. This preview trims that compromise down for teams that need Kubernetes close to the metal.

## PostgreSQL Keeps Expanding Its Footprint

Postgres fans ate well this week. **[Azure HorizonDB is expanding to additional regions in public preview](https://azure.microsoft.com/updates?id=572940)**, giving you more places to deploy Microsoft's cloud-native, PostgreSQL-compatible database closer to your users.

More interesting for existing workloads: **[Azure Backup for PostgreSQL flexible server and elastic cluster (v2) is now in public preview](https://azure.microsoft.com/updates?id=573425)**. This brings enterprise-grade long-term retention using physical backups taken from managed disk snapshots and vaulted in an Azure Backup vault, extending protection to servers up to 32 TB on Premium SSD v1. If your backup strategy has been "the built-in retention and a hope," this is a meaningful upgrade in durability and scale. And yes, **[Azure Database for PostgreSQL flexible server also lit up in the East US 3 region](https://azure.microsoft.com/updates?id=573691)** for those of you planning deployments there.

## A Few More GA Releases Worth Knowing

Three more "Launched" items rounded out the week:

- **[Anyscale on Azure is now generally available](https://azure.microsoft.com/updates?id=573744)** - a managed platform for running distributed Python workloads on Ray, deploying directly onto your AKS cluster and integrating with the Azure services you already use. If you are scaling Python-based ML or data processing, this is a much shorter path than wiring Ray together yourself.
- **[Microsoft Agent 365 integration with Azure API Management is in public preview](https://azure.microsoft.com/updates?id=574204)**, connecting centralized governance with runtime enforcement for MCP servers and tools. As agent platforms grow up, putting an API gateway in front of your MCP endpoints is going to be the obvious governance move.
- **[The bulkadmin role is now enabled for SQL Server on Linux](https://azure.microsoft.com/updates?id=573443)** (SQL Server 2025 CU9 and 2022 CU27), so you can run bulk import operations without handing out `sysadmin`. Least-privilege wins are always welcome.

## The Retirement Pile: Put These on a Calendar

Azure was in a tidying mood this week, so grab your migration planning hat:

- **[Azure Deployment Environments retires February 22, 2027](https://azure.microsoft.com/updates?id=567934)** - the nearest deadline on this list, and the one to act on first.
- **[Microsoft Dev Box retires September 18, 2028](https://azure.microsoft.com/updates?id=567933)**, now in maintenance mode with the closing-down process already underway.
- **[App Service support for Java 8, 11, and 17 ends September 1, 2027](https://azure.microsoft.com/updates?id=568585)** - apps keep running, but security updates and support stop. Plan the move to a newer LTS.
- **[The Azure Key Vault Secrets Provider Extension for Arc-enabled Kubernetes retires October 9, 2027](https://azure.microsoft.com/updates?id=570313)**, with the Secret Store Extension as the migration target.
- **[Always Encrypted with Intel SGX enclaves retires October 31, 2027](https://azure.microsoft.com/updates?id=569236)** as SGX-enabled DC-series hardware phases out; move to VBS enclaves.
- **[App Service on Azure Stack Hub retires September 30, 2029](https://azure.microsoft.com/updates?id=568178)**, with new installations unsupported from September 30, 2026.
- **[The pod name dimension in AKS pod platform metrics retires September 30, 2027](https://azure.microsoft.com/updates?id=570232)** as those metrics move to aggregate pod counters - check any dashboards or alerts that slice by pod name.

None of these are fire drills today. But "the app still runs" and "the app is still supported" are different sentences, and the gap between them has a habit of becoming urgent at the worst possible moment.

## Bicep Corner: v0.48.1 Lands

Right on cue, **[Bicep v0.48.1 shipped](https://github.com/Azure/bicep/releases/tag/v0.48.1)**, and the visualizer got most of the love this time.

The **visualizer improvements** are the standout: a separate resource-creation dock with better browsing and filtering, API version selection that respects your deployment scope, automatic filling of required properties, and inline diagnostics right on the graph. It even lists common resource providers first. Paired with brand-new **undo/redo support** (Ctrl/Cmd+Z and friends for resource creation, node moves, and layout resets), the visual authoring story is getting genuinely usable rather than just a pretty diagram.

There is also a security-minded change worth flagging for anyone using custom clouds. Custom clouds that are not in the built-in list now have to be explicitly allowed through a new environment variable, the same way trusted registries work:

```bash
# Allow a custom cloud endpoint for Bicep
BICEP_TRUSTED_CLOUDS='[{"resourceManagerEndpoint":"https://management.example.com","activeDirectoryAuthority":"https://login.example.com"}]'
```

Rounding it out: GA language version emission for `NullableExisting` and `ThisNamespace`, `apiVersion` is now optional in the Azure resource schema MCP tool, and a batch of community fixes around linting, decorator placement, and the `bicep test` exit code. A tidy, practical release.

## What I Am Watching Next

Three threads on my radar: whether WAF exceptions become the default tuning tool teams reach for instead of custom Allow rules, how quickly IPv6 WAF support moves toward GA now that the groundwork is down, and whether the Agent 365 plus API Management pairing becomes the standard way to govern MCP servers as agent platforms mature.

## Wrapping Up

This week was all about control at the edges - sharper WAF tuning, more resilient AKS networking, broader database reach, and a visualizer that finally lets you undo your mistakes. If you only act on one thing, let it be the WAF exceptions GA: it is the kind of feature that pays for itself the very first time it saves you from choosing between a false positive and a security hole.

And if you have a retirement from that list quietly judging you from the backlog, maybe give it five minutes this week too.

What caught your eye first - the WAF exceptions, the StandardV2 NAT Gateway, or that retirement list you are pretending you did not see?
