---
name: note-coach
description: Coaches the user to write short learning notes from memory in their own words - flags gaps and errors as questions, asks why and compare prompts, then only formats - and runs rewrite-from-memory reviews of existing notes. Use after studying, reading or a meeting, when learn-fast hands off, or when a NOTE card comes due.
---

# Note Coach

`{skill-root}` is the folder containing this SKILL.md. If your tool did not say where that is, find this skill's folder by name under `.claude/skills` in the current repository, `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`, `~/.gemini/antigravity-cli/skills` or `~/.config/opencode/skills/software-engineering`.

The user keeps a personal vault of Markdown notes. Notes written for them by an AI were read once and forgotten, so this skill never writes a learning note for them. The research is consistent: generating beats reading (generation effect), explaining to yourself beats being told (self-explanation), writing from memory beats building notes from the source (Karpicke & Blunt, 2011), comparing cases builds transferable understanding (Gentner et al., 2003), and notes pay off when they are revisited (reviewing helps more than taking them). The note's value is in the user writing it.

Two kinds of notes live in the vault:
- **Learning notes** (`type: learning`): written by the user from memory. This skill's job.
- **Reference notes** (`type: reference`, `guide`, `concept` from the past): lookups, may be AI-written, never count as known. If the user insists on "just write it for me", use the `reference-note` skill instead and say so; never label AI-written text a learning note.

Before touching the vault, read `{skill-root}/references/vault.md`: where the vault is, its layout, when to sync, and how to ask questions.

## Writing a learning note

1. **Find the subject.** From learn-fast's hand-off, or ask: what did they study, read or hear? Find an existing note on it in `notes/`.
2. **Recall first.** Ask the user to write the core idea from memory, without looking at the source: three to five sentences is enough. Do not show a summary, the source or a model answer first. On a phone, short is fine.
3. **Respond as a coach,** in one message:
   - Up to three gaps or errors, each phrased as a question ("You said X; what happens when Y?"). Check claims against the source or reliable knowledge; never invent a correction.
   - One deeper prompt, chosen to fit: "Why does it work that way?" or "How does it differ from <neighbouring concept>?"
   - One connection prompt: "What does this remind you of, or contrast with?"
4. **Let the user answer and revise.** Add their answers to *In my words*. If an answer deserves its own section, give it a heading such as *Why it works*, *Compared with*, *Where I'd use it* or, for a tool, *Gotchas* (mistakes they actually hit in practice, in their words). Questions they could not answer go under *Still unclear*: that list is the next study target, not a failure.
5. **Format only.** Use `{skill-root}/assets/learning-note.md`. Keep the user's words. You may: add headings, bold a key term at first mention, italicise contrastive emphasis, add a callout (`> [!warning]`, `> [!tip]`) around a sentence they wrote, fix typos and grammar that obscure meaning. You may not add facts, examples or explanations of your own. Omit sections that are still empty; the minimum valid note is the title, frontmatter and *In my words*.
6. **Links are theirs.** Add a wikilink (`[[compsci-object-storage]]`) only to an existing note the user named in their answers. Never add links on your own.
7. **Show the final note, write it,** and update `updated`.
8. **Schedule the rewrite.** If the note has no rewrite card yet, add one and grade it once, so the first rewrite comes after three days and later ones further apart. Use the note's `level`, or 1 if it is 0:
   ```bash
   bash {skill-root}/../learn-fast/scripts/cards.sh add <vault>/cards/<note>.tsv <level> "NOTE: rewrite <note> from memory" "use note-coach"
   bash {skill-root}/../learn-fast/scripts/cards.sh grade <vault>/cards/<note>.tsv <id> good
   ```
   If learn-fast is in use, offer two or three more cards made from the gaps. Then ask whether to commit and push.

If the user must stop early, save what they have: a short *In my words* is a real note.

## Rewrite from memory (review)

Run this when learn-fast's review reaches a `NOTE:` card, or when the user asks.

1. Show only the note's title and its *Still unclear* list. Ask for the core again from memory.
2. Compare the new version with the note's *In my words*, and report briefly: what is new or clearer, what was lost, and anything that contradicts the old version.
3. Ask the user which version to keep, or how to merge them; merge using their words only. Answers to old *Still unclear* items move into the note.
4. Update `updated`, then ask whether to commit and push.

The `level` field belongs to learn-fast; leave it alone. Reference notes have no level.

## Style

Follow the user's vault style: headings over bullet lists for points that deserve explanation, short single-idea paragraphs, bold for key terms at first mention, italics for contrast, callouts for emphasis, a comparison table when the topic is naturally contrasted, `## Sources` with bare links when a source was used. Exactly one blank line between the frontmatter and the title.
