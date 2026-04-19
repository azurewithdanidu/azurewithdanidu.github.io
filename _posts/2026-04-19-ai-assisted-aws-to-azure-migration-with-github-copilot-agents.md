---
title: "AI-Assisted AWS to Azure Migration with GitHub Copilot Agents"
date: 2026-04-19 09:00:00 +1000
categories: [Azure, Migration]
tags: [azure, aws, migration, github-copilot, ai, github-actions, azure-functions, bicep]
description: "How I built a framework of custom GitHub Copilot agents that automate the full AWS-to-Azure migration pipeline — from live account discovery through architecture design, code refactoring, IaC generation, and deployment validation."
author: danidu
toc: true
comments: true
pin: false
mermaid: false
math: false
image:
  path: /assets/img/posts/2026-04-19-aws-azure-migration-copilot-agents.jpg
  alt: "AI-Assisted AWS to Azure Migration with GitHub Copilot Agents — One Prompt, Full Pipeline"
---

Howdy Folks,

Cloud migrations are hard. Not because the technology is hard — Azure and AWS have well-documented service equivalents, the tooling is mature, and the patterns are well understood. Migrations are hard because of **scale, consistency, and human error at each handoff**. A typical AWS-to-Azure migration involves at least five distinct disciplines: infrastructure discovery, architecture design, application code refactoring, IaC generation, and CI/CD pipeline setup. Each phase is usually handled by a different person or team, and context gets lost at every boundary.

So here's the question I kept asking myself: what if a single prompt could kick off the entire pipeline?

In this post, I'll walk you through a framework I built using **custom GitHub Copilot agents** — eight purpose-built agents that run entirely inside VS Code, orchestrated by a project manager agent, covering the full migration lifecycle from a live AWS account all the way to a passing deployment validation report on Azure. No external scripts, no stitching together CLI pipelines. Just agents, MCP servers, and well-crafted instructions.

Let's dive in.

---

## The Problem: Migration at Scale

Let's paint a realistic picture. Your organisation has a workload running on AWS — Lambda functions, S3 buckets, API Gateway, CloudFormation stacks. Management has decided to migrate to Azure. You have a team of engineers, a deadline, and a long list of decisions to make:

- Which AWS services map to which Azure equivalents?
- How do you re-platform Python Lambda functions to Azure Functions without breaking the application logic?
- How do you generate production-grade Bicep from CloudFormation without writing it from scratch?
- How do you ensure the CI/CD pipelines use OIDC and not long-lived credentials?
- How do you validate that all generated artefacts are consistent with each other before anyone touches the deploy button?

The traditional answer is: lots of meetings, lots of documents, and lots of manual effort. The answer I landed on: **a framework of custom GitHub Copilot agents backed by MCP servers**.

---

## The Framework at a Glance

The framework consists of **eight custom Copilot agents**, each with a single responsibility, backed by their own instruction files and connected to MCP servers for live data access. They are organised into four sequential phases, with Phase 3 running three agents in parallel.

![Agent Orchestration — One Prompt, Full Pipeline](/assets/img/posts/2026-04-19-aws-azure-migration-copilot-agents.jpg)

| Agent | Phase | Responsibility |
|---|---|---|
| `@migration-project-manager` | Orchestrator | Runs all phases in order, verifies artefacts, maintains task plan |
| `@aws-discovery` | 1 — Discovery | Read-only AWS resource enumeration via MCP |
| `@aws-discovery-skills` | 1 — Discovery | Alternative: uses CLI skill instead of MCP |
| `@azure-architect` | 2 — Architecture | AWS-to-Azure mapping, design document, Mermaid diagrams |
| `@iac-transformation` | 3a — IaC | CloudFormation → Bicep (AVM modules) |
| `@code-refactor` | 3b — Code | Lambda → Azure Functions v2 (Python 3.11, decorator model) |
| `@pipeline-builder-agent` | 3c — Pipelines | GitHub Actions CI/CD with OIDC / Workload Identity Federation |
| `@deployment-validation` | 4 — Validation | 15-point static checklist across all generated artefacts |

The whole thing is triggered with a single prompt to the orchestrator:

```
@migration-project-manager Run the full migration pipeline for AWS account <your-account-id>
```

Or if you want to drive individual phases:

```
@aws-discovery Discover all resources in AWS account 535002891143 and produce the inventory artifacts

@azure-architect Design Azure architecture based on the discovery outputs in outputs/aws-migration-artifacts/

@iac-transformation Convert the CloudFormation template to Bicep using AVM modules

@code-refactor Refactor all Lambda functions to Azure Functions v2 (Python 3.11)

@pipeline-builder-agent Create GitHub Actions CI/CD pipelines for infra, functions, and static web app

@deployment-validation Validate all generated artifacts and produce a validation report
```

---

## Phase 1: Discovery

![Phase 1: AWS Discovery](/assets/img/posts/2026-04-19-aws-azure-migration-phase1-discovery.jpg)

The `@aws-discovery` agent performs **read-only enumeration** of a live AWS account using the **AWS Cloud Control API MCP server**. No CLI, no scripts — just MCP tool calls inside the agent context window. It scans all enabled regions and produces four output artefacts:

| Artefact | What it contains |
|---|---|
| `aws-inventory.json` | Complete resource list: every resource type, region, ARN, and metadata |
| `architecture-diagram.mmd` | Mermaid diagram of the AWS topology (services, connections, tiers) |
| `dependency-matrix.csv` | Service dependency relationships (e.g., Lambda → S3, Lambda → API GW) |
| `migration-assessment.md` | Complexity ratings and effort estimates per service |
| `cloudformation-template.yaml` | Captured CloudFormation stack template for direct conversion |

The decision to use **MCP instead of CLI** was deliberate. CLI commands require credentials configured on the host machine, produce unstructured text output that agents need to parse, and aren't portable across operating systems. MCP gives the agent structured JSON responses directly, keeps the agent logic clean, and works identically on any platform where VS Code runs.

If you don't have the AWS Cloud Control API MCP server configured, there's an alternative: `@aws-discovery-skills`, which uses a built-in SKILL.md that defines a comprehensive CLI-based discovery workflow as a fallback. That agent uses **no MCP servers** at all — it drives discovery entirely through AWS CLI commands via the `execute` tool.

**MCP tools declared in `aws-discovery.agent.md`:**

```yaml
tools:
  - aws-api-mcp-server/*   # AWS Cloud Control API — full resource enumeration across all regions
  - aws-knowledge-mcp/*    # AWS service documentation lookups
  - azure-mcp/search       # Azure region and service availability checks
```

> The `@aws-discovery` agent is **strictly read-only**. It makes zero write calls. The agent instructions explicitly prohibit any mutation operations.
{: .prompt-info }

---

## Phase 2: Architecture Design

![Phase 2: Azure Architecture Design](/assets/img/posts/2026-04-19-aws-azure-migration-phase2-architecture.jpg)

The `@azure-architect` agent reads the Phase 1 artefacts and produces a complete Azure architecture design. It uses the **Microsoft Learn MCP server** to validate service equivalents against current documentation and the **Mermaid Chart MCP server** to generate and syntax-validate diagrams.

The design document covers 11 sections — service mapping, network topology, security posture, identity model, cost comparison, HA/DR strategy, and deployment approach. The key outputs are:

- `design-document.md` — the full architecture narrative
- `architecture-diagram-azure.mmd` — Mermaid diagram of the target Azure topology
- `service-mapping.md` — explicit AWS → Azure service equivalence table
- `cost-comparison.md` — rough cost modelling for the target architecture

**MCP tools declared in `azure-architect.agent.md`:**

```yaml
tools:
  - aws-knowledge-mcp/*                                          # AWS service docs (source-side mapping)
  - microsoftdocs/mcp/*                                          # Microsoft Learn — Azure docs + AVM modules
  - azure-mcp/documentation                                      # Azure service documentation
  - azure-mcp/search                                             # Azure resource/service search
  - mermaidchart.vscode-mermaid-chart/get_syntax_docs            # Mermaid syntax reference
  - mermaidchart.vscode-mermaid-chart/mermaid-diagram-validator  # Validates every .mmd file before writing
  - mermaidchart.vscode-mermaid-chart/mermaid-diagram-preview    # Previews rendered diagrams inline
```

> The three `mermaidchart` tools come from the **Mermaid Chart VS Code extension** — not a remote MCP server. The agent uses them to validate every diagram it generates before writing the `.mmd` file to disk.
{: .prompt-info }

### The APIM Decision

One of the most common over-engineering pitfalls in migrations is the reflexive addition of **Azure API Management (APIM)** as the equivalent of AWS API Gateway. APIM is a powerful product — it gives you rate limiting, request transformation, a developer portal, and policy enforcement. But it also starts at roughly $150/month for the Developer tier and adds significant operational complexity.

For migrations where the original AWS API Gateway is simply fronting Lambda functions (a very common pattern), **Azure Functions HTTP triggers are a direct equivalent**. There's no meaningful gap in capability, and HTTP triggers are included in the Consumption plan's free grant.

The architecture instructions in this framework explicitly call this out: add APIM only when gateway-layer features are explicitly required. This saved the sample migration roughly $1,800/year.

---

## Phase 3: Parallel Execution

Phase 3 runs three agents concurrently. Each has a specific input/output contract and writes to its own output folder, so there are no interference risks.

### 3a — IaC Transformation: CloudFormation → Bicep

The `@iac-transformation` agent converts the captured CloudFormation template to modular Azure Bicep using **Azure Verified Modules (AVM)** where available. The output structure is:

```
outputs/bicep-templates/
  main.bicep              # Subscription-scoped root
  modules/
    storage.bicep
    functions.bicep
    staticwebapp.bicep
    appinsights.bicep
    keyvault.bicep
    rbac.bicep
  parameters/
    dev.bicepparam
    staging.bicepparam
    prod.bicepparam
```

The agent uses the **Microsoft Learn MCP server** to look up current AVM module references during generation — no hardcoded module versions.

**MCP tools declared in `iac-transformation.agent.md`:**

```yaml
tools:
  - aws-knowledge-mcp/*   # AWS CloudFormation service and resource docs
  - microsoftdocs/mcp/*   # Microsoft Learn — AVM module references and Bicep docs
  - azure-mcp/*           # Full Azure MCP access (resource info, service lookups)
```

### 3b — Code Refactor: Lambda → Azure Functions

The `@code-refactor` agent re-writes Python Lambda handlers to the **Azure Functions v2 decorator model**. The critical decisions here are:

**Identity**: AWS Lambda uses execution roles (IAM). Azure Functions uses **System-Assigned Managed Identity** with RBAC. The refactored code replaces all `boto3` calls with `azure-storage-blob` + `azure-identity`, using `DefaultAzureCredential` for local dev and Managed Identity in production. Zero credentials in environment variables.

**Pre-signed URL → SAS Token**: The pre-signed URL pattern from S3 maps cleanly to Azure Blob **SAS tokens using user-delegation keys** (generated via `get_user_delegation_key()` from `BlobServiceClient`). The client-side upload/download path is preserved — clients still talk directly to storage; the API generates short-lived tokens. The key detail: use user-delegation SAS (Managed Identity path) rather than account-key SAS.

**Environment variables**: One lesson learned the hard way — `CONTAINER_NAME` is a reserved environment variable in the Azure Functions host. Renaming it to `BLOB_CONTAINER_NAME` is not optional.

**MCP tools declared in `code-refactor.agent.md`:**

```yaml
tools:
  - aws-knowledge-mcp/*                          # boto3 API docs — source SDK reference
  - microsoftdocs/mcp/*                          # azure-storage-blob and azure-identity SDK docs
  - ms-python.python/getPythonEnvironmentInfo    # Inspect local Python virtual environments
  - ms-python.python/getPythonExecutableCommand  # Locate the correct Python 3.11 executable
  - ms-python.python/installPythonPackage        # Install azure-* packages into .venv
  - ms-python.python/configurePythonEnvironment  # Set interpreter path for the workspace
```

> The `ms-python.python/*` entries are **VS Code Python extension tools**, not external MCP servers. They let the agent manage the local virtual environment directly without shelling out raw CLI commands.
{: .prompt-info }

### 3c — Pipeline Builder: GitHub Actions with OIDC

The `@pipeline-builder-agent` generates three GitHub Actions workflows:

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy-infra.yml` | push to `main` (`bicep-templates/**`) | `az deployment sub validate` → what-if → deploy |
| `deploy-functions.yml` | push to `main` (`azure-functions/**`) | pip install, zip deploy, smoke test, rollback on failure |
| `deploy-static-web.yml` | push to `main` (`static-web-app/**`) | Azure/static-web-apps-deploy@v1, skip_app_build: true |

Authentication uses **OIDC / Workload Identity Federation** throughout — no client secrets, no expiry dates, no rotation. The Bicep deployment uses subscription scope (`az deployment sub create`) to handle resource group creation as part of the IaC lifecycle.

The `deploy-infra.yml` what-if step is surfaced as a pull request comment when triggered from a PR, giving you a diff of planned changes before the merge button is touched. Environment gates enforce: dev auto-deploys; staging requires 1 reviewer; prod requires 2 reviewers.

**MCP tools declared in `pipeline-builder-agent.agent.md`:**

```yaml
tools:
  - azure-mcp/search   # Looks up Azure service names, regions, and resource IDs for workflow config
```

---

## Phase 4: Deployment Validation

The `@deployment-validation` agent runs a **15-point static validation checklist** across all generated artefacts from Phases 1–3:

1. Bicep template syntax (via `az bicep build`)
2. AVM module version pinning
3. Environment parameter completeness
4. Managed Identity — no hardcoded credentials
5. RBAC scope correctness — least privilege
6. Key Vault soft-delete and purge protection
7. Storage — public blob access disabled
8. GitHub Actions OIDC — no stored client secrets
9. Smoke test coverage (HTTP trigger endpoints)
10. AWS→Azure functional parity (resource-by-resource)
11. Application Insights instrumentation
12. Python 3.11 runtime declared (not 3.12/3.13)
13. `staticwebapp.config.json` routing rules present
14. Dependency-matrix cross-referenced against Bicep outputs
15. Azure Policy compliance (naming conventions, tagging)

The output is `outputs/validation-report.md` — a structured report with pass/fail status per check plus remediation notes for any failures. The sample migration ran 15/15.

> This agent has **no MCP tools declared**. It works entirely from artefacts already on disk — no network calls, no MCP server dependency. That makes validation fast and reliable regardless of MCP server availability.
{: .prompt-info }

---

## The Orchestrator: `@migration-project-manager`

If the four phases are the engine, the `@migration-project-manager` is the icing on the cake. It's the agent that turns a collection of capable specialists into a single automated pipeline you can trigger with one prompt.

```
@migration-project-manager Run the full migration pipeline for AWS account <your-account-id>
```

That's it. One prompt. The project manager then:

1. **Invokes `@aws-discovery`** — waits for all five artefacts to appear in `outputs/aws-migration-artifacts/` before proceeding
2. **Invokes `@azure-architect`** — waits for `design-document.md`, `architecture-diagram-azure.mmd`, `service-mapping.md`, and `cost-comparison.md` before proceeding
3. **Invokes `@iac-transformation`, `@code-refactor`, and `@pipeline-builder-agent` in parallel** — all three run concurrently since they write to separate output folders with no shared state
4. **Invokes `@deployment-validation`** — only after all three Phase 3 agents have completed and their artefacts are verified

At each boundary, the orchestrator **reads the output folder** and verifies the expected artefacts exist before calling the next agent. If something is missing, it surfaces a clear blocker to the user rather than letting a downstream agent run against incomplete inputs.

Throughout the run, it maintains a live task plan at `outputs/migration-task-plan.md` — a structured Markdown file that logs phase status, completed tasks, and any blockers. This is what feeds the Visualizer dashboard.

**MCP tools declared in `migration-project-manager.agent.md`:**

```yaml
tools:
  - read     # reads artefact files to verify phase completion
  - edit     # writes and updates outputs/migration-task-plan.md
  - agent    # delegates to all specialist agents
  - search   # searches the outputs/ folder for artefacts
  - todo     # tracks in-progress tasks
```

Notice what's **not** in that list: no MCP servers whatsoever. The orchestrator has deliberately zero external dependencies. It reads files, delegates to agents, and verifies outputs. All the real work — and all the MCP server calls — happens inside the specialist agents it invokes. This is intentional: a lightweight coordinator should never be blocked by an unavailable MCP server.

> You can also start from a specific phase if a previous run partially completed: `@migration-project-manager Resume from architecture phase`. The agent will re-verify existing artefacts and pick up from the correct point.
{: .prompt-tip }

---

## The Visualizer: A Live Migration Dashboard

The repository ships with a **Vite-powered single-page web app** that gives you a real-time view of migration progress.

```bash
cd visualizer
npm install
npm run dev
# Opens at http://localhost:5173
```

It reads `outputs/migration-task-plan.md` (maintained by the orchestrator agent during a live run), renders phase cards with status badges, lets you open any generated artefact in the browser directly, and renders the AWS and Azure Mermaid diagrams side-by-side. A 30-second auto-refresh countdown keeps it live as agents are running.

---

## Design Principles: The Decisions That Matter

### Agents Don't Use CLI — They Use MCP

Every agent in this framework uses **MCP servers** for data access, not shell commands. This keeps agents portable (no OS assumptions), keeps output structured (JSON, not unstructured text), and keeps the agent logic clean (no regex parsing of CLI output).

The MCP servers in use:

| MCP Server | Used by | Purpose |
|---|---|---|
| AWS Cloud Control API MCP | `@aws-discovery` | Read-only AWS resource enumeration |
| AWS Knowledge MCP | `@aws-discovery`, `@azure-architect`, `@code-refactor` | AWS service documentation |
| Microsoft Learn MCP | `@azure-architect`, `@iac-transformation`, `@code-refactor` | Azure docs and AVM references |
| Azure MCP | `@azure-architect`, `@iac-transformation`, `@deployment-validation` | Live Azure resource information |
| Mermaid Chart MCP | `@azure-architect` | Diagram generation and syntax validation |

### Managed Identity Replaces All IAM Keys

AWS IAM roles and access keys are replaced — unconditionally — by **Azure System-Assigned Managed Identity** with fine-grained RBAC. The code refactor agent is instructed to fail validation if it finds any storage account keys or connection strings in the refactored output.

### Bicep Is Subscription-Scoped

Rather than resource-group-scoped templates (which require the resource group to pre-exist), the generated Bicep uses **subscription scope**. The `main.bicep` creates the resource group as part of the deployment. This makes the templates genuinely self-contained: a fresh subscription is sufficient to run a full deployment.

### The Pre-Signed URL Pattern Is Preserved

This was a key architectural decision. The original AWS application used S3 pre-signed URLs so that clients upload/download directly to S3 — no proxying through the API, no Lambda bandwidth cost. This pattern maps cleanly to Azure Blob **SAS tokens with user-delegation keys**. The API generates tokens; clients use them directly against Blob Storage. The same cost and performance characteristics carry over.

---

## Known Gotchas — Lessons from the First Run

These issues were all encountered during the first migration run. They're now baked into the agent instructions so future runs don't hit them.

**Python version.** Azure Functions v4 supports Python 3.9, 3.10, and 3.11 only. Python 3.12 and 3.13 crash the worker with a `0xC0000005` Access Violation. Always create the venv with Python 3.11:

```bash
python3.11 -m venv .venv
```

**Reserved environment variable.** `CONTAINER_NAME` is reserved by the Azure Functions host. Using it causes silent failures in environment variable binding. Rename to `BLOB_CONTAINER_NAME`.

**Static Web Apps entry point.** Azure Static Web Apps requires `index.html` as the default file at the root. A standalone `app.html` is invisible without an explicit `staticwebapp.config.json` routing rule:

```json
{
  "navigationFallback": {
    "rewrite": "/index.html"
  }
}
```

**SAS token generation.** Use `get_user_delegation_key()` from `BlobServiceClient` (the Managed Identity path), not storage account keys. Account-key SAS tokens break the zero-credentials posture of the rest of the architecture.

**APIM is optional.** Don't add it reflexively. HTTP triggers cover the API Gateway pattern for most workloads.

---

## Key Takeaways

![Key Takeaways](/assets/img/posts/2026-04-19-aws-azure-migration-key-takeaways.jpg)

The framework is available on GitHub and is fully open. The agents are defined as `.agent.md` files in `.github/agents/`, backed by `.instructions.md` files in `.github/instructions/`. The `Sample-Migrations/` folder contains a complete worked example — an AWS serverless image upload service (4 Lambda functions + S3 + API Gateway + CloudFormation) migrated end-to-end to Azure.

A few things I'd emphasise for anyone thinking about using or adapting this framework:

**Agent instructions are the hard part.** Getting the agents to produce consistent, correct output across every run required careful iteration on the instruction files — specifying not just what to do but what *not* to do (no APIM, no account keys, no Python 3.12, no CLI inside agent flows). The instructions encode the lessons.

**MCP quality drives output quality.** The Microsoft Learn MCP server being able to pull current AVM module references during Bicep generation is what makes the IaC output actually usable. If your MCP servers are stale or unavailable, agent output degrades.

**Parallelism in Phase 3 works because of output contracts.** IaC, code refactor, and pipeline builder each write to distinct output folders and have no shared state during generation. The orchestrator verifies all three before Phase 4 begins.

**Validation is non-negotiable.** The 15-point checklist catches things that slip through even careful manual review — RBAC scope drift, missing purge protection on Key Vault, a smoke test endpoint that resolves to 404 because the route wasn't updated. Run it every time.

---

Hope this will help someone in need — whether you're planning a migration or just thinking about how to structure multi-agent AI workflows for complex engineering tasks. The full framework and sample migration are in the GitHub repository linked above.

Feel free to reach out if you have any questions. Until next time...!
