# 🌐 jleechanorg

✨ This meta-repository collects shared configuration for the organization and serves as a jumping-off point for all other public projects under **@jleechanorg**. Explore the highlights below to quickly find the automation framework or showcase build that fits your needs.

---

## 🚀 Flagship Systems

### 🤖 [claude-commands](https://github.com/jleechanorg/claude-commands)
- Automation backbone that scales Anthropic's Claude Code across heterogeneous environments.
- 150+ purpose-built slash commands compose MCP tools, shell scripts, and remote workflows into repeatable playbooks.
- Pipelines include queueing, rate limiting, observability hooks, and audit-friendly transcripts for full lifecycle coverage.
- Cross-platform setup guidance ensures Linux, macOS, and WSL contributors can bootstrap consistent workspaces in minutes.

### 🧩 [codex_plus](https://github.com/jleechanorg/codex_plus)
- Extends the stock Codex CLI with a FastAPI proxy that brokers long-running automations.
- Streaming gateways (built on `curl_cffi`) let Codex orchestrate builds, evals, and infrastructure changes without blocking.
- Bundled slash commands integrate log tailing, structured prompts, and rollback-safe checkpoints for reliable execution.
- Grafana-ready telemetry, request tracing, and alerting keep teams in control while gating risky mutations behind approvals.

### 📧 [mcp_mail](https://github.com/jleechanorg/mcp_mail)
- Multi-agent coordination system via async messaging (forked from [Dicklesworthstone/mcp_agent_mail](https://github.com/Dicklesworthstone/mcp_agent_mail)).
- **9 core enhancements** removing coordination barriers: 65% token reduction via lazy loading, global agent/message lookup across projects, automatic @mention scanning in unified inbox.
- Streamlined workflows: one-step agent registration with auto-project creation, contact-free messaging without approval gates.
- Projects as metadata only (not boundaries), enabling seamless cross-repo agent collaboration with flexible project keys.

### 🕸️ [ai_web_crawler](https://github.com/jleechanorg/ai_web_crawler)
- Node.js FastMCP façade with Python scraping workers for reliable traversal of the public web.
- Translates natural-language crawl intents into structured jobs that return deduplicated Markdown in real time.
- Built-in sanitizers strip tracking cruft and normalize typography, yielding clean corpora for downstream models.
- Operational resilience via caching, rate limits that respect robots.txt, and resumable streams for transient failures.

---

## 💼 Portfolio Highlights

| 🗂️ Repository | 🎯 Focus | ✨ Highlights |
| --- | --- | --- |
| [jleechan_fun](https://github.com/jleechanorg/jleechan_fun) | Sandbox experiments | Lightweight playground for quick ideas and creative prototypes. |
| [claude_llm_proxy](https://github.com/jleechanorg/claude_llm_proxy) | Claude CLI proxying | Unified installer connecting Claude Code CLI to Vast.ai, Cerebras Cloud, or local Ollama backends while preserving tool execution. |
| [claude_misc](https://github.com/jleechanorg/claude_misc) | WSL stability tooling | Scripts that monitor Claude Code memory use on WSL2, auto-restart the agent, and integrate with cron for persistent protection. |
| [snap_clone](https://github.com/jleechanorg/snap_clone) | Web Snapchat clone | React + Vite app rebuilding public Snapchat profile pages with metadata parsing and feature tab rendering. |
| [snap_ios_clone](https://github.com/jleechanorg/snap_ios_clone) | iOS Snapchat clone | SwiftUI + Firebase implementation covering camera UX, ephemeral messaging, stories, and MVVM architecture. |

> 🔍 Looking for something else? Explore the full organization at [github.com/jleechanorg](https://github.com/jleechanorg).
