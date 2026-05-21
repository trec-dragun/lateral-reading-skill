# Citation Rules

Use sentence-level citations. The reader should be able to inspect every factual sentence and see which sources support it.

## Required Practice

- Put one sentence in each `responses[].text`.
- Add all supporting URLs for that sentence in `responses[].citations`.
- Use the target article or post URL when describing what the target claims.
- Use outside URLs when verifying, contradicting, or contextualizing the target.
- Prefer canonical source URLs over shorteners, tracking URLs, AMP pages, social mirrors, or search result pages.
- Use empty citations only for a synthetic judgment, limitation, or transition sentence that does not introduce a new fact.

## What To Avoid

- Do not invent citations or preserve placeholders such as `[URL1]`.
- Do not cite a homepage when a specific document, article, filing, dataset, or transcript supports the sentence.
- Do not cite sources that merely repeat the target unless the sentence is about repetition or media spread.
- Do not use citations as decoration. A cited source must support the precise sentence.
- Do not use a citation to launder uncertainty. If sources disagree, say so.

## Citation Granularity

Prefer 1 to 3 citations per factual sentence. Use more only when a sentence summarizes a dispute with several independent sides.

Good pattern:

```json
{
  "text": "The central factual claim is supported by the agency's original notice, but the article omits the later correction.",
  "citations": ["https://example.com/agency-notice", "https://example.com/correction"]
}
```

Bad pattern:

```json
{
  "text": "This is misleading for many reasons.",
  "citations": ["https://example.com"]
}
```
