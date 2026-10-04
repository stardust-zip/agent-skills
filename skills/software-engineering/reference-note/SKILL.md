---
name: reference-note
description: Writes AI-researched reference notes for lookup - concept overviews, hands-on kickstart guides and annotated cheatsheets - into the user's note vault, always marked type reference and sourced, never counted as known. Use when the user asks for a cheatsheet, a how-to or kickstart, or a reference write-up on a topic.
---

# Reference Note

Reference notes are for looking things up while working: commands, syntax, steps, comparisons. They may be AI-written because their job is external storage, not learning. They never count as something the user knows; learning notes (`type: learning`) are written by the user through `note-coach`.

## The vault

- **Work machine** (`~/work-docs/` exists): `~/work-docs/notebook/notes/`, never synced. Examples may use the user's real services (via `service-map`).
- **Personal machines:** `<vault>/notes/`, where `<vault>` is the first that exists of: the current Git repository, if it is the vault (its root has `notes/` and an `AGENTS.md` that describes `cards/` and learning notes), which is the case in a cloud session from the Claude app; `$NOTEBOOK_DIR`; `~/notebook` (the phone); `~/projects/gitea/gitkeeper/notebook` (the laptop). If none exists, ask where the notebook clone is. Never write company details here; keep internal systems generic.

On personal machines:
- **Sync only when the user agrees.** Before touching the vault, ask whether to pull the latest version first (pull, or work locally), in the same question batch as the other setup questions rather than as a round of its own. At the end, ask what to do with the changes: commit and push, commit only, or leave uncommitted.
- When committing, stage only the files you touched, with the repo's convention: `note-creation: <topic>` for a new note, `note-update: <topic>` otherwise.
- Git may ask for a password, which this session cannot type. If a pull or push fails that way, say so in one line, keep working locally, and suggest the user run the same command themselves with a leading `!`. Never retry in a loop, and never force-push.
- In a cloud session (Claude Code on the web or in the Claude app) the repository is a fresh clone, so skip the pull question. At the end, still ask before committing, then follow the session's own git workflow; it may push to a branch of its own for the user to merge.

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

No `status` or `level`: reference notes have no learning status.

## Style

The user's vault style: headings over bullet lists for points that deserve explanation, short single-idea paragraphs, bold key terms at first mention, italics for contrast, callouts (`> [!warning]`, `> [!tip]`) for emphasis, a `mermaid` diagram only when a flow or hierarchy is clearer as a picture, a comparison table when the topic is naturally contrasted. Exactly one blank line between the frontmatter and the title. Link an existing note with a wikilink at its first natural mention; do not force links.

Keep it to what someone needs at lookup time. A cheatsheet is a page, not a tutorial.

## After writing

Report the file written and its sources. Then offer, in one line, a `learn-fast` check on the topic if the user wants proof they know it; reading a reference note is not learning it.
