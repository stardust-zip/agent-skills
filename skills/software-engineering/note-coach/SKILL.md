---
name: note-coach
description: Coaches the user to write short learning notes from memory in their own words - flags gaps and errors as questions, asks why and compare prompts, then only formats - and runs rewrite-from-memory reviews of existing notes. Use after studying, reading or a meeting, when learn-fast hands off, or when a note is due for review.
---

# Note Coach

`{skill-root}` is the folder containing this SKILL.md. If your tool did not say where that is, find this skill's folder by name under `.claude/skills` in the current repository, `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`, `~/.gemini/antigravity-cli/skills` or `~/.config/opencode/skills/software-engineering`.

The user keeps a personal vault of Markdown notes. Notes written for them by an AI were read once and forgotten, so this skill never writes a learning note for them. The research is consistent: generating beats reading (generation effect), explaining to yourself beats being told (self-explanation), writing from memory beats building notes from the source (Karpicke & Blunt, 2011), comparing cases builds transferable understanding (Gentner et al., 2003), and notes pay off when they are revisited (reviewing helps more than taking them). The note's value is in the user writing it.

Two kinds of notes live in the vault:
- **Learning notes** (`type: learning`): written by the user from memory. This skill's job.
- **Reference notes** (`type: reference`, `guide`, `concept` from the past): lookups, may be AI-written, never count as known. If the user insists on "just write it for me", use the `reference-note` skill instead and say so; never label AI-written text a learning note.

## The vault

- **Work machine** (`~/work-docs/` exists): `~/work-docs/notebook/`, never synced.
- **Personal machines:** the first that exists of: the current Git repository, if it is the vault (its root has `notes/` and an `AGENTS.md` that describes `cards/` and learning notes), which is the case in a cloud session from the Claude app; `$NOTEBOOK_DIR`; `~/notebook` (the phone); `~/projects/gitea/gitkeeper/notebook` (the laptop). If none exists, ask the user where their notebook clone is (and suggest setting `NOTEBOOK_DIR`); never create a new vault silently.

Layout: flat `notes/` (one Markdown file per topic, YAML frontmatter) and flat `cards/` (review cards, one TSV per topic, same base name as the note). File names are domain-prefixed like the existing ones (`compsci-object-storage`); reuse the existing note for a topic rather than creating a second one.

On personal machines:
- **Sync only when the user agrees.** Before touching the vault, ask whether to pull the latest version first (pull, or work locally), in the same question batch as the other setup questions rather than as a round of its own. At the end, ask what to do with the changes: commit and push, commit only, or leave uncommitted.
- When committing, stage only the files you touched, with the repo's convention: `note-creation: <topic>` for a new note, `note-update: <topic>` otherwise.
- Git may ask for a password, which this session cannot type. If a pull or push fails that way, say so in one line, keep working locally, and suggest the user run the same command themselves with a leading `!`. Never retry in a loop, and never force-push.
- In a cloud session (Claude Code on the web or in the Claude app) the repository is a fresh clone, so skip the pull question. At the end, still ask before committing, then follow the session's own git workflow; it may push to a branch of its own for the user to merge.
- **No company details.** If the user mentions an internal system, keep it generic and never write internal names, data or designs into the vault.

## Asking

- **Choices go through the question tool.** If the environment has a structured question tool (for example AskUserQuestion), use it for every choice between options: which meaning of a term, the goal and target level, the mode, syncing, keeping or merging a rewrite. Batch up to four of them into a single call. Without such a tool, use a short numbered list.
- **Quiz and recall questions never do.** They stay open, typed answers, because producing an answer from memory is what builds it; picking from options only tests recognition. The user types the answer and a confidence rating (1 guess, 2 fairly sure, 3 certain) together.

## Writing a learning note

1. **Find the subject.** From learn-fast's hand-off, or ask: what did they study, read or hear? Find an existing note on it in `notes/`.
2. **Recall first.** Ask the user to write the core idea from memory, without looking at the source: three to five sentences is enough. Do not show a summary, the source or a model answer first. On a phone, short is fine.
3. **Respond as a coach,** in one message:
   - Up to three gaps or errors, each phrased as a question ("You said X; what happens when Y?"). Check claims against the source or reliable knowledge; never invent a correction.
   - One deeper prompt, chosen to fit: "Why does it work that way?" or "How does it differ from <neighbouring concept>?"
   - One connection prompt: "What does this remind you of, or contrast with?"
4. **Let the user answer and revise.** Place their answers in the sections: *Why it works*, *Compared with*, *Where I'd use it*. Questions they could not answer go under *Still unclear*: that list is the next study target, not a failure.
5. **Format only.** Use `{skill-root}/assets/learning-note.md`. Keep the user's words. You may: add headings, bold a key term at first mention, italicise contrastive emphasis, add a callout (`> [!warning]`, `> [!tip]`) around a sentence they wrote, fix typos and grammar that obscure meaning. You may not add facts, examples or explanations of your own. Omit sections that are still empty; the minimum valid note is the title, frontmatter and *In my words*.
6. **Links are theirs.** Add a wikilink (`[[compsci-object-storage]]`) only to an existing note the user named in their answers. Never add links on your own.
7. **Show the final note, write it,** update `updated`, and ask whether to commit and push. If learn-fast is in use, offer two or three cards made from the gaps, added with learn-fast's script (`{skill-root}/../learn-fast/scripts/cards.sh add <vault>/cards/<note>.tsv ...`).

If the user must stop early, save what they have: a short *In my words* is a real note.

## Rewrite from memory (review)

Run this when learn-fast's review mode hands over a note, or when the user asks. Due notes come from `{skill-root}/../learn-fast/scripts/cards.sh notes-due <vault>/notes`.

1. Show only the note's title and its *Still unclear* list. Ask for the core again from memory.
2. Compare the new version with the note's *In my words*, and report briefly: what is new or clearer, what was lost, and anything that contradicts the old version.
3. Ask the user which version to keep, or how to merge them; merge using their words only. Answers to old *Still unclear* items move into the right sections.
4. Update `last_reviewed` and `updated`. Raise `status` from `seed` to `growing` after a successful rewrite. Then ask whether to commit and push.

## Status rules

Status follows evidence, never effort or length:
- `seed`: written.
- `growing`: rewritten from memory at least once.
- `green`: a learn-fast check passed at level 3 or higher. Only learn-fast sets this.
- `level` (0–4): the highest level learn-fast has recorded as `placed` or `known`.

Reference notes have no learning status; leave theirs alone.

## Style

Follow the user's vault style: headings over bullet lists for points that deserve explanation, short single-idea paragraphs, bold for key terms at first mention, italics for contrast, callouts for emphasis, a comparison table when the topic is naturally contrasted, `## Sources` with bare links when a source was used. Exactly one blank line between the frontmatter and the title.
