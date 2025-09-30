# jleechanorg .github

This meta-repository collects shared configuration for the organization and serves as a jumping-off point for all other public projects under **@jleechanorg**.

## Flagship Systems

### [claude-commands](https://github.com/jleechanorg/claude-commands)
Claude Commands is the automation backbone for scaling Anthropic's Claude Code across heterogeneous environments. The repository documents more than 150 purpose-built slash commands that compose MCP tools, shell scripts, and remote workflows into repeatable playbooks. It covers the full lifecycle from project discovery through scoped planning, implementation, validation, and post-launch QA hand-off so assistants can run autonomous delivery loops without bespoke operator oversight.

Beyond raw command listings, the project explains how to stitch commands together into guardrailed pipelines with queueing, rate limiting, and audit-friendly transcripts. Observability hooks surface live progress to human reviewers and feed retrospective analytics that inform new automations. The guide also walks through environment setup for Linux, macOS, and Windows Subsystem for Linux, ensuring contributors can bootstrap a consistent workspace in minutes.

### [codex_plus](https://github.com/jleechanorg/codex_plus)
Codex Plus extends the stock Codex CLI with a FastAPI proxy that brokers long-running automations. It introduces streaming gateways built on `curl_cffi`, letting Codex orchestrate build pipelines, eval suites, and infrastructure changes without blocking. The project bundles curated slash commands for recurring operations, integrating log tailing, structured prompts, and rollback-safe task checkpoints.

To keep teams in control, Codex Plus layers Grafana-ready telemetry, request tracing, and alerting into every command path. Contributors will find guidance on provisioning remote execution sandboxes, gating risky mutations behind human approvals, and composing advanced workflows that chain Claude and Codex capabilities. Companion examples illustrate how to retrofit existing tools with the proxy to gain observability without rewriting automation logic.

### [ralph-orchestrator](https://github.com/jleechanorg/ralph-orchestrator)
Ralph Orchestrator unifies Claude, Q Chat, and Gemini agents into a single mission-control plane for complex delivery programs. It ships an evented job graph that coordinates discovery, build-out, QA, and launch readiness, capturing intermediate artifacts as versioned checkpoints so teams can resume or audit any stage mid-stream. The scheduler supports both cron-like cadences and reactive triggers, making it equally comfortable driving routine maintenance or urgent incident response.

Reliability features include per-agent sandbox isolation, circuit breakers that downgrade misbehaving connectors, and human-in-the-loop sign-offs for production changes. The repository documents how to extend the orchestrator with bespoke adapters, wire in observability exporters, and tune retry policies for latency-sensitive operations. Example playbooks show Ralph delegating to Claude Commands and Codex Plus, demonstrating how the flagship systems interoperate to deliver end-to-end automation.

### [ai_web_crawler](https://github.com/jleechanorg/ai_web_crawler)
The AI Web Crawler pairs a Node.js FastMCP façade with Python scraping workers to give agents a reliable way to traverse the public web. It translates natural-language crawl intents into structured jobs, fetches sitemaps or arbitrary URLs, and emits deduplicated Markdown back to clients in real time. Built-in sanitizers strip tracking cruft, collapse navigation noise, and normalize typography so downstream models ingest clean corpora.

Operational resilience is a core focus: caching layers prevent redundant fetches, rate-limit guards respect robots.txt and remote policies, and resumable streams survive transient network failures. Extensive docs outline the data-contracts used by Claude, GPT, and other MCP-compatible agents, while deployment notes cover containerization, secret management, and monitoring hooks for production rollouts.

## Portfolio Highlights

| Repository | Focus | Highlights |
| --- | --- | --- |
| [jleechan_fun](https://github.com/jleechanorg/jleechan_fun) | Sandbox experiments | Lightweight playground for quick ideas and creative prototypes. |
| [claude_llm_proxy](https://github.com/jleechanorg/claude_llm_proxy) | Claude CLI proxying | Unified installer connecting Claude Code CLI to Vast.ai, Cerebras Cloud, or local Ollama backends while preserving tool execution. |
| [claude_misc](https://github.com/jleechanorg/claude_misc) | WSL stability tooling | Scripts that monitor Claude Code memory use on WSL2, auto-restart the agent, and integrate with cron for persistent protection. |
| [snap_clone](https://github.com/jleechanorg/snap_clone) | Web Snapchat clone | React + Vite app rebuilding public Snapchat profile pages with metadata parsing and feature tab rendering. |
| [snap_ios_clone](https://github.com/jleechanorg/snap_ios_clone) | iOS Snapchat clone | SwiftUI + Firebase implementation covering camera UX, ephemeral messaging, stories, and MVVM architecture. |

> Looking for something else? Explore the full organization at [github.com/jleechanorg](https://github.com/jleechanorg).
