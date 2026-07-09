import unittest
import sys
import os
import re

# Add scripts directory to path to import scan_runner_defaults
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import scripts.scan_runner_defaults as scan_runner_defaults

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

def run_gate_logic(text: str, vis: str) -> list[str]:
    """Helper mimicking the Python audit logic in runner-policy-gate.yml."""
    violations = []
    for m in re.finditer(r"runs-on\s*:", text):
        runners = parse_runners(text, m.end())
        if not runners:
            continue
        
        preceding_lines = [line for line in text[:m.start()].splitlines() if line.strip()]
        recent_lines = preceding_lines[-2:] if len(preceding_lines) >= 2 else preceding_lines
        has_override = any(re.search(r"^\s*#\s*runner-override", line) for line in recent_lines)
        
        for runner in runners:
            if vis == "private" and (runner.startswith("ubuntu") or runner.startswith("macos") or runner.startswith("windows")):
                if not has_override:
                    violations.append(f"violation: private-hosted-{runner}")
            if vis == "public" and "self-hosted" in runner:
                if not has_override:
                    violations.append(f"violation: public-self-hosted-{runner}")
    return violations

class TestRunnerPolicyGate(unittest.TestCase):
    def test_public_repo_hosted_runners_allowed(self):
        """Public repos should allow ubuntu, macos, and windows runners without warnings."""
        for runner in ["ubuntu-latest", "macos-13", "windows-2022"]:
            text = f"runs-on: {runner}"
            violations = run_gate_logic(text, "public")
            self.assertEqual(violations, [], f"{runner} should be allowed on public repos")

    def test_public_repo_self_hosted_violates_unless_overridden(self):
        """Public repos using self-hosted runners without override comment should violate policy."""
        text = "runs-on: self-hosted"
        violations = run_gate_logic(text, "public")
        self.assertTrue(len(violations) > 0, "self-hosted on public repo should violate policy")

        # With override comment
        text_with_override = "# runner-override: testing\nruns-on: self-hosted"
        violations_with_override = run_gate_logic(text_with_override, "public")
        self.assertEqual(violations_with_override, [], "self-hosted on public repo with override should not violate policy")

    def test_private_repo_hosted_violates_unless_overridden(self):
        """Private repos using GitHub-hosted runners without override comment should violate policy."""
        text = "runs-on: ubuntu-latest"
        violations = run_gate_logic(text, "private")
        self.assertTrue(len(violations) > 0, "ubuntu-latest on private repo should violate policy")

        text_with_override = "# runner-override: testing\nruns-on: ubuntu-latest"
        violations_with_override = run_gate_logic(text_with_override, "private")
        self.assertEqual(violations_with_override, [], "ubuntu-latest on private repo with override should not violate policy")

    def test_private_repo_self_hosted_allowed(self):
        """Private repos should allow self-hosted runners."""
        text = "runs-on: self-hosted"
        violations = run_gate_logic(text, "private")
        self.assertEqual(violations, [], "self-hosted on private repo should be allowed")

    def test_multiline_runs_on(self):
        """Multiline runs-on blocks should be parsed and checked for violations."""
        text = "runs-on:\n  - linux\n  - self-hosted"
        violations = run_gate_logic(text, "public")
        self.assertTrue(len(violations) > 0, "Multiline self-hosted on public repo should violate policy")

    def test_strict_override_context(self):
        """Override comment must be adjacent/preceding, not leak from unrelated context."""
        text = "jobs:\n  job1:\n    # runner-override: testing\n    runs-on: ubuntu-latest\n  job2:\n    runs-on: ubuntu-latest"
        violations = run_gate_logic(text, "private")
        # job2 has no override comment directly preceding it, so it should violate policy in a private repo
        self.assertEqual(len(violations), 1, "job2 should violate policy because its override comment is far away/for job1")

class TestScanRunnerDefaults(unittest.TestCase):
    def test_mixed_violations_not_masked(self):
        """
        A private repo with one ubuntu-latest workflow (cost leak) and one self-hosted
        workflow should be classified as ('private', 'hosted') (COST LEAK), not ('private', 'self_hosted').
        """
        scans = [
            {
                "repo": "mixed-repo",
                "visibility": "private",
                "workflows": [
                    {"file": "comply.yml", "runs_on": ["self-hosted"]},
                    {"file": "leak.yml", "runs_on": ["ubuntu-latest"]}
                ],
                "violations": [
                    {"file": "leak.yml", "runner": "ubuntu-latest"}
                ]
            }
        ]
        buckets = scan_runner_defaults.classify(scans)
        # It should be classified under private, hosted (cost leak)
        self.assertIn("mixed-repo", [s["repo"] for s in buckets[("private", "hosted")]])
        self.assertNotIn("mixed-repo", [s["repo"] for s in buckets[("private", "self_hosted")]])

    def test_compliant_repo(self):
        """
        A repo where all workflows comply should be correctly classified.
        """
        scans = [
            {
                "repo": "clean-private",
                "visibility": "private",
                "workflows": [
                    {"file": "comply.yml", "runs_on": ["self-hosted"]}
                ],
                "violations": []
            },
            {
                "repo": "clean-public",
                "visibility": "public",
                "workflows": [
                    {"file": "comply.yml", "runs_on": ["ubuntu-latest"]}
                ],
                "violations": []
            }
        ]
        buckets = scan_runner_defaults.classify(scans)
        self.assertIn("clean-private", [s["repo"] for s in buckets[("private", "self_hosted")]])
        self.assertIn("clean-public", [s["repo"] for s in buckets[("public", "hosted")]])

if __name__ == "__main__":
    unittest.main()
