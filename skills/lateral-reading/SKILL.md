---
name: lateral-reading
description: Assess the trustworthiness of articles, posts, claims, screenshots, or copied text using lateral reading, source-quality review, primary and independent evidence, sentence-level URL citations, and an HTML visualization. Use when asked to check news, verify a claim, check credibility, inspect missing context, compare a post with outside sources, extract a target article into a text file, or produce a structured cited trust report with a rendered HTML page.
---

# Lateral Reading

## Overview

Assess one article, post, claim, URL, or screenshot at a time by first normalizing the target into a plain text file, then reading laterally across the open web, then rendering a human-readable HTML report beside that extracted text.

## Default Deliverables

Unless the user asks for JSON only, create a small output folder in the current workspace:

```text
reports/lateral-reading-YYYYMMDD-HHMMSS/
  target.txt
  report.json
  report.html
```

Use `target.txt` as the normalized input for rendering. Use `report.json` for the structured sentence-level findings. Use `report.html` as the final reader-facing visualization.

If the user asks only for a chat answer, return the JSON object directly instead of writing files.

## JSON Contract

Use this exact top-level shape for the report:

```json
{
  "responses": [
    {
      "text": "One complete sentence.",
      "citations": ["https://example.com/source"]
    }
  ]
}
```

Use one complete sentence per `responses` item. Do not put multiple sentences in one `text` field. When writing `report.json` or returning the structured report directly, include no Markdown, no prose outside JSON, and no code fences.

Stay concise by default: simple claims usually need 4 to 8 response sentences, complex claims usually need 8 to 14.

## Artifact Workflow

1. Prepare `target.txt` from the user input. Read `references/input-preparation.md` for URL, pasted-text, and screenshot handling.
2. Perform lateral reading using the normalized target and outside evidence.
3. Write `report.json` with the `responses` array described above.
4. Validate `report.json` when a shell is available:

```bash
python3 skills/lateral-reading/scripts/validate_report.py reports/lateral-reading-YYYYMMDD-HHMMSS/report.json
```

5. Render the HTML page from `target.txt` and `report.json`:

```bash
python3 skills/lateral-reading/scripts/render_report_html.py \
  --input reports/lateral-reading-YYYYMMDD-HHMMSS/target.txt \
  --report reports/lateral-reading-YYYYMMDD-HHMMSS/report.json \
  --out reports/lateral-reading-YYYYMMDD-HHMMSS/report.html
```

6. Final response: link to `report.html`, mention validation status, and keep the summary brief.

## Core Workflow

1. Identify the target: source, author or account, date, URL, genre, and central claim or framing.
2. Preserve claim precision: distinguish fact, allegation, interpretation, prediction, satire, opinion, and causal claim.
3. Search laterally using the headline, named entities, key numbers, dates, quoted phrases, images, and the source name.
4. Prefer original and primary evidence: official records, filings, datasets, papers, statements, transcripts, court documents, archived pages, and the original post or article.
5. Add independent evidence: reputable reporting, domain experts, fact checks, and context sources that do not merely repeat the same upstream source.
6. Check source quality: ownership, author expertise, conflicts of interest, corrections, sourcing transparency, and whether the article is news, analysis, opinion, sponsored content, or aggregation.
7. Check claim quality: missing context, selective quotes, stale dates, changed circumstances, denominator problems, money scale, conflated legal or policy stages, and causal overreach.
8. Synthesize with calibrated language. If evidence is insufficient, say the claim is unverified or unresolved rather than guessing.

## Citation Rules

Read `references/citation-rules.md` before finalizing any report. In brief:

- Cite every factual sentence with the URLs that support it.
- Cite the target article or post for claims about what the target says.
- Cite outside sources for verification, contradiction, missing context, or background.
- Use actual `http` or `https` URLs only. Do not invent URLs, use `[URL1]` placeholders, or cite search result pages.
- Use empty `citations` only for a purely synthetic verdict, limitation, or transition sentence whose support comes from cited neighboring sentences.

## Evidence Expectations

Read `references/evidence-taxonomy.md` when deciding what evidence is strongest. Read `references/source-quality.md` when the source, author, outlet, or account is part of the trust assessment.

High-quality reports usually include:

- A direct statement of the central claim or framing.
- A source assessment of the target when relevant.
- Primary evidence or the best available original source.
- Independent corroboration or contradiction.
- Missing context and residual uncertainty.
- A calibrated bottom-line judgment.

Do not over-weight repeated syndications, copied summaries, AI spam, content farms, anonymous social posts, or partisan commentary unless the task is specifically about that source's framing.

## Resource Map

- `references/input-preparation.md`: how to create `target.txt` from pasted text, URL input, or screenshot input.
- `references/report-schema.md`: exact JSON contract and examples.
- `references/citation-rules.md`: sentence-level citation rules.
- `references/evidence-taxonomy.md`: evidence strength ladder.
- `references/source-quality.md`: outlet, author, account, and source-quality review.
- `references/examples.md`: example prompts and output shapes.
- `scripts/validate_report.py`: validate report JSON.
- `scripts/render_report_html.py`: render a report beside the target text.

## Failure Modes

If browsing or retrieval tools are unavailable for a URL, ask the user to paste the article text or provide a screenshot instead of fabricating the target. If screenshot text is illegible, ask for a clearer screenshot or pasted text. If outside retrieval is unavailable, state that limitation in a response sentence and cite only sources that were actually provided or available.

Never present absence of evidence as disproof. Never use a citation to imply support for a stronger claim than the cited source actually makes.
