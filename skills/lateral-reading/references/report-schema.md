# Report Schema

Use this reference when preparing final output or writing adapters around the skill.

## Responses-Only Output

The default skill output is a single JSON object:

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

Rules:

- `responses` must be a non-empty array.
- Each `text` must be a non-empty string containing one complete sentence.
- Each `citations` value must be an array of strings.
- Citations must be actual `http` or `https` URLs.
- Do not include Markdown fences, comments, trailing prose, or extra top-level keys.
