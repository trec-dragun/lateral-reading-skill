# Input Preparation

Use this reference before the investigation. The renderer should receive a plain text target file, so normalize the user's input first.

## Output File

Create `target.txt` in the run output folder. Use this structure when fields are available:

```text
Title: ...
Source: ...
Author: ...
Date: ...
URL: ...
Input type: article | url | screenshot | post | claim | unknown

...
```

After the blank line, include the extracted article, post, claim, or screenshot text. Preserve meaningful headings, captions, quotes, dates, and visible labels. Remove navigation menus, cookie banners, ads, newsletter prompts, unrelated recommendations, and boilerplate.

## Pasted Text

If the user pasted the article or post:

- Copy the relevant text into `target.txt`.
- Add title, source, date, author, and URL only when present in the pasted content or provided by the user.
- Do not "clean up" wording in a way that changes the claim.

## URL

If the user provided a URL:

- Open or fetch the URL with available browsing tools.
- Extract the title, source or site name, author, date, canonical URL, and main article text.
- Include the original URL in the `URL:` field.
- If the page is inaccessible, paywalled, blocked, or mostly script-rendered and tools cannot extract it, ask the user to paste the article text or provide screenshots.
- Do not rely on snippets or search result summaries as the target article text unless the user explicitly wants to assess the snippet.

## Screenshot

If the user provided a screenshot:

- Read the visible text from the screenshot into `target.txt`.
- Use `Input type: screenshot`.
- Include a short note such as `Source: user-provided screenshot` when no outlet or URL is visible.
- Preserve visible title, account name, outlet, date, caption, and body text.
- If text is cropped or illegible, transcribe what is visible and state the limitation in the report, or ask for a clearer image when the missing content is central.

## Short Claim Or Tweet

If the input is only a short claim, tweet, or post:

- Still create `target.txt`.
- Use `Input type: claim` or `Input type: post`.
- Put the full claim or post text after the blank line.
- During investigation, search for the original post or strongest primary source before judging the claim.
