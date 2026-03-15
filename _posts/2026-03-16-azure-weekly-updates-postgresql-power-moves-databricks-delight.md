---
title: "Azure Weekly Updates - Week of March 16, 2026"
date: 2026-03-16
categories:
  - "azure"
  - "weekly-updates"
  - "cloud"
tags:
  - "azure-updates"
  - "bicep"
  - "cloud-news"
  - "postgresql"
  - "databricks"
---

![Azure Weekly Updates - PostgreSQL Power Moves and Databricks Delight](/images/2026-03-16-azure-weekly-updates.png)

Howdy Folks,

Let me tell you about a week that PostgreSQL fans have been waiting for. If you've ever tried to convince your team to use PostgreSQL on Azure but got pushback about tooling support or operational capabilities, this week's updates just handed you the ammunition you need. Terraform, Bicep, Ansible support for elastic clusters? Grafana dashboards baked in? Customer-managed keys on Premium SSD v2? Yeah, Microsoft is serious about PostgreSQL.

But that's not all. We've got Databricks updates that make lakehouse management less painful, storage migration tools that actually understand privacy requirements, and - because Microsoft can't help themselves - an AI-powered SRE agent that's now generally available. Let's dive in.

## PostgreSQL's Big Week: Infrastructure as Code Arrives for Elastic Clusters

Here's the thing about PostgreSQL elastic clusters on Azure - they're powerful, they scale beautifully, and until this week, managing them through infrastructure as code was... let's say "creative". If you've been manually clicking through the portal to provision and configure elastic clusters while the rest of your infrastructure lived in Bicep or Terraform, those days are over.

[Terraform, Bicep, and Ansible support for elastic clusters](https://azure.microsoft.com/en-au/updates/generally-available-terraform-bicep-ansible-support-for-elastic-clusters-on-azure-database-for-postgresql/) hit general availability this week. This means you can now provision, configure, and manage your entire PostgreSQL elastic cluster infrastructure the same way you manage everything else - as code.

The practical impact? Your database infrastructure can finally live in the same Git repository as your application infrastructure. Code reviews for database changes. Version history. Automated deployments. All the good stuff you've been doing with your other Azure resources, now available for your distributed PostgreSQL workloads.

If you're running microservices with PostgreSQL backends, or you're dealing with multi-tenant architectures where each tenant gets their own database cluster, this update is a game changer. Define once, deploy everywhere, track changes forever.

## Observability Gets Easier: Grafana Dashboards for PostgreSQL

Remember when monitoring your PostgreSQL databases meant either staring at raw metrics in Azure Monitor or spending a weekend building custom Grafana dashboards? Well, Microsoft heard the collective groan and decided to do something about it.

[Azure Database for PostgreSQL now comes with Grafana dashboards](https://azure.microsoft.com/en-au/updates/generally-available-azure-database-for-postgresql-dashboards-with-grafana/) built right in. These aren't basic "here's your CPU usage" dashboards either - they're pre-configured with the metrics that actually matter for PostgreSQL workloads. Connection pool status, query performance, replication lag, transaction throughput - all the stuff you'd spend hours configuring yourself.

The cool part is this integrates directly with Azure Managed Grafana, so if you're already using Grafana for your observability stack, these dashboards just... appear. No manual import, no configuration copying, no "let me adjust this query syntax for the fourteenth time."

For teams running PostgreSQL in production, this means faster incident response and better visibility into what's actually happening with your databases. No more squinting at raw metrics trying to figure out why that query is slow.

## Security Gets Tighter: Customer-Managed Keys for Premium SSD v2

If you're in healthcare, finance, or any other heavily regulated industry, the phrase "customer-managed encryption keys" probably makes your compliance team breathe a little easier. This week, that capability expanded to [Premium SSD v2 disks for Azure Database for PostgreSQL](https://azure.microsoft.com/en-au/updates/public-preview-customer-managed-encryption-keys-now-supported-on-premium-ssd-v2-disks-for-azure-database-for-postgresql/).

Currently in preview, this lets you bring your own keys from Azure Key Vault to encrypt your PostgreSQL data at rest. Microsoft handles the encryption mechanics, but you control the keys. The data is yours, the keys are yours, and if you need to revoke access, you revoke the key.

The combination of Premium SSD v2 performance with customer-managed encryption gives you both speed and security. High IOPS, low latency, and the ability to tell your auditors "yes, we control the encryption keys" with a straight face.

## Databricks Gets Lakehouse Love

Two updates hit general availability for Databricks users this week, and both solve real operational headaches.

First up is [Azure Databricks Lakebase](https://azure.microsoft.com/en-au/updates/generally-available-azure-databricks-lakebase/), which brings enhanced capabilities for managing your lakehouse architecture. If you're running a data lakehouse on Databricks - combining the best of data lakes and data warehouses - Lakebase gives you better control over how you organize, govern, and manage that data.

Think of it as the management layer you didn't know you needed until you hit scale. Data governance policies, catalog management, and organizational controls that make sense when you're dealing with petabytes instead of gigabytes.

The second update is the ability to [update workspace network configuration](https://azure.microsoft.com/en-au/updates/generally-available-azure-databricks-update-workspace-network-configuration/) after the fact. This might sound boring, but if you've ever provisioned a Databricks workspace and then needed to change network settings - maybe you're migrating to private endpoints, or changing VNet integration - you know the pain of "sorry, you need to destroy and recreate the workspace."

Not anymore. You can now modify network configuration on existing workspaces. It's the kind of operational flexibility that should have been there from day one, but better late than never.

## Storage Migration Gets Private: AWS S3 to Azure Blob

Moving data from AWS S3 to Azure Blob Storage is nothing new - tools have existed for years. But here's where it gets interesting: [Azure Storage Mover now supports private data transfers](https://azure.microsoft.com/en-au/updates/public-preview-azure-storage-mover-enables-private-data-transfers-from-aws-s3-to-azure-blob/).

Currently in preview, this means your data never touches the public internet during migration. Traffic stays on private networks using Azure Private Link. For organizations with compliance requirements around data in transit, this removes a major blocker to cloud migration.

The practical scenario? You're migrating sensitive data from AWS to Azure - patient records, financial data, anything covered by strict data handling regulations. Storage Mover now lets you do that migration over private connections, maintaining your security posture throughout the entire process.

No more explaining to security teams why migration data briefly lives on the public internet. No more building complex VPN tunnels or ExpressRoute configurations just to move data. Storage Mover handles it.

## Developer Tools: Query Profiler for SQL in VS Code

If you're developing SQL database applications and using Visual Studio Code, the [Query Profiler in the MSSQL extension](https://azure.microsoft.com/en-au/updates/public-preview-query-profiler-in-mssql-extension-for-visual-studio-code/) just entered preview. This brings query performance analysis directly into your editor.

No more switching to SQL Server Management Studio or Azure Data Studio just to profile a query. Run your query in VS Code, see the execution plan, identify bottlenecks, optimize, and test again - all without leaving your development environment.

For developers who live in VS Code, this is one less context switch. And context switches are expensive - not in compute terms, but in "wait, what was I doing?" terms.

## Azure SRE Agent: AI-Powered Operations Hit General Availability

The [Azure SRE Agent with new capabilities](https://azure.microsoft.com/en-au/updates/generally-available-azure-sre-agent-with-new-capabilities/) reached GA this week. This is Microsoft's bet on AI-assisted site reliability engineering - an agent that helps you troubleshoot, diagnose, and resolve operational issues.

The new capabilities expand what the agent can do beyond basic diagnostics. We're talking root cause analysis, automated remediation suggestions, and integration with Azure Monitor and Application Insights for context-aware recommendations.

Is it going to replace your SRE team? No. Will it help your on-call engineer at 2 AM figure out why that service is throwing 500 errors? Probably. Think of it as having a really knowledgeable colleague who never sleeps and has read every Azure troubleshooting guide ever written.

## Heads Up: Policy Changes Coming in April

A quick heads-up for those using Azure Policy's faster enforcement feature: [the login/logout workaround is being retired in April 2026](https://azure.microsoft.com/en-au/updates/retirement-azure-policy-faster-enforcement-and-retirement-of-loginlogout-workaround/). If you're relying on that workaround for faster policy enforcement, now's the time to review your policy configuration and update to supported methods.

This isn't a critical breaking change for most organizations, but if you've got automation scripts that rely on this behavior, mark your calendar to update them before April hits.

## Bicep Corner: Still Riding the Snapshot Wave

On the Bicep front, v0.41.2 from a couple weeks ago continues to be the star. The snapshot command hitting GA means you can now confidently use it in production workflows for preview deployments and validation.

Meanwhile, v0.40.2 from January brought multi-line interpolated strings to GA - finally ending the era of concatenating strings across multiple lines with ugly syntax. Plus the MCP Server tools and .NET 10 migration set the foundation for future improvements.

No new releases this week, but that's fine. Sometimes you need time to actually use the features Microsoft ships before they ship more.

## What This Week Tells Us

Reading between the lines, Microsoft is doubling down on PostgreSQL as a first-class citizen on Azure. Three major updates in one week - IaC support, Grafana dashboards, and customer-managed keys - isn't coincidence. They're building PostgreSQL tooling and integration that matches what you'd expect for SQL Server.

The Databricks updates show Microsoft listening to operational feedback. Being able to update network configuration after deployment shouldn't be revolutionary, but in the world of managed services, it kind of is.

And Storage Mover getting private transfer support is Microsoft acknowledging that compliance-driven migrations are a different beast than "just move the data" migrations. Not everything can touch the public internet, and having that baked into the migration tool matters.

What are you most excited about from this week's updates? Hit me up and let me know if any of these solve problems you've been dealing with.

Until next week - keep building, keep shipping, and maybe give PostgreSQL another look if you haven't already.
