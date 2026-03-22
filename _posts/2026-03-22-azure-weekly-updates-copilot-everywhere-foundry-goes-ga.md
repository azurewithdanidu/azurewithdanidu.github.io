---
title: "Azure Weekly Updates - Week of March 22, 2026"
date: 2026-03-22
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "github-copilot"
  - "foundry"
  - "cloud-news"
---

Howdy Folks,

Let me tell you about the week Microsoft decided to put GitHub Copilot in everything database-related. If you've been working with Azure SQL or the MSSQL extension in VS Code, you're about to get very familiar with AI-assisted development. Between SQL Server Management Studio getting Copilot, the MSSQL extension getting multiple Copilot features, and even a brand new SQL MCP Server hitting preview, it's clear Microsoft is betting big on AI-powered database workflows.

But that's just one storyline this week. We've also got Microsoft Foundry Agent Service going GA, a bunch of VM retirements you need to know about, and Azure Red Hat OpenShift picking up some seriously useful identity features. Let's break it down.

## GitHub Copilot Takes Over Your Database Tooling

Here's the thing about working with databases - you spend half your time writing queries and the other half trying to remember exact syntax, table relationships, and that one JOIN you always mess up. Microsoft apparently decided enough was enough and dropped GitHub Copilot integration across their entire database tooling ecosystem this week.

**SQL Server Management Studio 22 gets Copilot** and it's now generally available. If you're still using SSMS as your primary database management tool - and let's be honest, plenty of us are - you can now get AI-powered code completions, query suggestions, and help right inside the tool you already know. No more switching to Google to remember the exact T-SQL syntax for window functions.

But wait, there's more. The MSSQL extension for Visual Studio Code is getting not one, not two, but multiple Copilot-powered features:

**Schema Designer with Copilot integration** is in preview, which means you can now design database schemas with AI assistance. Describe what you want in natural language, and Copilot helps generate the schema. Need a multi-tenant schema with proper isolation? Just ask.

**Database DevOps powered by SQL projects** is also in preview. This brings proper DevOps workflows to your database development - source control, CI/CD integration, and deployment automation, all with Copilot helping along the way. If you've been manually managing database migrations with numbered SQL scripts in a folder labeled "scripts-do-not-touch," this is your wake-up call.

**Data API builder with built-in Copilot** rounds out the preview features. Building REST or GraphQL APIs on top of your database is already easier with Data API builder, and now Copilot helps you configure endpoints, permissions, and query logic faster.

The cool part about all these Copilot integrations is they're not just code completion - they understand database context. Table relationships, index strategies, performance implications. It's like having a database architect looking over your shoulder, except it never gets tired of your questions.

## SQL MCP Server: Model Context Protocol Comes to Databases

Speaking of AI integrations, there's a new **SQL MCP Server in preview** that caught my attention. If you've been following the Model Context Protocol trend - and you should be - you know MCP is becoming the standard way for AI tools to interact with various services.

A SQL MCP Server means your AI coding assistants can now directly query and interact with SQL databases through a standardized protocol. Build agents that can read schema information, execute queries, analyze performance, and suggest optimizations - all without you having to write custom database connectors.

This is particularly interesting if you're building AI agents that need to work with database documentation, query historical data, or help with migrations. The MCP abstraction means your agent code stays clean and portable across different database systems.

## Azure SQL Gets Versionless Key Support for TDE

Here's a feature that solves an annoying operational problem. **Versionless key support for transparent data encryption** hit GA for Azure SQL Database this week.

If you've ever managed TDE with customer-managed keys, you know the pain - every time you rotate your keys in Azure Key Vault, you need to update references in your database configurations. Miss an update, and you're potentially looking at access issues or security gaps.

Versionless keys remove that headache. Point your TDE configuration at a key without specifying a version, and Azure SQL automatically uses the latest key version from Key Vault. Rotate your keys as often as your security team demands, and the database just picks up the new version. No manual updates, no deployment scripts, no forgotten references.

The practical impact? Key rotation becomes an actual operational practice instead of that thing you know you should do but keep postponing because it's annoying. Your security posture improves, and you sleep better.

## Microsoft Foundry Agent Service Hits GA

Big news for anyone building AI agents on Azure - **Microsoft Foundry Agent Service is now generally available**. If you've been experimenting with Foundry in preview for building, deploying, and managing AI agents, you can now use it for production workloads.

Foundry gives you the infrastructure for building multi-agent systems - orchestration, state management, tool calling, and deployment workflows all baked in. Instead of cobbling together agent frameworks, prompt management, and deployment pipelines yourself, Foundry provides the platform.

What makes this GA announcement significant is timing. We're seeing GitHub Copilot integrations everywhere, SQL MCP servers launching, and AI-assisted development becoming the norm. Foundry provides the foundation for organizations to build their own specialized agents on top of Azure's infrastructure.

If you've been holding back on agent-based workflows because you're worried about preview stability or enterprise support, that barrier just disappeared.

## Azure Databricks: OneLake Federation and Lakeflow Connect Free Tier

Two updates for Databricks users this week, and both make data integration easier.

**Azure Databricks OneLake Catalog Federation** hit preview, which means you can now federate Microsoft Fabric's OneLake catalogs directly into your Databricks workspace. If your organization uses both Databricks and Microsoft Fabric, you've probably been dealing with data silos and awkward integration patterns. OneLake Federation lets you query OneLake data from Databricks without copying or moving data around.

The practical scenario? Your data engineering team uses Databricks for complex transformations and ML workflows, but your analytics team has datasets in OneLake from Power BI and Fabric. Instead of duplicating data or building custom connectors, you just federate the catalog and query directly.

**Lakeflow Connect Free Tier** went GA this week. Lakeflow Connect is Databricks' managed connectivity layer for integrating various data sources into your lakehouse. The free tier means you can start connecting data sources - databases, SaaS applications, cloud storage - without upfront costs. Test it out, build your data pipelines, and only pay when you scale up.

This is particularly useful for teams just getting started with lakehouse architectures. The barrier to experimentation just dropped to zero.

## Azure Red Hat OpenShift Gets Identity Upgrades

If you're running OpenShift on Azure, two identity features just hit GA: **Managed Identity and Workload Identity support**.

Managed Identity means your OpenShift cluster can authenticate to Azure services without storing credentials. Need your pods to read from Azure Storage or write to Cosmos DB? Assign a managed identity, grant it permissions, and let Azure handle the authentication. No secrets in environment variables, no connection strings in config files.

Workload Identity takes this further by extending Kubernetes service accounts to work with Azure AD identities. Each workload in your cluster can have its own identity with specific permissions. Microservice A gets read access to Storage, Microservice B gets write access to Event Hubs, and you manage it all through Azure RBAC.

For teams running containerized workloads on OpenShift, this removes a major security and operational headache. Credential rotation, secret management, and least-privilege access all become manageable instead of nightmares.

## WAF Gets Default Rule Set 2.2

**Application Gateway and Azure Front Door WAF** got an update to Default Rule Set 2.2, now generally available. This update includes improved threat detection, refined rule logic to reduce false positives, and enhanced coverage for OWASP Top 10 vulnerabilities.

What matters here is the ruleset support policy update that came with it. Microsoft is now providing clearer guidance on rule set lifecycles, deprecation timelines, and upgrade paths. If you're managing WAF policies across multiple applications, knowing when rule sets get updated or retired makes planning much easier.

The core recommendation remains the same - use the latest rule set for new deployments, and plan upgrades for existing deployments to stay current on threat protection.

## Heads Up: Virtual Machine Retirements Coming in 2027

If you're running any of these VM series, mark your calendar for May 31, 2027:

- **NP-series** (FPGA-optimized VMs)
- **HBv2-series** (HPC workloads)
- **HC-series** (compute-intensive HPC)

All three are being retired. You've got about 14 months to plan migrations to newer VM series. For HPC workloads, look at HBv3 or HBv4 series. For FPGA workloads, evaluate whether FPGAs are still your best option or if GPU-based alternatives make more sense now.

May 2027 feels far away, but procurement, testing, and migration planning for specialized workloads takes time. Don't wait until April 2027 to start planning.

Also getting retired:

- **Azure SQL Elastic query (Shard_Map_Manager mode)** - March 2027
- **Emissions Impact Dashboard** - March 2027
- **Azure VMware Solution AV36P and AV52 nodes** - June 2029
- **Azure Sphere** - July 2031

Azure Sphere retiring in 2031 is notable because it's a five-year runway for IoT device migrations. If you're running Azure Sphere devices in production, start evaluating alternatives now. Five years sounds long, but device lifecycles and embedded system migrations are measured in years, not months.

## Bicep Corner: Still on v0.41.2

On the Bicep front, we're still running with v0.41.2 from early March, which brought the snapshot command to GA. No new releases this week, which is fine - not every week needs to be a release week.

If you haven't upgraded yet:

```bash
az bicep upgrade
```

The snapshot command is worth it alone. Preview your infrastructure deployments, validate changes before they hit Azure, and show stakeholders exactly what resources will be created or modified. It's the feature you didn't know you needed until you tried it.

## What This Week Tells Us

Reading between the lines, the GitHub Copilot database integrations show Microsoft is going all-in on AI-assisted development for every part of the stack. SQL tooling was one of the last places where AI assistance wasn't standard, and that gap just closed.

Microsoft Foundry hitting GA suggests enterprise adoption of agent-based workflows is accelerating. Organizations are moving past experimentation and into production deployment of AI agents, and Microsoft is providing the infrastructure to support that shift.

The VM retirement notices are part of the normal hardware lifecycle, but they're also a signal to evaluate whether your workload really needs specialized hardware or if newer general-purpose VMs can handle it more cost-effectively.

## Wrapping Up

Between GitHub Copilot showing up in every database tool, Foundry going GA for agent deployments, and identity improvements for OpenShift, this week brings some genuinely useful capabilities. The database tooling updates in particular solve real workflow problems - less context switching, better AI assistance, and tighter integration between development and operations.

And if you're running any of those specialized VM series getting retired, you've got advance notice to plan migrations properly. Don't be the person scrambling in May 2027.

Are you planning to try GitHub Copilot in SSMS or the MSSQL extension? Thinking about building agents on Foundry now that it's GA? Let me know what you're excited about from this week's updates.

Until next week - keep building, keep shipping, and maybe let AI write some of those SQL queries for you.

---

**Useful Links:**
- [Azure Updates Portal](https://azure.microsoft.com/en-au/updates)
- [Bicep v0.41.2 Release Notes](https://github.com/Azure/bicep/releases/tag/v0.41.2)
