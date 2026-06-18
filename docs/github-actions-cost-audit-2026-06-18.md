# GitHub Actions Cost Audit — 2026-06-18

**Scope:** All non-archived, non-fork repos in `jleechanorg` (83 repos).
**Method:** Shallow-cloned each repo, parsed `.github/workflows/*.yml` for `runs-on:` declarations, classified by repo visibility.

## Top-line

- **8 private repos** running on GitHub-hosted runners (cost leak)
- **4 public repos** using self-hosted runners (wasting free quota)
- **5 private repos** correctly using self-hosted
- **7 public repos** correctly using GitHub-hosted
- **59 repos** have no workflows (out of scope)

## Cost leaks: Private repos on GitHub-hosted runners

These repos are billing minutes against the personal GitHub account.

| Repo | Workflow files using hosted runners | Likely workload |
| --- | --- | --- |
| `ai_universe` | ci.yml, deploy-dev.yml, deploy-production.yml, auto-deploy.yml, runner-validation.yml, skeptic-cron.yml, skeptic-gate.yml, daily-user-activity-report.yml, deploy-mcp-inspector-pages.yml, deployment-simulation.yml, backend-coverage.yml, resolve-conflicts.yml, test-email-notification.yml, manual-smoke-tests.yml, pr-dev-preview.yml | Heavy CI + daily cron jobs — biggest bill |
| `ai_universe_frontend` | ci.yml, deploy-dev.yml, deploy-prod.yml, auto-deploy.yml, pr-preview.yml, pr-cleanup.yml, claude.yml, test-email-notification.yml, skeptic-cron.yml | Frontend CI + deploys |
| `ai_universe_convo_mcp` | ci.yml, deploy-dev.yml, deploy-prod.yml, auto-deploy-dev.yml, pr-preview.yml, pr-preview-smoke.yml, smoke-command.yml, presubmit.yml, test-email-notification.yml, skeptic-cron.yml, skeptic-gate.yml | MCP server CI |
| `worldai_genesis` | deploy.yml | Single deploy workflow |
| `worldai_ralph` | deploy.yml | Single deploy workflow |
| `ai_universe_mobile` | skeptic-cron.yml, skeptic-gate.yml | Skeptics only |
| `amazon-mvp-ralph-benchmark` | ci.yml | CI |
| `claude-code` | claude.yml, sweep.yml, backfill-duplicate-comments.yml, claude-dedupe-issues.yml, issue-opened-dispatch.yml, issue-lifecycle-comment.yml, lock-closed-issues.yml, auto-close-duplicates.yml, non-write-users-check.yml, claude-issue-triage.yml, log-issue-events.yml, remove-autoclose-label.yml | Issue triage + housekeeping |

**Estimated impact:** These 8 repos are running on the personal GitHub Actions bill. `ai_universe` alone has 15 hosted workflows including daily cron jobs — likely the single biggest line item.

## Wasteful: Public repos on self-hosted runners

These repos get free GitHub-hosted minutes but are burning MacBook CPU instead.

| Repo | Workflow files using self-hosted |
| --- | --- |
| `mctrl_test` | ci.yml, evidence-gate.yml, skeptic-gate.yml |
| `agent-orchestrator` | 17 workflow files (ci.yml, release.yml, test.yml, test-main.yml, integration-tests.yml, coverage.yml, skeptic-cron.yml, skeptic-cron-reusable.yml, skeptic-gate.yml, skeptic-gate-reusable.yml, green-gate.yml, evidence-gate.yml, wholesome.yml, wholesome-checks.yml, security.yml, coderabbit-ping-on-push.yml, cr-loop-health.yml, onboarding-test.yml, generate-pr-design-docs.yml) |
| `smartclaw` | 5 files (ci.yml, green-gate.yml, staging-canary-full.yml, staging-canary-gate.yml, skeptic-cron.yml, coderabbit-ping-on-push.yml) |
| `hermes-agent` | 14 files (ci.yml, tests.yml, lint.yml, nix.yml, nix-lockfile-fix.yml, uv-lockfile-check.yml, docker-publish.yml, deploy-site.yml, green-gate.yml, supply-chain-audit.yml, osv-scanner.yml, skills-index.yml, docs-site-checks.yml, skeptic-cron.yml, contributor-check.yml) |

**Estimated impact:** `agent-orchestrator` and `hermes-agent` together run ~30 hosted-capable workflows on the MacBook self-hosted runner. Each PR on these repos competes with your actual local dev work for CPU cycles.

## Correct

**Public + GitHub-hosted (7):** codex_plus, mcp_mail, codex_fork, ai_universe_living_blog, merge_train, dark-factory, .github

**Private + self-hosted (5):** worldarchitect.ai, jleechanclaw, worldai_claw, openclaw_sso, worldarchitect-autor-eval

## Next steps

1. **Quick wins (today):** Fix single-workflow leaks first.
   - `worldai_genesis/deploy.yml`, `worldai_ralph/deploy.yml` — flip `runs-on:` to `self-hosted` in 5 min.
2. **High-volume fixes (this week):** Audit `ai_universe*` repos — 15+ workflows each. Prioritize the daily cron jobs (`daily-user-activity-report.yml`, `skeptic-cron.yml`) since those run every day regardless of activity.
3. **Public flips:** Convert `hermes-agent` and `agent-orchestrator` workflows to GitHub-hosted — biggest impact on MacBook free CPU.
4. **Lock the policy:** Land `jleechanorg/.github` policy doc + reusable workflows. Then opt-in the gate per repo.

## Methodology

```bash
# Full scan script lives at scripts/scan_runner_defaults.py
gh api orgs/jleechanorg/repos --paginate -q \
  '.[] | select(.fork==false and .archived==false) | .name + "\t" + .visibility' \
  > /tmp/repos.tsv
# For each repo: shallow clone, parse .github/workflows/*.yml for runs-on
```

Raw scan output: `/tmp/gh_workflow_scan.json`