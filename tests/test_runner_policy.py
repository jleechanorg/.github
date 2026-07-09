import unittest
import sys
import os
import re

# Add scripts directory to path to import scan_runner_defaults
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import scripts.scan_runner_defaults as scan_runner_defaults

def run_gate_logic(text: str, vis: str) -> list[str]:
    """Helper mimicking the Python audit logic in runner-policy-gate.yml."""
    violations = []
    for m in re.finditer(r"runs-on:\s*([^\n#]+)", text):
        runner = m.group(1).strip()
        start = max(0, m.start() - 400)
        context = text[start:m.start()]
        has_override = "runner-override" in context
        
        # Strip wrapping quotes or brackets from runner if present
        r_clean = runner.strip("['\" ]")
        if vis == "private" and (r_clean.startswith("ubuntu") or r_clean.startswith("macos") or r_clean.startswith("windows")):
            if not has_override:
                violations.append(f"violation: private-hosted-{runner}")
        if vis == "public" and "self-hosted" in r_clean:
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
