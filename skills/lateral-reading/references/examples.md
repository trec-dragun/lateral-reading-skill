# Examples

The examples below show shape, not a claim that the example URLs are real evidence.

## Article Prompt

```text
Use $lateral-reading on this article:

Title: City announces new recycling pilot
Text: The city says the pilot will cut landfill waste by 20 percent next year...
```

Expected response shape:

```json
{
  "responses": [
    {
      "text": "The article's main claim is that a new recycling pilot is expected to reduce landfill waste by 20 percent next year.",
      "citations": ["https://example.com/target-article"]
    },
    {
      "text": "That forecast should be treated cautiously unless the city has published the model, baseline waste volume, and implementation timeline behind the estimate.",
      "citations": ["https://example.com/city-plan"]
    },
    {
      "text": "Bottom line: the announcement may be real, but the effect size is not yet independently demonstrated.",
      "citations": []
    }
  ]
}
```

## Social Post Prompt

```text
Use $lateral-reading on this post:

A screenshot says a regulator banned a medication today.
```

Good behavior:

- Locate the original regulator notice.
- Check whether the action was a ban, warning, recall, label update, proposal, or investigation.
- Check date and jurisdiction.
- Cite the regulator page and independent context.
- Say `unverified` if the original notice cannot be located.
