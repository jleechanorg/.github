# 🌐 jleechanorg

✨ This meta-repository collects shared configuration for the organization and serves as a jumping-off point for all other public projects under **@jleechanorg**. Explore the highlights below to quickly find the automation framework or showcase build that fits your needs.

## 📋 Table of Contents

- [🛠️ AI Development Recommendations](#%EF%B8%8F-ai-development-recommendations) - **Battle-tested AI coding toolchain**
- [🧠 Consensus ML](#-consensus-ml) - Multi-model AI consultation platform
- [🎮 WorldAI GenAI RPG](#-worldai-genai-rpg) - AI-powered tabletop RPG
- [🚀 Flagship Systems](#-flagship-systems)
  - [📧 mcp_mail](#-mcp_mail) - Multi-agent coordination
  - [🤖 claude-commands](#-claude-commands) - Claude Code automation
    - [⚡ Orchestration Framework](#-orchestration-framework)
    - [🔄 GitHub PR Automation](#-github-pr-automation-framework)
  - [🕸️ ai_web_crawler](#%EF%B8%8F-ai_web_crawler) - Web scraping MCP
- [💼 Portfolio Highlights](#-portfolio-highlights)

---

## 🛠️ AI Development Recommendations

### [ai_dev_recs](https://github.com/jleechanorg/ai_dev_recs) - Battle-Tested AI Coding Toolchain

**Evidence-based AI development toolchain recommendations from production usage at WorldArchitect.AI**

Based on 19,044 commits over 6 months running a production AI-powered D&D platform. This is NOT a "top 10 AI tools" listicle - it's a battle-tested toolchain extracted from actual production usage, backed by git commit evidence and real workflow patterns.

**🔗 [View the Recommendations →](https://github.com/jleechanorg/ai_dev_recs)**

#### What's Inside

- ✅ **19 Tools** - Claude Code CLI, pytest, gh CLI, Gemini, beads, tmux, Cursor, Warp, Docker, and more
- ✅ **10 MCP Servers** - Multi-agent coordination, testing, Chrome automation
- ✅ **80+ Custom Commands** - `/copilot`, `/fixpr`, `/redgreen`, `/fake`, and specialized workflows
- ✅ **Multi-Agent Orchestration** - 4 AI agents (copilot, cursor, codex, claude) working autonomously
- ✅ **Automatic Quality Gates** - `/fake` hook catches speculative code (15% catch rate, 343 checks/month)
- ✅ **12-Step Development Workflow** - Complete lifecycle from planning to deployment

#### Key Metrics

- 📊 **19,044 commits analyzed** (6 months of production usage)
- 🧪 **17.4% test coverage** (3,308 testing commits)
- 🤖 **7,950 /copilot invocations** (PR automation)
- 🔍 **343 automatic code quality checks** (via /fake hook)
- 💰 **$40-60/month** (cost-conscious AI development)

#### Documentation

- [**README.md**](https://github.com/jleechanorg/ai_dev_recs/blob/main/README.md) - Executive summary of all 19 tools
- [**TOOLCHAIN.md**](https://github.com/jleechanorg/ai_dev_recs/blob/main/TOOLCHAIN.md) - Complete tool inventory with evidence scores
- [**WORKFLOWS.md**](https://github.com/jleechanorg/ai_dev_recs/blob/main/WORKFLOWS.md) - 12-step multi-AI development workflow
- [**FAKE_HOOK_ANALYSIS.md**](https://github.com/jleechanorg/ai_dev_recs/blob/main/FAKE_HOOK_ANALYSIS.md) - Automatic code quality gate analysis
- [**SETUP_GUIDE.md**](https://github.com/jleechanorg/ai_dev_recs/blob/main/SETUP_GUIDE.md) - Installation instructions

**Who This Is For**: Developers using Claude Code, Cursor, or other AI coding tools who want to see real production patterns with evidence-based recommendations.

---

## 🧠 Consensus ML

### [Consensus ML](https://consensus-ml.ai) - Multi-Model AI Consultation Platform

Ask one question, receive synthesized analysis from 5 major AI models (Cerebras, Claude Sonnet 4, Gemini 2.5 Flash, Perplexity Sonar, Grok) with consensus, divergent perspectives, and comprehensive coverage highlighted. Research shows multi-model approaches reduce hallucinations by 60% and outperform single models.

**🔗 [Explore the Platform →](https://consensus-ml.ai)**

#### Core Technology Stack
- **Backend**: TypeScript FastMCP HTTP/STDIO server + Express middleware
- **Frontend**: React 19 + TypeScript + Vite with Tailwind CSS
- **Conversations**: Dedicated MCP server for conversation persistence
- **Architecture**: "MCP all the way down" - separate services communicate via Model Context Protocol
- **Infrastructure**: Google Cloud Run, Firebase Auth, Firestore persistence, Secret Manager

#### Key Features
- 🤝 **2-Round Parallel Architecture** - Round 1: All models execute in parallel (~22s), Round 2: Cerebras synthesizes insights (~8s)
- ⚡ **Cost Efficiency** - Cerebras synthesis at ~$0.60/M tokens vs $5-20/M for premium models
- 📦 **Published npm Packages** - Reusable `@ai-universe/*` packages for MCP-based applications
- 🔄 **Dual Transport** - FastMCP HTTP proxy (production) + STDIO transport (Claude CLI development)
- 📊 **Conversation Persistence** - MCP-native conversation management with Firestore storage
- 🛡️ **Tiered Rate Limiting** - Anonymous/authenticated/VIP tiers with distributed coordination

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

### 📧 [mcp_mail](https://github.com/jleechanorg/mcp_mail)
- Multi-agent coordination system via async messaging (forked from [Dicklesworthstone/mcp_agent_mail](https://github.com/Dicklesworthstone/mcp_agent_mail)).
- **9 core enhancements** removing coordination barriers: 65% token reduction via lazy loading, global agent/message lookup across projects, automatic @mention scanning in unified inbox.
- Streamlined workflows: one-step agent registration with auto-project creation, contact-free messaging without approval gates.
- Projects as metadata only (not boundaries), enabling seamless cross-repo agent collaboration with flexible project keys.

### 🤖 [claude-commands](https://github.com/jleechanorg/claude-commands)
Automation backbone that scales Anthropic's Claude Code across heterogeneous environments.
- 150+ purpose-built slash commands compose MCP tools, shell scripts, and remote workflows into repeatable playbooks.
- Pipelines include queueing, rate limiting, observability hooks, and audit-friendly transcripts for full lifecycle coverage.
- Cross-platform setup guidance ensures Linux, macOS, and WSL contributors can bootstrap consistent workspaces in minutes.

#### ⚡ [Orchestration Framework](https://github.com/jleechanorg/claude-commands/blob/main/orchestration)
Multi-agent orchestration system for complex development tasks using tmux-based agent management:
- **Specialized Agents**: Frontend, backend, testing, and task-specific agents with complete isolation
- **Intelligent Reuse**: 50-80% efficiency gains through idle agent detection and strategic reuse
- **Real-time Coordination**: Redis-backed coordination with progress monitoring via `/orch status`
- **Natural Language Commands**: "Build X urgently", "connect to sonnet 1", "monitor agents"
- **Branch Isolation Protocol**: Agents work in dedicated worktrees preventing context contamination

#### 🔄 [GitHub PR Automation Framework](https://github.com/jleechanorg/claude-commands/tree/main/automation)
Seamless CI/CD integration with intelligent PR processing ([PyPI: jleechanorg-pr-automation](https://pypi.org/project/jleechanorg-pr-automation/) | [source](https://github.com/jleechanorg/claude-commands/tree/main/automation)):
- **Actionable PR Detection**: Only processes PRs that need attention based on commit-based tracking
- **Safety Limits**: Built-in rate limiting (per-PR and global) with cross-process thread-safe persistence
- **Hook Integration**: Auto-triggers after push operations with full Claude Code workflow integration
- **Email Notifications**: Optional SMTP integration for automation alerts
- **TodoWrite Integration**: Tracks automation tasks with comprehensive progress reporting

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
