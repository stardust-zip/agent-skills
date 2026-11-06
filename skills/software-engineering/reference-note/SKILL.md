---
name: reference-note
description: Writes AI-researched reference notes for lookup - concept overviews, hands-on kickstart guides and annotated cheatsheets - into the user's note vault, always marked type reference and sourced, never counted as known. Use when the user asks for a cheatsheet, a how-to or kickstart, or a reference write-up on a topic; in the notebook vault, use this rather than a document or docs skill.
---

# Reference Note

`{skill-root}` is the folder containing this SKILL.md. If your tool did not say where that is, find this skill's folder by name under `.claude/skills` in the current repository, `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`, `~/.gemini/antigravity-cli/skills` or `~/.config/opencode/skills/software-engineering`.

Reference notes are for looking things up while working: commands, syntax, steps, comparisons. They may be AI-written because their job is external storage, not learning. They never count as something the user knows; learning notes (`type: learning`) are written by the user through `note-coach`.

Before touching the vault, read `{skill-root}/../note-coach/references/vault.md`: where the vault is, its layout, when to sync, and how to ask questions. Reference notes go in `<vault>/notes/`.

## What to write

Write only what the user asked for. If they asked for "a note on X" without saying which kind, ask which kind with the structured question tool if the environment has one (recommend the best fit first), batched with the sync question; otherwise pick the one kind that fits best and say why in one line. Never produce a set.

| Kind | File name | When it fits | Contents |
|---|---|---|---|
| Concept | `<prefix>-<topic>-reference` | An overview to look up later | Definition, how it works, real named examples with checkable facts, a comparison table with neighbouring concepts, when not to use it |
| Kickstart | `<prefix>-<topic>-kickstart` | A practicable skill with hands-on steps | Numbered steps the reader actually does, Linux commands only, how to verify each step |
| Cheatsheet | `<prefix>-<topic>-cheatsheet` | Discrete commands, syntax or terms | Each entry annotated as good practice or a footgun, and why |

Before writing, check `notes/` for an existing note on the topic. Update it rather than creating a near-duplicate. If a learning note exists for the topic, do not touch it; a reference note can sit next to it.

## Research

Check current sources with web search before writing anything that can drift (versions, commands, APIs, pricing, health, job-market advice). Verify every command and syntax entry against current documentation; an outdated "good practice" annotation is worse than none. End with `## Sources`, bare links. If web search is unavailable, say so in the note's summary and mark claims you could not check.

## Frontmatter

```yaml
domain: # one of the vault's domains, e.g. computer-science
aliases:
  - # readable title, without the domain prefix
tags: # max 5, lowercase, hyphen-separated
  -
type: reference
summary: "One to two sentences."
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

No `level`: reference notes have no learning record.

## Style

The user's vault style: headings over bullet lists for points that deserve explanation, short single-idea paragraphs, bold key terms at first mention, italics for contrast, callouts (`> [!warning]`, `> [!tip]`) for emphasis, a `mermaid` diagram only when a flow or hierarchy is clearer as a picture, a comparison table when the topic is naturally contrasted. Exactly one blank line between the frontmatter and the title. Link an existing note with a wikilink at its first natural mention; do not force links.

Keep it to what someone needs at lookup time. A cheatsheet is a page, not a tutorial.

## After writing

Report the file written and its sources. Then offer, in one line, a `learn-fast` check on the topic if the user wants proof they know it; reading a reference note is not learning it.
