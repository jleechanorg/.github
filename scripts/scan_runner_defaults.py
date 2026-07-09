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


def parse_runners(text: str, match_end_idx: int) -> list[str]:
    after_colon = text[match_end_idx:]
    first_line = after_colon.split("\n", 1)[0]
    inline_part = first_line.split("#", 1)[0].strip()
    if inline_part:
        if inline_part.startswith("[") and inline_part.endswith("]"):
            items = inline_part[1:-1].split(",")
            return [item.strip(" '\"") for item in items if item.strip()]
        else:
            return [inline_part.strip(" '\"")]
    lines = after_colon.splitlines()[1:]
    runners = []
    for line in lines:
        if not line.strip():
            continue
        if line.strip().startswith("#"):
            continue
        m = re.match(r"^\s+-\s*([^\n#]+)", line)
        if m:
            item = m.group(1).strip().strip(" '\"")
            runners.append(item)
        else:
            break
    return runners


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
            return {"repo": name, "visibility": visibility, "workflows": [], "violations": []}
        workflows = []
        violations = []
        for fn in sorted(os.listdir(wf_dir)):
            if not (fn.endswith(".yml") or fn.endswith(".yaml")):
                continue
            try:
                with open(os.path.join(wf_dir, fn)) as f:
                    content = f.read()
                runs_on_list = []
                for m in re.finditer(r"runs-on\s*:", content):
                    line_start = content.rfind("\n", 0, m.start()) + 1
                    line_end = content.find("\n", m.end())
                    if line_end == -1:
                        line_end = len(content)
                    line = content[line_start:line_end]
                    if line.strip().startswith("#"):
                        continue

                    runners = parse_runners(content, m.end())
                    if not runners:
                        continue
                    
                    preceding_lines = [line for line in content[:m.start()].splitlines() if line.strip()]
                    recent_lines = preceding_lines[-2:] if len(preceding_lines) >= 2 else preceding_lines
                    has_override = any(re.search(r"^\s*#\s*runner-override", line) for line in recent_lines)
                    
                    for runner in runners:
                        runs_on_list.append(runner)
                        is_violation = False
                        if visibility == "private" and (runner.startswith("ubuntu") or runner.startswith("macos") or runner.startswith("windows")):
                            if not has_override:
                                is_violation = True
                        elif visibility == "public" and "self-hosted" in runner:
                            if not has_override:
                                is_violation = True
                        
                        if is_violation:
                            violations.append({"file": fn, "runner": runner})
                workflows.append({"file": fn, "runs_on": runs_on_list})
            except Exception as e:
                print(f"Error parsing workflow file {fn} in {name}: {e}", file=sys.stderr)
        return {"repo": name, "visibility": visibility, "workflows": workflows, "violations": violations}
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
        has_violation = len(s.get("violations", [])) > 0
        vis = s["visibility"]
        if vis == "public":
            key = ("public", "self_hosted" if has_violation else "hosted")
        else:
            key = ("private", "hosted" if has_violation else "self_hosted")
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
        files = ", ".join(v["file"] for v in s.get("violations", []))
        print(f"  {s['repo']:45s}  {files}")

    print("\n--- WASTEFUL: Public + self-hosted ---")
    for s in buckets[("public", "self_hosted")]:
        files = ", ".join(v["file"] for v in s.get("violations", []))
        print(f"  {s['repo']:45s}  {files}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(scans, f, indent=2)
        print(f"\nRaw scan saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())