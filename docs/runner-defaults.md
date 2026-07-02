# Runner Defaults — jleechanorg Org Policy

**Owner:** @jleechanorg
**Status:** Active (effective immediately for new repos; existing repos should adopt on next workflow touch)
**Last updated:** 2026-06-18

## TL;DR

| Repo visibility | Default runner | Why |
| --- | --- | --- |
| **Public** | `ubuntu-latest` / `macos-latest` / `windows-latest` (GitHub-hosted) | Free for public repos — 2,000 min/mo macOS, unlimited Linux/Windows. Don't waste a self-hosted slot. |
| **Private** | `self-hosted` (MacBook runner) | GitHub-hosted minutes bill against your account. Self-hosted is free. |
| **Override** | Explicit `runs-on:` opt-out | Comment `# runner-override: <reason>` required above the override. |

## Rule

**Private repos use self-hosted runners by default. Public repos use GitHub-hosted runners by default.**

The only exceptions are explicitly-listed overrides with a `runner-override:` comment.

## What you must do

When adding a new workflow:

1. **Public repo?** Use `ubuntu-latest`, `macos-latest`, `windows-latest` — whatever the job needs.
2. **Private repo?** Use `runs-on: self-hosted` (or a self-hosted label like `self-hosted-macos`, `self-hosted-linux`).
3. **Need to override?** Add a comment immediately above `runs-on:`:

   ```yaml
   jobs:
     heavy-matrix:
       # runner-override: public repo + need cross-OS matrix in one job, cheaper to run on GitHub-hosted
       runs-on: ${{ matrix.os }}
       strategy:
         matrix:
           os: [ubuntu-latest, macos-latest, windows-latest]
   ```

   No comment = policy violation = CI will warn (see enforcement below).

## Why this exists

Audit on 2026-06-18 across 83 jleechanorg repos found:

- **8 private repos running on GitHub-hosted runners** (cost leak against your personal bill)
  - ai_universe, ai_universe_frontend, ai_universe_convo_mcp, worldai_genesis,
    worldai_ralph, ai_universe_mobile, amazon-mvp-ralph-benchmark, claude-code
- **4 public repos using self-hosted runners** (wasting free quota + burning MacBook CPU)
  - mctrl_test, agent-orchestrator, smartclaw, hermes-agent

Concrete cost numbers in `docs/github-actions-cost-audit-2026-06-18.md` (this folder).

## Enforcement

### Soft enforcement (now)

A reusable workflow `runner-defaults.yml` (in this repo's `.github/workflows/`) wraps new jobs and emits a warning annotation if `runs-on` violates the policy for the current repo's visibility. **Use it via `uses:`**:

```yaml
jobs:
  test:
    uses: jleechanorg/.github/.github/workflows/runner-defaults.yml@main
    with:
      visibility: private            # or 'public'
      job-name: test
      runs-on-override: macos-latest  # optional, requires comment in caller
```

### Hard enforcement (later, opt-in per repo)

Add this to any repo to **fail CI** when `runs-on:` violates policy:

```yaml
# .github/workflows/runner-policy-gate.yml
name: Runner Policy Gate
on:
  pull_request:
    paths: ['.github/workflows/**']
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: jleechanorg/.github/.github/workflows/runner-policy-gate.yml@main
        with:
          repo-visibility: ${{ github.event.repository.private && 'private' || 'public' }}
```

The gate is **opt-in** because flipping it on for an existing repo with 30 workflows creates a wall of red. Roll it out repo-by-repo as workflows are modernized.

## Migration cheat-sheet

### Private repo, currently `ubuntu-latest`

```yaml
# before
jobs:
  test:
    runs-on: ubuntu-latest

# after
jobs:
  test:
    runs-on: self-hosted
```

If the runner label matters (e.g., you need macOS, or a specific GPU):

```yaml
runs-on: self-hosted-macos   # or self-hosted-linux, self-hosted-gpu, etc.
```

### Public repo, currently `self-hosted`

```yaml
# before
jobs:
  test:
    runs-on: self-hosted

# after
jobs:
  test:
    runs-on: ubuntu-latest    # or macos-latest / windows-latest
```

### Matrix jobs that mix OS

This is the most common legitimate override. Add the comment:

```yaml
jobs:
  cross-platform:
    # runner-override: cross-OS matrix requires GitHub-hosted because self-hosted is single-OS
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
```

## FAQ

**Q: My private repo has a job that needs a clean Linux container for security reasons. Can I use GitHub-hosted?**
A: Yes — add `# runner-override: need ephemeral Linux sandbox` above `runs-on:`. Self-hosted is the default, not a hard rule.

**Q: My public repo's tests need 32 GB RAM. GitHub-hosted maxes out at 64 GB on `ubuntu-latest-8-cores`. Is self-hosted justified?**
A: Sometimes, yes. Add the override comment with the reason. Track in the cost audit doc.

**Q: Where do I find the available self-hosted labels?**
A: Run `gh api repos/OWNER/REPO/actions/runners --jq '.[].labels[]'` — defaults are `self-hosted`, `self-hosted-linux`, `self-hosted-macos`, plus any custom labels you've configured on the MacBook runner.

**Q: Does this apply to forks?**
A: No — forks use the parent repo's policy by default. This policy is for org-owned repos.

**Q: Does this apply to GitHub Actions on `jleechan` (personal account)?**
A: Personal-account repos are out of scope for this org policy, but the same logic applies. Personal private repos also bill minutes — default to self-hosted.

## Related

- `docs/github-actions-cost-audit-2026-06-18.md` — raw audit numbers
- `.github/workflows/runner-defaults.yml` — reusable workflow (soft enforcement)
- `.github/workflows/runner-policy-gate.yml` — opt-in hard gate
- `.github/CODEOWNERS` — runner label additions must be approved by `@jleechan`