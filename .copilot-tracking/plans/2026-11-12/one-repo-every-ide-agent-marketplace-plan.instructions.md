<!-- markdownlint-disable-file -->

# One Repo, Every IDE: Blog Post Plan

## Requirements

* Topic: The `agentz` central agent-plugin marketplace at [azurewithdanidu/agentz](https://github.com/azurewithdanidu/agentz).
* Audience: Intermediate to advanced.
* Scope: One standalone post.
* Code: Keep practical CLI and repository script examples.
* Diagram: Add a Mermaid diagram for the CI, Copilot review, and CODEOWNERS gate; add a hero-image placeholder because no image was supplied.
* References: The repository plus official documentation links for platform-specific facts. No talk link for now.
* Date: 2026-11-12, Melbourne timezone (`+1100`).

## Editorial outline

1. Open with the duplication, quality, and trust problems caused by team-local copies of agent assets.
2. Introduce `agentz` and a Git repository as the marketplace.
3. Explain the core design: one source for behavior, generated client-specific manifests, and the difference between legacy Copilot layout and Agent Plugins 1.0.
4. Describe why skills are the portable center, while agents, commands, MCP configuration, and manifests need client-aware handling.
5. Walk through the publisher workflow, catalog, validation scripts, and eval expectations.
6. Explain the three layers of the quality gate, including the branch-instruction loophole and the need for CODEOWNERS review.
7. Cover duplicate detection and lessons from validating actual client behavior.
8. End with honest limitations, key takeaways, the repository link, and a concise invitation to adapt the pattern.

## Accuracy and review guardrails

* Call Agent Plugins 1.0 a published specification, not a universal GA product feature.
* State that Cursor documents Agent Plugins support, but do not claim identical runtime behavior across all clients.
* Distinguish source-format compatibility from the repository's generated manifests and client-specific support.
* Do not claim that Vally evals always block merges; their run is conditional on the configured token, and repository branch protection was not verified.
* Do not state GHES compatibility or universal marketplace capacity limits.
* Explain that repo structure and validation rules were confirmed by source inspection; successful installation/runtime behavior across all clients was not tested.

## Assets and front matter

* Filename: `_posts/2026-11-12-one-repo-every-ide-agent-marketplace.md`
* Categories: `[GitHub, Copilot]`
* Tags: `[github-copilot, claude-code, cursor, agent-plugins, ai-governance, platform-engineering]`
* Mermaid gate diagram; set `mermaid: true`.
* Hero image placeholder: `/assets/img/posts/2026-11-12-agentz-marketplace-quality-gate.png`.
