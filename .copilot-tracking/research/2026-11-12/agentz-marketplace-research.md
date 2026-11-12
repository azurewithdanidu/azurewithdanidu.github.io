<!-- markdownlint-disable-file -->

# Agentz Marketplace Technical Claims Research

## Scope and questions

Verify the attached draft's claims about the Agentz marketplace across VS Code, GitHub Copilot CLI, Claude Code, and Cursor. Prioritize current official documentation for:

- Supported manifest/layout formats and marketplace installation/discovery procedures.
- Version pinning and update semantics.
- Agent Plugins 1.0 specification, GA timing, and semantics.
- Generated Claude/Cursor manifests and interoperability of skills, agents, and commands.
- Marketplace limits and GitHub Enterprise Server (GHES) support.
- Public `azurewithdanidu/agentz` repository structure, scripts, gates, eval requirements, and CI.

Research only. Do not edit the blog post or other files. Repo-specific statements remain unverified until inspected.

## Findings

### Draft availability and scope

- The user supplied the draft as a session attachment, which was read by the parent agent. It was not present in the workspace's `_posts/` or `_drafts/` directories, so this note verifies the draft's claim areas and the public `agentz` repository rather than recording line-by-line annotations. Do not treat the repository README's claims as the draft's text.
- Public repo inspected: `azurewithdanidu/agentz`, branch `main`; GitHub API reported latest commit `9dbd75ad845b13132dbf942b4a611eb9cba2e96e` at 2026-11-11T14:18:50Z. Tree and key source files were read remotely. Repository-specific findings below are snapshot evidence, not independent proof of runtime behavior.

### Official platform/spec evidence

| Topic | Verified evidence and caveats |
|---|---|
| VS Code layouts | VS Code recognizes Agent Plugins 1.0 at root `plugin.json` with the canonical `$schema`, the legacy Copilot format at root `plugin.json` without that marker, Claude at `.claude-plugin/plugin.json`, and legacy OpenPlugin at `.plugin/plugin.json`. In the Copilot format, root `agents/`, `skills/`, `commands/`, and `.mcp.json` are supported conventions. In Agent Plugins 1.0, portable components are skills and MCP only; VS Code-specific agents/commands belong under `com.github.copilot/`. Thus “one layout is natively identical everywhere” is too broad; format markers change semantics. |
| Copilot CLI layouts and installation | CLI accepts both legacy Copilot and Agent Plugins manifests. `copilot plugin marketplace add OWNER/REPO`, `copilot plugin marketplace browse NAME`, and `copilot plugin install PLUGIN@MARKETPLACE` are current documented flows. It also accepts GitHub subdirectories, Git URLs and local paths. Marketplace catalog location for Copilot CLI is `.github/plugin/marketplace.json`; `marketplace.json` is the catalog and its `name` (not repository name) is the qualifier. |
| Claude Code format/install | A Claude plugin manifest is `.claude-plugin/plugin.json`; components stay at plugin root (`skills/`, `agents/`, `commands/`, etc.). A Claude marketplace is a repository/directory with `.claude-plugin/marketplace.json`. Shell/interactive flows include `claude plugin marketplace add ...`, `/plugin marketplace add ...`, and `/plugin install <name>@<marketplace>`; there are also install commands that combine add+install. Do not imply the Claude plugin marketplace is Anthropic's separate claude.com Marketplace directory. |
| Cursor formats/marketplaces | Cursor supports both Agent Plugins (root `plugin.json`: skills and MCP) and Cursor Plugins (`.cursor-plugin/plugin.json`: skills, MCP, rules, agents, commands, hooks and variables). Cursor plugin authoring docs support automatic folder discovery for those Cursor components. Team marketplaces can distribute either format; repo import/admin procedures are documented. Therefore generated Cursor manifests are a plausible adaptation, but they do not prove all source-format capabilities work unchanged in Cursor. Cursor docs explicitly say standard `${PLUGIN_ROOT}` / `${PLUGIN_DATA}` expansion is not supported in Cursor's `mcp.json`; use `${CURSOR_PLUGIN_ROOT}`. |
| Agent Plugins v1.0 status and scope | The normative specification states “Spec Version: 1.0.0” and “Status: Published.” The v1.0.0 Git tag metadata gives 2026-09-28T18:59:20Z. This establishes spec publication, not that every client feature called “plugins” is GA. VS Code's current documentation marks `chat.plugins.marketplaces` Experimental and the unified Customization Marketplace Preview. No official evidence located that assigns an overall GA date to the standard or makes all client plugin capabilities GA. |
| Agent Plugins 1.0 semantics | It is a package format/interoperability floor, not a universal plugin runtime or full feature parity promise. Root `plugin.json` must carry canonical schema URL; allowed portable manifest keys are closed; standard component types are skills in `skills/` and MCP config in root `mcp.json`. Other components (agents, commands, hooks, rules, LSP) are client extensions/namespaces. A client may support only some component types and ignores unsupported extensions. Plugin `version` is metadata clients **may** use for update availability/cache freshness, not a mandatory semver lock/pinning contract. |
| Skills/agents/commands interoperability | Agent Skills are an open standard and skills are portable subject to client-specific locations/features. This does not make plugins' agents or commands interoperable by default: Claude agent/subagent and command conventions, Cursor agent/command definitions, and Copilot-specific namespaces remain different. Claude Code calls a skill usable as a command, but that is not equivalent to a portable command specification. VS Code's own plugin reference says a supported package format does not guarantee every component works in every harness/client. |
| Version selection/update | VS Code marketplace source refs can be selected (`owner/repo#ref`); VS Code update action/automatic update behavior is controlled by editor settings, with npm/PyPI plugins excluded from auto-update. Copilot CLI marketplace add accepts refs; marketplace/plugin update commands exist, while custom marketplace auto-update is opt-in. Claude marketplace and plugin sources can use refs/SHAs; if manifest `version` is set and unchanged, Claude treats it as unchanged; omitting it for a Git-hosted marketplace allows commit-SHA tracking. Cursor documents manual refresh or GitHub Auto Refresh on pushes (at most once per 10 minutes); docs don't describe a version pin mechanism for team marketplaces. A marketplace Git ref and plugin semantic version are different controls; avoid conflating them. |
| Marketplace limits / GHES | Cursor documents a Teams-plan limit of one team marketplace; its Default marketplace does not count toward that imported-marketplace limit, so Teams can have Default plus one import. Enterprise lists unlimited team marketplaces. No numeric maximum for plugin count or marketplace count was found in the VS Code, Copilot CLI, or Claude Code pages inspected. This is “no published limit found,” not proof of unlimited scale. GitHub Copilot marketplace docs describe GitHub.com repositories, other Git hosts, and local directories; private GitHub marketplaces require repository read access. The pages inspected do not establish marketplace support on GitHub Enterprise Server (GHES), nor explicitly establish that it is unsupported. Treat a claim either way as unverified unless the exact surface/version and an official GHES source are cited. |

### Public `azurewithdanidu/agentz` repo (main snapshot)

- The tree confirms `.claude-plugin/marketplace.json`, generated `.github/plugin/marketplace.json` and `.cursor-plugin/marketplace.json`; `plugins/<name>/plugin.json`; `skills/`, `agents/`, `commands/`, optional `.mcp.json`, evals, and scripts. There are four marketplace plugins in the current catalog. README calls root plugin manifests the source and Claude/Cursor manifests generated.
- `scripts/sync_manifests.py` copies marketplace/catalog fields into the three marketplaces; emits `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and Cursor `mcp.json` from sources. It filters Cursor author fields to name/email and generates Cursor marketplace sources without `./`. `--check` detects stale generated files.
- `scripts/build_catalog.py` builds `catalog.json` and refreshes the README table; `--check` fails if stale. `marketplace_lib.py` maps canonical Claude catalog and generated Copilot/Cursor paths and sets legacy-layout expectations.
- `scripts/validate_repo.py` enforces marketplace entries/registered folders, legacy plugin manifest/name/semver/author requirements, MCP shape, README, CODEOWNERS line, at least one valid skill, skill naming/description length, agent and command frontmatter, secret-pattern scan, and eval rules. It calls both `sync_manifests.py --check` and `build_catalog.py --check`, so generated files and catalog/README table freshness are part of the structural gate. PR-only checks enforce version increase and duplicate similarity warnings. Its source explicitly disallows the Agent Plugins `$schema`/`extensions` and `com.github.copilot/` in this classic-layout repo; this is a project design choice, not a platform restriction.
- Eval gate encoded in validator: minimum 10 named stimuli; each with a prompt/turns and grader; at least three `skill-invocation.required` (positive) and two `.disallowed` (negative) cases; every skill must have a positive case. `vally lint` also runs in CI. The repo's docs say evals are 3 runs with threshold 0.7, but the workflow command itself only passes `--require-pass`; visible source here does not pass explicit run-count/threshold flags. Verify Vally defaults/config before stating those parameters are enforced.
- `.github/workflows/validate.yml` runs structural validation on PRs and main pushes; pinned Anthropic `claude plugin validate` (`@anthropic-ai/claude-code@2.1.317`); pinned Vally lint (`@microsoft/vally-cli@0.20.0`); and changed-plugin Vally evals on PRs only. Evals are skipped successfully with a warning and exit 0 if `COPILOT_GITHUB_TOKEN` is absent, so the README's “Yes” blocking status is conditional, not an unconditional required check. The duplicate check is a warning, not a blocker. Workflow does not itself enforce the documented Copilot code-review comments or CODEOWNERS approval; repository branch-protection/ruleset settings were not inspected.
- `docs/consuming-plugins.md` asserts Cursor loads skills/MCP and marks agent/command support “to be confirmed.” Current Cursor official reference says Cursor Plugins discover `agents/` and `commands/` by default, so that statement is stale/too cautious for a generated Cursor manifest that selects Cursor Plugin format. Validate the exact generated plugin in the Cursor client before asserting runtime success. The same doc's pin/update table is broadly consistent with platform docs: CLI marketplace add accepts `owner/repo#ref`, and plugin source objects can specify a full 40-character `sha`.
- `docs/plugin-standard.md` says Agent Plugins is read “only [by] the Copilot clients.” That is no longer accurate: Cursor's current official docs explicitly support Agent Plugins. The underlying design rationale (Agent Plugins 1.0 has no portable agents/commands, while Copilot's namespaced agent files are ignored by Claude) remains supported, but describes component-format tradeoffs, not which clients can read the standard.
- The repo's “consumed by four clients” assertion is supported as repository intent by its manifests, generation code, and client guides, but the source inspection did not execute installations in all four clients. Treat successful interoperability as a test claim until validated per client/version.

## References

### Official platform and standard sources

- VS Code Agent plugins overview, installation, updates, compatibility, marketplace settings (page footer date 2026-11-11): https://code.visualstudio.com/docs/agent-customization/agent-plugins
- VS Code Agent plugin authoring reference (formats, paths, marketplace source formats, versioning): https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference
- VS Code Agent Skills (standard and portability caveat): https://code.visualstudio.com/docs/agent-customization/agent-skills
- GitHub Copilot CLI find/install procedures: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing
- GitHub Copilot CLI plugin reference (legacy vs Agent Plugins, CLI locations, commands): https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference
- GitHub plugin/marketplace overview and catalog description: https://docs.github.com/en/copilot/concepts/customizations/plugins
- GitHub marketplace publishing procedure: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/create-and-share-plugin-marketplaces
- GitHub enterprise-managed marketplace/plugin policies: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/manage-plugin-marketplaces-and-plugins
- Agent Plugins 1.0.0 normative spec: https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md
- Agent Plugins v1.0.0 tag: https://github.com/agentplugins/agent-plugins-spec/releases/tag/v1.0.0
- Agent Plugins overview: https://agent-plugins.org/
- Claude Code plugins overview: https://code.claude.com/docs/en/plugins
- Claude Code plugin manifest reference: https://code.claude.com/docs/en/plugins/manifest-reference
- Claude Code plugin install/manage: https://code.claude.com/docs/en/plugins/install
- Claude Code create plugin/layout: https://code.claude.com/docs/en/plugins/create
- Claude Code marketplace distribution/versioning: https://code.claude.com/docs/en/plugins/publish
- Claude Code plugin components (skills, commands, subagents): https://code.claude.com/docs/en/plugins/components
- Cursor plugin guide (marketplaces, imports, update behavior, team limits): https://cursor.com/docs/plugins
- Cursor plugin manifest/layout reference: https://cursor.com/docs/reference/plugins

### Repository evidence

- Repository root/README: https://github.com/azurewithdanidu/agentz
- Marketplace docs: https://github.com/azurewithdanidu/agentz/blob/main/docs/consuming-plugins.md
- Publishing standard: https://github.com/azurewithdanidu/agentz/blob/main/docs/plugin-standard.md
- Validator: https://github.com/azurewithdanidu/agentz/blob/main/scripts/validate_repo.py
- Manifest generator: https://github.com/azurewithdanidu/agentz/blob/main/scripts/sync_manifests.py
- Catalog generator: https://github.com/azurewithdanidu/agentz/blob/main/scripts/build_catalog.py
- Workflow: https://github.com/azurewithdanidu/agentz/blob/main/.github/workflows/validate.yml
- Eval instruction: https://github.com/azurewithdanidu/agentz/blob/main/.github/instructions/plugin-evals.instructions.md
- Canonical Claude marketplace manifest: https://github.com/azurewithdanidu/agentz/blob/main/.claude-plugin/marketplace.json
- Generated Copilot marketplace manifest: https://github.com/azurewithdanidu/agentz/blob/main/.github/plugin/marketplace.json
- Generated Cursor marketplace manifest: https://github.com/azurewithdanidu/agentz/blob/main/.cursor-plugin/marketplace.json

## Unresolved items

- Establish GHES compatibility/limitations for each specific client and version from an explicit official GHES source; sources accessed here are GitHub.com Copilot documentation and do not settle that question.
- Verify Vally eval execution defaults (repetitions and pass threshold) and whether repository branch protection requires the reported workflow checks/approvals; source workflow shows a successful skip when the token is unset, and repository settings were unavailable.
- Distinguish the spec's publication date (v1.0.0 tag: 2026-09-28T18:59:20Z) from any product-specific GA date. No universal Agent Plugins or marketplace-product GA date was found in the official docs inspected.

The post will not make claims about GHES support, Vally's default repetitions or threshold, or configured branch-protection rules. It will describe the documented Cursor Teams/Enterprise marketplace limits with a note that plans and limits can change.
