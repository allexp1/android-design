# Contributing

Thanks for your interest in improving **android-design**.

## What's especially welcome

- **Guideline updates.** Google revises Material and the Android design guides through the year. PRs that correct a value or reflect a new direction, with a link to Google's current page, are the most valuable contribution.
- **Resolved conflicts and unverified items.** `ledger/claims.tsv` lists the values Google's pages state differently and the ones not yet confirmed. A primary source that settles one is welcome.
- **Worked examples** in `android-design/references/applying.md`.

## Ground rules

1. **Never paste Google's text verbatim.** Paraphrase and link to the page. Names are fine: component, token and API names, page titles.
2. **Source every fact.** Add or update a row in `ledger/claims.tsv` for any number, date or rule you add, with its URL and status.
3. **State conflicts as conflicts.** If two Google pages disagree, say so in the text and test both.
4. **Keep Play policy out of design rules.** Store policy belongs to the Play kit.
5. **Match the house style.** Each reference opens with *Applies to* and ends with *Sources*.

## Before you open a PR

```bash
bash scripts/build.sh --check
```

It is read-only and runs the frontmatter, routing, size, ledger, source and style checks.
