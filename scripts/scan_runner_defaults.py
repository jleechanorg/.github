#!/usr/bin/env python3
"""
Scan all jleechanorg repos for runner-defaults policy violations.

Classifies each repo as public/private, then audits each .github/workflows/*.yml
file for runs-on: declarations. Reports:
  - Private repos using GitHub-hosted runners (cost leak)
  - Public repos using self-hosted runners (wasteful)

Usage:
  python3 scripts/scan_runner_defaults.py [--output FILE]

Requires: gh CLI authenticated.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed


def list_repos(org: str) -> list[tuple[str, str]]:
    """Return [(name, visibility), ...] for non-fork, non-archived repos."""
    out = subprocess.run(
        ["gh", "api", f"orgs/{org}/repos", "--paginate", "-q",
         ".[] | select(.fork==false and .archived==false) | .name + \"\\t\" + .visibility"],
        check=True, capture_output=True, text=True,
    )
    return [tuple(line.split("\t")) for line in out.stdout.splitlines() if line.strip()]


def scan_repo(name: str, visibility: str, org: str = "jleechanorg") -> dict:
    """Shallow-clone a repo and audit its workflows."""
    full = f"{org}/{name}"
    tmp = tempfile.mkdtemp(prefix=f"runner-scan-{name}-")
    try:
        clone = subprocess.run(
            ["gh", "repo", "clone", full, tmp, "--", "--depth=1", "--quiet"],
            capture_output=True, text=True, timeout=30,
        )
        if clone.returncode != 0:
            return {"repo": name, "visibility": visibility, "error": clone.stderr.strip()[:200]}
        wf_dir = os.path.join(tmp, ".github", "workflows")
        if not os.path.isdir(wf_dir):
            return {"repo": name, "visibility": visibility, "workflows": []}
        workflows = []
        for fn in sorted(os.listdir(wf_dir)):
            if not (fn.endswith(".yml") or fn.endswith(".yaml")):
                continue
            with open(os.path.join(wf_dir, fn)) as f:
                content = f.read()
            runs_on = []
            for m in re.finditer(r"runs-on:\s*(\[.*?\]|[^\n#]+)", content):
                runs_on.append(m.group(1).strip())
            workflows.append({"file": fn, "runs_on": runs_on})
        return {"repo": name, "visibility": visibility, "workflows": workflows}
    except subprocess.TimeoutExpired:
        return {"repo": name, "visibility": visibility, "error": "clone timeout"}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def classify(scans: list[dict]) -> dict:
    """Group scans by visibility × runner choice."""
    buckets = {
        ("public", "hosted"): [],
        ("public", "self_hosted"): [],
        ("private", "hosted"): [],
        ("private", "self_hosted"): [],
        "no_workflows": [],
        "errors": [],
    }
    for s in scans:
        if "error" in s:
            buckets["errors"].append(s)
            continue
        wfs = s.get("workflows", [])
        if not wfs:
            buckets["no_workflows"].append(s["repo"])
            continue
        uses_selfhosted = any("self-hosted" in str(ro) for wf in wfs for ro in wf["runs_on"])
        vis = s["visibility"]
        key = (vis, "self_hosted" if uses_selfhosted else "hosted")
        buckets[key].append(s)
    return buckets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", default="jleechanorg")
    parser.add_argument("--output", default=None, help="Write raw JSON to this path")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    repos = list_repos(args.org)
    print(f"Scanning {len(repos)} repos in {args.org}...")

    scans = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(scan_repo, n, v, args.org): (n, v) for n, v in repos}
        for f in as_completed(futures):
            scans.append(f.result())

    buckets = classify(scans)

    print(f"\n=== Runner policy audit — {args.org} ===\n")
    print(f"PUBLIC + GitHub-hosted  (CORRECT):  {len(buckets[('public', 'hosted')])}")
    print(f"PUBLIC + self-hosted    (WASTEFUL): {len(buckets[('public', 'self_hosted')])}")
    print(f"PRIVATE + self-hosted   (CORRECT):  {len(buckets[('private', 'self_hosted')])}")
    print(f"PRIVATE + GitHub-hosted (COST LEAK): {len(buckets[('private', 'hosted')])}")
    print(f"No workflows / errors:              {len(buckets['no_workflows']) + len(buckets['errors'])}")

    print("\n--- COST LEAK: Private + GitHub-hosted ---")
    for s in buckets[("private", "hosted")]:
        files = ", ".join(w["file"] for w in s["workflows"])
        print(f"  {s['repo']:45s}  {files}")

    print("\n--- WASTEFUL: Public + self-hosted ---")
    for s in buckets[("public", "self_hosted")]:
        files = ", ".join(w["file"] for w in s["workflows"])
        print(f"  {s['repo']:45s}  {files}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(scans, f, indent=2)
        print(f"\nRaw scan saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())