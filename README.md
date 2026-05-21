# lateral-reading-skill

Claude Code plugin and portable skill for assessing articles, posts, claims, URLs, and screenshot text with lateral reading. The skill extracts the target into a text file, writes a structured sentence-level report, and renders an HTML visualization.

```json
{
  "responses": [
    {
      "text": "This is a complete sentence.",
      "citations": ["https://example.com/source"]
    }
  ]
}
```

The repo intentionally stays focused on everyday use.

## Use

Load the local plugin in Claude Code:

```bash
claude --plugin-dir .
```

Then invoke:

```text
/lateral-reading-skill:lateral-reading
```

Paste an article, URL, claim, tweet, or screenshot. The skill will first write the normalized target content into `target.txt`, then identify the central claim, read laterally against primary and independent sources, write `report.json`, and render `report.html`.

By default, a run should produce:

```text
reports/lateral-reading-YYYYMMDD-HHMMSS/
  target.txt
  report.json
  report.html
```

## Output Contract

The default report JSON is one object with a non-empty `responses` array. Each item is one complete sentence:

- `text`: the sentence shown to the reader.
- `citations`: zero or more `http` or `https` URLs supporting that sentence.

Keep reports concise by default, with detail scaled to the claim's complexity.

## Input Extraction

For pasted text, the skill copies the relevant article or post into `target.txt` with source fields when available. For a URL, it uses available browsing tools to extract the main article text and stores the original URL in the `URL:` field. For a screenshot, it transcribes the visible text into `target.txt` and notes limitations when text is cropped or illegible.

## Helper Scripts

Validate a report:

```bash
python3 skills/lateral-reading/scripts/validate_report.py examples/report.json
```

Render a report beside input text:

```bash
python3 skills/lateral-reading/scripts/render_report_html.py \
  --input examples/article_input.txt \
  --report examples/report.json \
  --out examples/report.html
```

Both scripts use only the Python standard library.

## Files

- `.claude-plugin/plugin.json`: Claude Code plugin manifest.
- `skills/lateral-reading/SKILL.md`: model instructions.
- `skills/lateral-reading/references/`: detailed guidance loaded as needed.
- `schemas/`: JSON Schema for the simple responses-only report shape.
- `examples/`: sample input and report fixtures.
