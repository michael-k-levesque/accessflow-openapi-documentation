#!/usr/bin/env python3
"""Lightweight repository and documentation quality checks.

These checks intentionally avoid a heavyweight toolchain so the portfolio can
run locally and in CI with predictable behavior. They complement, rather than
replace, a dedicated prose linter or full OpenAPI ruleset in a production repo.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "AI_ASSISTED_DOCUMENTATION_WORKFLOW.md",
    "DOCUMENTATION_STRATEGY_AND_MEASUREMENT.md",
    "openapi.yaml",
    "requirements.txt",
    "docs/AccessFlow_API_Developer_Guide.pdf",
    "examples/create-access-request.json",
    "examples/access-request-approved.json",
    "examples/problem-validation.json",
    "scripts/validate_examples.py",
    "scripts/check_repository.py",
    ".github/workflows/validate.yml",
    ".github/workflows/publish-docs.yml",
    "site/index.html",
    ".github/pull_request_template.md",
}

FORBIDDEN_DIR_NAMES = {"_render", "_render2", "_pdf_verify", "__pycache__"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".json", ".txt"}
LOCAL_MD_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_required_files(errors: list[str]) -> None:
    existing = {relative(p) for p in ROOT.rglob("*") if p.is_file()}
    for required in sorted(REQUIRED_FILES - existing):
        errors.append(f"Missing required repository file: {required}")


def check_hygiene(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if path.is_dir() and path.name in FORBIDDEN_DIR_NAMES:
            errors.append(f"Temporary/build directory must not be committed: {relative(path)}")
        if path.is_file() and path.suffix.lower() == ".docx":
            errors.append(f"Editable Office source is excluded from the public repository: {relative(path)}")


def check_text_files(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                errors.append(f"Trailing whitespace: {relative(path)}:{lineno}")
            if "\t" in line:
                errors.append(f"Tab character found: {relative(path)}:{lineno}")
        markers = ("TO" + "DO", "TB" + "D")
        if any(marker in text for marker in markers):
            errors.append(f"Unresolved placeholder marker: {relative(path)}")


def check_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for match in LOCAL_MD_LINK.finditer(text):
            target = match.group(1).split("#", 1)[0].strip()
            if not target or target.startswith("<"):
                continue
            target_path = (path.parent / target).resolve()
            try:
                target_path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"Local Markdown link escapes repository: {relative(path)} -> {target}")
                continue
            if not target_path.exists():
                errors.append(f"Broken local Markdown link: {relative(path)} -> {target}")


def main() -> None:
    errors: list[str] = []
    check_required_files(errors)
    check_hygiene(errors)
    check_text_files(errors)
    check_markdown_links(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)

    print("PASS: repository structure, hygiene, text quality, and local Markdown links validated.")


if __name__ == "__main__":
    main()
