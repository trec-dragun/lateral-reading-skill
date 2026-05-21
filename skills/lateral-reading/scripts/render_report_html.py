#!/usr/bin/env python3
"""Render a lateral-reading report beside the target text."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

WORD_RE = re.compile(r"\b[\w'-]+\b")


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def load_report(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw)


def load_target(path: Path | None) -> dict[str, str]:
    if path is None:
        return {"title": "Target input", "body": ""}

    raw = path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return parse_text_target(path, raw)

    if not isinstance(parsed, dict):
        return {"title": path.name, "body": raw}

    title = str(parsed.get("title") or parsed.get("headline") or path.name)
    body = parsed.get("text") or parsed.get("content") or parsed.get("body") or raw
    url = str(parsed.get("url") or parsed.get("source_url") or "")
    source = str(parsed.get("source") or parsed.get("outlet") or "")
    return {"title": title, "body": str(body), "url": url, "source": source}


def parse_text_target(path: Path, raw: str) -> dict[str, str]:
    target = {"title": path.name, "body": raw}
    for line in raw.splitlines()[:12]:
        key, sep, value = line.partition(":")
        if not sep:
            continue
        normalized = key.strip().lower()
        cleaned = value.strip()
        if not cleaned:
            continue
        if normalized in {"title", "headline"}:
            target["title"] = cleaned
        elif normalized in {"source", "outlet"}:
            target["source"] = cleaned
        elif normalized in {"url", "source url", "source_url"}:
            target["url"] = cleaned
    return target


def citation_label(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc:
        return parsed.netloc
    return url


def render(report: dict[str, Any], target: dict[str, str], title: str | None) -> str:
    responses = report.get("responses", [])
    sentences = [r for r in responses if isinstance(r, dict)]
    words = sum(word_count(str(item.get("text", ""))) for item in sentences)
    citations = sum(len(item.get("citations", [])) for item in sentences if isinstance(item.get("citations"), list))
    missing_citations = sum(1 for item in sentences if not item.get("citations"))
    page_title = title or target.get("title") or "Lateral Reading Report"
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    sentence_html = []
    for index, item in enumerate(sentences, start=1):
        text = html.escape(str(item.get("text", "")))
        raw_citations = item.get("citations", [])
        citation_items = []
        if isinstance(raw_citations, list):
            for citation in raw_citations:
                if not isinstance(citation, str):
                    continue
                safe_url = html.escape(citation, quote=True)
                label = html.escape(citation_label(citation))
                citation_items.append(f'<a href="{safe_url}" rel="noreferrer" target="_blank">{label}</a>')
        if citation_items:
            cited = " ".join(citation_items)
        else:
            cited = '<span class="muted">No citation</span>'
        sentence_html.append(
            f"""
            <article class="sentence">
              <div class="sentence-index">{index}</div>
              <p>{text}</p>
              <div class="citations">{cited}</div>
            </article>
            """
        )

    target_meta = []
    if target.get("source"):
        target_meta.append(f"<span>{html.escape(target['source'])}</span>")
    if target.get("url"):
        safe_url = html.escape(target["url"], quote=True)
        target_meta.append(f'<a href="{safe_url}" rel="noreferrer" target="_blank">{html.escape(target["url"])}</a>')

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --panel: #ffffff;
      --text: #1f2328;
      --muted: #6a7178;
      --border: #d8d8d0;
      --accent: #0f6b5f;
      --warn: #9a4f00;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    header {{
      padding: 28px min(5vw, 56px) 18px;
      border-bottom: 1px solid var(--border);
      background: var(--panel);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(24px, 3vw, 38px);
      letter-spacing: 0;
    }}
    .subtle, .muted {{
      color: var(--muted);
    }}
    main {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(360px, 0.95fr);
      gap: 24px;
      padding: 24px min(5vw, 56px) 40px;
    }}
    section {{
      min-width: 0;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
    }}
    h2 {{
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }}
    pre {{
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      margin: 0;
      font: inherit;
    }}
    .stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 0 0 16px;
    }}
    .badge {{
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 4px 10px;
      background: #fbfbf9;
      color: var(--muted);
      font-size: 13px;
    }}
    .badge.warn {{
      color: var(--warn);
      border-color: #e0b37b;
      background: #fff7ed;
    }}
    .sentence {{
      display: grid;
      grid-template-columns: 32px minmax(0, 1fr);
      gap: 12px;
      padding: 14px 0;
      border-top: 1px solid var(--border);
    }}
    .sentence:first-of-type {{
      border-top: 0;
    }}
    .sentence-index {{
      grid-column: 1;
      grid-row: 1;
      width: 28px;
      height: 28px;
      display: grid;
      place-items: center;
      border-radius: 50%;
      background: var(--accent);
      color: white;
      font-size: 13px;
      font-weight: 700;
    }}
    .sentence p {{
      grid-column: 2;
      margin: 0 0 8px;
    }}
    .citations {{
      grid-column: 2;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .citations a {{
      display: inline-flex;
      max-width: 100%;
      padding: 3px 8px;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: #fbfbf9;
      text-decoration: none;
      overflow-wrap: anywhere;
    }}
    .citations a:hover {{
      text-decoration: underline;
    }}
    a {{
      color: var(--accent);
      overflow-wrap: anywhere;
    }}
    @media (max-width: 860px) {{
      main {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(page_title)}</h1>
    <div class="subtle">Generated {generated_at}</div>
  </header>
  <main>
    <section class="panel">
      <h2>Target</h2>
      {'<div class="subtle">' + ' | '.join(target_meta) + '</div>' if target_meta else ''}
      <pre>{html.escape(target.get("body", ""))}</pre>
    </section>
    <section class="panel">
      <h2>Report</h2>
      <div class="stats">
        <span class="badge">{len(sentences)} sentences</span>
        <span class="badge">{words} words</span>
        <span class="badge">{citations} citations</span>
        <span class="badge {'warn' if missing_citations else ''}">{missing_citations} uncited</span>
      </div>
      {''.join(sentence_html)}
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path, help="Report JSON file")
    parser.add_argument("--input", type=Path, help="Target article, claim, tweet, or JSON input")
    parser.add_argument("--out", required=True, type=Path, help="Output HTML path")
    parser.add_argument("--title", help="Override HTML title")
    args = parser.parse_args()

    report = load_report(args.report)
    if not isinstance(report, dict):
        raise SystemExit("report must be a JSON object")
    target = load_target(args.input)
    html_output = render(report, target, args.title)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_output, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
