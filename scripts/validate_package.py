"""Read-only package checks; not a behavioral evaluator or privacy scanner."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


REQUIRED = (
    "SKILL.md", "README.md", "LICENSE", "agents/openai.yaml",
    "references/evidence-and-scope.md", "references/decision-guide.md",
    "references/change-procedure.md", "references/worked-example.md",
    "references/acceptance-cases.md",
)


def validate(root):
    """Return errors without modifying the package or making network requests."""
    root = Path(root).resolve()
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"missing file: {name}")

    skill = root / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
        if not match:
            errors.append("SKILL.md: missing or malformed YAML frontmatter")
        else:
            try:
                data = yaml.safe_load(match.group(1))
                if not isinstance(data, dict):
                    errors.append("SKILL.md: frontmatter must be a mapping")
                else:
                    if data.get("name") != "reflect-and-apply":
                        errors.append("SKILL.md: incorrect skill name")
                    description = data.get("description")
                    if not isinstance(description, str) or not description.strip():
                        errors.append("SKILL.md: missing description")
                    elif len(description) > 1024:
                        errors.append("SKILL.md: description exceeds 1024 characters")
            except yaml.YAMLError:
                errors.append("SKILL.md: invalid YAML frontmatter")

    ui = root / "agents" / "openai.yaml"
    if ui.is_file():
        try:
            data = yaml.safe_load(ui.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                errors.append("openai.yaml: expected a mapping")
            else:
                interface = data.get("interface")
                if not isinstance(interface, dict):
                    errors.append("openai.yaml: expected an interface mapping")
                else:
                    for key in ("display_name", "short_description", "default_prompt"):
                        value = interface.get(key)
                        if not isinstance(value, str) or not value.strip():
                            errors.append(f"openai.yaml: missing interface.{key}")
                    prompt = interface.get("default_prompt", "")
                    if isinstance(prompt, str) and "$reflect-and-apply" not in prompt:
                        errors.append("openai.yaml: default_prompt must name the skill")
                policy = data.get("policy")
                if not isinstance(policy, dict) or type(
                    policy.get("allow_implicit_invocation")
                ) is not bool:
                    errors.append("openai.yaml: invocation policy must be boolean")
        except yaml.YAMLError:
            errors.append("openai.yaml: invalid YAML")

    # Supports this package's inline links and backtick/tilde fenced code blocks.
    # Deliberately does not claim to implement the full Markdown grammar.
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", "__pycache__"}
               for part in path.relative_to(root).parts):
            continue
        fence = None
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if marker:
                token, suffix = marker.groups()
                if fence is None:
                    fence = token
                elif token[0] == fence[0] and len(token) >= len(fence) and not suffix.strip():
                    fence = None
                continue
            if fence is not None:
                continue
            for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", line):
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                resolved = (path.parent / unquote(parts.path)).resolve()
                if not resolved.is_relative_to(root):
                    errors.append(f"{relative}:{number}: link outside package")
                elif not resolved.exists():
                    errors.append(f"{relative}:{number}: broken link: {target}")
        if fence is not None:
            errors.append(f"{relative}: unclosed fence")
    return errors


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python scripts/validate_package.py [package-root]")
        sys.exit(2)
    package_root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    issues = validate(package_root)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        sys.exit(1)
    print("Package structure, YAML, local file links, and code fences: OK")
