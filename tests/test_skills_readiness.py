"""Agent-readiness checks for the project-owned skills (router, Kling, adapter)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "projects" / "andre-time-travel"
PROJECT_OWNED = [
    ROOT / "skills/andre-time-travel/SKILL.md",
    ROOT / "skills/andre-time-travel/references/shared-skills-adapter.md",
    ROOT / ".agents/skills/kling-cli/SKILL.md",
]
PATH_TOKEN = re.compile(r"`([A-Za-z0-9_./\-]+\.(?:md|json|py|csv|sh))`")
NOT_FILES = {"package.json", ".credentials", "request.json", "scope.json"}


def shared_skills_available() -> bool:
    return all(
        (ROOT / "skills" / name / "SKILL.md").is_file()
        for name in [
            "film-character-continuity",
            "film-dialogue-localization",
            "film-editing-qc",
            "grounded-citations",
        ]
    )


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"{path} has no frontmatter"
    result: dict[str, str] = {}
    key = None
    for line in match.group(1).splitlines():
        if re.match(r"^[A-Za-z_-]+:", line):
            key, _, value = line.partition(":")
            result[key] = value.strip().lstrip(">-").strip()
        elif key and line.startswith(" "):
            result[key] = (result[key] + " " + line.strip()).strip()
    return result


class SkillReadinessTests(unittest.TestCase):
    def test_referenced_files_exist(self) -> None:
        bases = [
            ROOT,
            EPISODE,
            ROOT / "docs/kling-manual",
            ROOT / "skills",
            ROOT / "skills/andre-time-travel",
            *sorted((ROOT / "skills").glob("*/")),
            *sorted((ROOT / "skills").glob("*/references")),
            # bare file names in prose: the folders where such records live
            EPISODE / "00_brief",
            EPISODE / "00_brief/research",
            EPISODE / "01_script",
            EPISODE / "memory",
            EPISODE / "tasks",
            ROOT / "shared/templates",
            ROOT / "docs/kling-manual/tools",
        ]
        missing: list[str] = []
        for source in PROJECT_OWNED:
            for match in PATH_TOKEN.finditer(source.read_text(encoding="utf-8")):
                token = match.group(1)
                if token in NOT_FILES or "<" in token:
                    continue
                if token.startswith("references/") and not shared_skills_available():
                    continue
                if not any((base / token).exists() for base in bases):
                    missing.append(f"{source.relative_to(ROOT)} -> {token}")
        self.assertEqual(missing, [])

    def test_frontmatter_is_loadable(self) -> None:
        for source in [path for path in PROJECT_OWNED if path.name == "SKILL.md"]:
            meta = frontmatter(source)
            self.assertEqual(meta["name"], source.parent.name, source)
            description = meta["description"]
            self.assertGreater(len(description), 80, f"{source} description too thin to trigger")
            self.assertLess(len(description), 1024, f"{source} description too long")

    def test_registry_hashes_match_project_skills(self) -> None:
        registry = json.loads((ROOT / "skills/registry.json").read_text(encoding="utf-8"))
        kling = next(item for item in registry["skills"] if item["name"] == "kling-cli")
        digest = hashlib.sha256((ROOT / ".agents/skills/kling-cli/SKILL.md").read_bytes()).hexdigest()
        self.assertEqual(kling["sourceSha256"], digest)
        self.assertEqual(kling["provenanceHistory"][-1]["sourceSha256"], digest)

    def test_project_skills_are_discoverable_by_claude_code(self) -> None:
        registry = json.loads((ROOT / "skills/registry.json").read_text(encoding="utf-8"))
        for item in registry["skills"]:
            if item["type"] in {"project_local", "project_vendored"}:
                link = ROOT / ".claude/skills" / item["name"]
                self.assertTrue((link / "SKILL.md").is_file(), f"{item['name']} not discoverable")
                self.assertEqual(
                    link.resolve(), (ROOT / item["path"]).resolve(), item["name"]
                )

    def test_router_covers_the_agents_md_contract(self) -> None:
        text = (ROOT / "skills/andre-time-travel/SKILL.md").read_text(encoding="utf-8")
        for needle in [
            "workflow-map-v1.md",
            "2026-10-09-direcao-encontros-fala-dificil.md",
            "mistakes.jsonl",
            "agent-handoff-v2.json",
            "manage.py resume",
            "kling_job_release",
            "higgsfield-scope.json",
            "shared-skills-adapter.md",
            "agents/registry.json",
        ]:
            self.assertIn(needle, text)

    def test_every_role_skill_has_a_registry_entry_and_contract_points_to_adapter(self) -> None:
        agents = json.loads((ROOT / "agents/registry.json").read_text(encoding="utf-8"))
        names = {
            item["name"]
            for item in json.loads((ROOT / "skills/registry.json").read_text(encoding="utf-8"))["skills"]
        }
        for role in agents["roles"]:
            self.assertTrue(set(role["skills"]) <= names, role["id"])
        contract = (ROOT / "agents/CONTRACT.md").read_text(encoding="utf-8")
        self.assertIn("shared-skills-adapter.md", contract)

    def test_higgsfield_gate_assets_are_wired(self) -> None:
        template = json.loads((ROOT / "shared/templates/higgsfield-scope.json").read_text(encoding="utf-8"))
        for field in ["ceiling", "grantedBy", "balanceBefore", "balanceTimestamp", "jobTypes"]:
            self.assertIn(field, template)
        settings = (ROOT / ".claude/settings.json").read_text(encoding="utf-8")
        self.assertIn("higgsfield-gate.py", settings)
        self.assertIn("mcp__.*[Hh]iggsfield", settings)
        policy = (ROOT / "docs/MODEL_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("higgsfield-gate.py", policy)


if __name__ == "__main__":
    unittest.main()
