# 🌐 jleechanorg

✨ This meta-repository collects shared configuration for the organization and serves as a jumping-off point for all other public projects under **@jleechanorg**. Explore the highlights below to quickly find the automation framework or showcase build that fits your needs.

---

## 🧠 Consensus ML

### [Consensus ML](https://consensus-ml.ai) - Multi-Model AI Consensus Platform

An intelligent orchestration platform that harnesses multiple AI models to achieve consensus-driven responses, combining the strengths of diverse LLMs for more reliable and balanced outputs.

**🔗 [Explore the Platform →](https://consensus-ml.ai)**

#### Core Technology Stack
- **Backend**: Python with FastAPI for high-performance async API handling
- **AI Integration**: Multi-provider support (OpenAI, Anthropic, Google, open-source models)
- **Consensus Engine**: Weighted voting and semantic similarity algorithms for response aggregation
- **Frontend**: React + TypeScript with real-time streaming responses

#### Key Features
- 🤝 **Multi-Model Consensus** - Query multiple LLMs simultaneously and synthesize unified responses
- ⚖️ **Weighted Voting** - Configurable confidence scoring across different model providers
- 🔄 **Fallback Chains** - Automatic failover between models for 99.9% uptime
- 📊 **Response Analytics** - Track model agreement rates and identify divergent outputs
- 🔌 **API-First Design** - RESTful endpoints for easy integration into existing workflows
- 🛡️ **Bias Mitigation** - Cross-model validation reduces single-model biases

---

## 🎮 WorldAI GenAI RPG

### [WorldArchitect.AI](https://github.com/jleechanorg/worldarchitect.ai) - AI-Powered Tabletop RPG Platform

Your Digital D&D 5e Game Master - an AI-powered tabletop RPG platform that generates dynamic narrative content, manages game state, and provides an immersive campaign experience.

**🎯 [Try the Live Demo →](https://mvp-site-app-stable-i6xf2p72ka-uc.a.run.app)**

#### Core Technology Stack
- **Backend**: Python 3.11 + Flask 2.x with Google Gemini AI integration
- **Database**: Firebase Firestore with real-time synchronization
- **Frontend**: Vanilla JavaScript + Bootstrap 5.x with multi-theme support (light/dark/fantasy/cyberpunk)
- **AI Pipeline**: Advanced prompt engineering with dual-pass generation, entity tracking, and model fallback

#### Key Features
- 🎭 **Interactive Story Generation** - Real-time AI-powered narrative with planning block enforcement
- ⚔️ **D&D 5e Mechanics** - Hybrid architecture combining rule-based validation with generative content
- 📊 **State Synchronization** - Explicit game state tracking with consistency validation
- 📄 **Multi-Format Export** - Campaign documents in PDF/DOCX/TXT for offline play
- 🎨 **Theme System** - 5 distinct visual themes with runtime switching
- 🔧 **MCP Architecture** - Model Context Protocol for clean separation of concerns

---

## 🚀 Flagship Systems

### 🤖 [claude-commands](https://github.com/jleechanorg/claude-commands)
Automation backbone that scales Anthropic's Claude Code across heterogeneous environments.
- 150+ purpose-built slash commands compose MCP tools, shell scripts, and remote workflows into repeatable playbooks.
- Pipelines include queueing, rate limiting, observability hooks, and audit-friendly transcripts for full lifecycle coverage.
- Cross-platform setup guidance ensures Linux, macOS, and WSL contributors can bootstrap consistent workspaces in minutes.

#### ⚡ [Orchestration Framework](https://github.com/jleechanorg/claude-commands/blob/main/.claude/commands/orchestrate.md)
Multi-agent orchestration system for complex development tasks using tmux-based agent management ([source](https://github.com/jleechanorg/claude-commands/tree/main/orchestration)):
- **Specialized Agents**: Frontend, backend, testing, and task-specific agents with complete isolation
- **Intelligent Reuse**: 50-80% efficiency gains through idle agent detection and strategic reuse
- **Real-time Coordination**: Redis-backed coordination with progress monitoring via `/orch status`
- **Natural Language Commands**: "Build X urgently", "connect to sonnet 1", "monitor agents"
- **Branch Isolation Protocol**: Agents work in dedicated worktrees preventing context contamination

#### 🔄 [GitHub PR Automation Framework](https://github.com/jleechanorg/claude-commands/blob/main/.claude/commands/automation.md)
Seamless CI/CD integration with intelligent PR processing ([PyPI: jleechanorg-pr-automation](https://pypi.org/project/jleechanorg-pr-automation/) | [source](https://github.com/jleechanorg/claude-commands/tree/main/automation)):
- **Actionable PR Detection**: Only processes PRs that need attention based on commit-based tracking
- **Safety Limits**: Built-in rate limiting (per-PR and global) with cross-process thread-safe persistence
- **Hook Integration**: Auto-triggers after push operations with full Claude Code workflow integration
- **Email Notifications**: Optional SMTP integration for automation alerts
- **TodoWrite Integration**: Tracks automation tasks with comprehensive progress reporting

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
