"""Keep release authority and the fresh platform matrix explicit in source."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_workflows_pin_actions_and_have_no_private_access_or_automatic_publish():
    paths = sorted((ROOT / ".github/workflows").glob("*.yml"))
    assert len(paths) == 2
    for path in paths:
        text = path.read_text()
        actions = re.findall(r"uses:\s*([^\s]+)", text)
        assert actions and all(re.fullmatch(r"[A-Za-z0-9_./-]+@[a-f0-9]{40}", action) for action in actions)
        assert "persist-credentials: false" in text
        assert "pull_request_target:" not in text and "workflow_run:" not in text
        assert "secrets." not in text and "contents: write" not in text
        assert "PhysicalSystems/node/" not in text
    publish = (ROOT / ".github/workflows/publish.yml").read_text()
    assert "workflow_dispatch:" in publish and "pull_request:" not in publish and "push:" not in publish
    assert "platform: [linux-x64, win32-x64]" in publish
    assert "python: ['3.10', '3.11', '3.12']" in publish
    assert "needs: [verify, install]" in publish
    assert "name: physical-node-pypi" in publish
    assert publish.count("id-token: write") == 1
    assert "packages-dir: .release-stage/upload/" in publish
    assert "skip-existing: false" in publish and "attestations: true" in publish
    assert "dc37677b2e1c63e2034f94d8a5b11f265b73ba33" in publish
    assert "node-proof-${{ github.run_id }}-${{ github.run_attempt }}-*" in publish
    assert "physicalsystems-node-install-v1" not in publish  # Generated only after exact readback.


def test_auth_fetch_and_installed_probe_are_separate_steps():
    text = (ROOT / ".github/workflows/publish.yml").read_text()
    install_step = text.split("- name: Install offline", 1)[1].split("- uses:", 1)[0]
    assert "GH_TOKEN" not in install_step and "github.token" not in install_step
    assert "'install'" in install_step and "--directory" in install_step
    assert "--candidate-release-id" not in install_step


def test_public_repository_has_no_wheel_or_private_runtime_code():
    assert not list(ROOT.glob("**/*.whl"))
    assert not (ROOT / "tinyedge_agent").exists()
    assert not (ROOT / "tinyedge_runtime").exists()
    text = (ROOT / "scripts/release.py").read_text()
    assert "build_physical_node" not in text
    assert "private-candidate" not in text
