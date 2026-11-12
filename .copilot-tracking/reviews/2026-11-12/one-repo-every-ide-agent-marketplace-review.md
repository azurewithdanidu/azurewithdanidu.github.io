<!-- markdownlint-disable-file -->

# Review

## Requirements

* Topic: Central `agentz` marketplace across VS Code, Copilot CLI, Claude Code, and Cursor.
* Audience: Intermediate to advanced.
* Scope: One post.
* Code: Includes the Copilot CLI install flow and repository validation commands.
* Diagram: Includes a Mermaid quality-gate diagram and a TODO placeholder for the hero image.
* References: Links to the repository and official platform/spec documentation; no talk link.

## Checklist

* [x] Opens with "Howdy Folks,"
* [x] Uses complete Chirpy front matter and the date-specific `_posts/` filename.
* [x] Tags are lowercase and the SEO description is under 160 characters.
* [x] Technical claims were checked against official platform documentation and repository sources.
* [x] Includes direct documentation links.
* [x] Code fences specify languages.
* [x] Image uses the date-prefixed path pattern and includes a TODO placeholder.
* [x] Explains trade-offs and distinguishes the published Agent Plugins specification from product GA status.
* [x] Matches the requested intermediate-to-advanced audience.
* [x] Uses Danidu's conversational voice and ends with encouragement.
* [x] Avoids unsupported claims about GHES support, universal plugin limits, eval defaults, and branch-protection configuration.
* [x] States that generated files do not demonstrate successful runtime behavior in every client.

## Validation

* Python YAML parsing and targeted checks passed for the front matter, date, author, lowercase tags, description length, Mermaid flag/diagram, greeting, final newline, and trailing whitespace.
* `git diff --check` completed; the new post is untracked, so it was additionally checked for trailing whitespace with Python.
* Jekyll site build could not run because Ruby, Bundler, and Jekyll are not installed in the environment. No dependencies were installed because no dependency manifest changed.

## Status

Complete. The post is ready for review; replace the hero-image placeholder before publishing. Cross-client runtime installation tests remain outside this writing task.
