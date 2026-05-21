#!/usr/bin/env python3
"""Validate lateral-reading report JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

WORD_RE = re.compile(r"\b[\w'-]+\b")
PLACEHOLDER_RE = re.compile(r"\[?\s*URL\s*\d+\s*\]?", re.IGNORECASE)


@dataclass
class Issue:
    path: str
    message: str


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def load_report(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("```"):
        raise ValueError("input appears to contain a Markdown code fence")

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc


def validate_report(record: Any, args: argparse.Namespace) -> tuple[list[Issue], int, int]:
    issues: list[Issue] = []
    total_words = 0
    total_citations = 0

    def add(path: str, message: str) -> None:
        issues.append(Issue(path, message))

    if not isinstance(record, dict):
        add("$", "record must be a JSON object")
        return issues, total_words, total_citations

    allowed_top = {"responses"}
    extra_top = sorted(set(record) - allowed_top)
    if extra_top:
        add("$", f"unexpected top-level key(s): {', '.join(extra_top)}")

    responses = record.get("responses")
    if not isinstance(responses, list) or not responses:
        add("$.responses", "responses must be a non-empty array")
        return issues, total_words, total_citations

    for index, response in enumerate(responses):
        base = f"$.responses[{index}]"
        if not isinstance(response, dict):
            add(base, "response must be an object")
            continue

        extra_keys = sorted(set(response) - {"text", "citations"})
        if extra_keys:
            add(base, f"unexpected key(s): {', '.join(extra_keys)}")

        text = response.get("text")
        if not isinstance(text, str) or not text.strip():
            add(f"{base}.text", "text must be a non-empty string")
        else:
            if "```" in text:
                add(f"{base}.text", "text must not contain Markdown fences")
            if PLACEHOLDER_RE.search(text):
                add(f"{base}.text", "text must not contain URL placeholders")
            total_words += word_count(text)

        citations = response.get("citations")
        if not isinstance(citations, list):
            add(f"{base}.citations", "citations must be an array")
            continue

        if args.require_citations and not citations:
            add(f"{base}.citations", "citations must not be empty")

        total_citations += len(citations)
        for citation_index, citation in enumerate(citations):
            citation_path = f"{base}.citations[{citation_index}]"
            if not isinstance(citation, str) or not citation.strip():
                add(citation_path, "citation must be a non-empty string")
                continue
            if PLACEHOLDER_RE.fullmatch(citation.strip()):
                add(citation_path, "citation must not be a placeholder")
            if not is_url(citation):
                add(citation_path, "citation must be an http or https URL")

    return issues, total_words, total_citations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to a JSON report file")
    parser.add_argument("--require-citations", action="store_true", help="Require every sentence to have at least one citation")
    parser.add_argument("--summary-json", action="store_true", help="Print machine-readable validation summary")
    args = parser.parse_args()

    try:
        record = load_report(args.report)
    except OSError as exc:
        print(f"error: cannot read {args.report}: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    all_issues, total_words, total_citations = validate_report(record, args)

    summary = {
        "valid": not all_issues,
        "word_count": total_words,
        "citation_count": total_citations,
        "issues": [issue.__dict__ for issue in all_issues],
    }

    if args.summary_json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif all_issues:
        for issue in all_issues:
            print(f"{issue.path}: {issue.message}", file=sys.stderr)
    else:
        print(f"valid: {total_words} word(s), {total_citations} citation(s)")

    return 0 if not all_issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
