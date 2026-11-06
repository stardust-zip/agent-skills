# The note vault

Shared by `learn-fast`, `note-coach` and `reference-note`.

Each machine keeps its own vault; nothing is ever copied from the work machine to a personal one, or the other way.

- **Work machine** (`~/work-docs/` exists): `~/work-docs/notebook/`, never synced. Examples may use the user's real services (via `service-map`).
- **Personal machines:** the first that exists of: the current Git repository, if it is the vault (its root has `notes/` and an `AGENTS.md` that describes `cards/` and learning notes), which is the case in a cloud session from the Claude app; `$NOTEBOOK_DIR`; `~/notebook` (the phone); `~/projects/gitea/gitkeeper/notebook` (the laptop). If none exists, ask the user where their notebook clone is (and suggest setting `NOTEBOOK_DIR`); never create a new vault silently.

Layout: flat `notes/` (one Markdown file per topic, YAML frontmatter) and flat `cards/` (review cards, one TSV per topic, same base name as the note). File names are domain-prefixed (`compsci-object-storage`); reuse the existing note for a topic rather than creating a second one.

## Rules on personal machines

- **No company details.** Use public knowledge only. If the user mentions an internal system, keep it generic ("your company's file-storage wrapper") and never write internal names, data or designs into the vault.
- **Sync only when the user agrees.** Before touching the vault, ask whether to pull the latest version first (pull, or work locally), in the same question batch as the other setup questions rather than as a round of its own. At the end, ask what to do with the changes: commit and push, commit only, or leave uncommitted.
- When committing, stage only the files you touched, with the repo's convention: `note-creation: <topic>` for a new note, `note-update: <topic>` otherwise.
- Git may ask for a password, which this session cannot type. If a pull or push fails that way, say so in one line, keep working locally, and suggest the user run the same command themselves with a leading `!`. Never retry in a loop, and never force-push.
- In a cloud session (Claude Code on the web or in the Claude app) the repository is a fresh clone, so skip the pull question. At the end, still ask before committing, then follow the session's own git workflow; it may push to a branch of its own for the user to merge.

## Asking

- **Choices go through the question tool.** If the environment has a structured question tool (for example AskUserQuestion), use it for every choice between options: which meaning of a term, the goal and target level, the mode, the kind of note, syncing, keeping or merging a rewrite. Batch up to four of them into a single call. Without such a tool, use a short numbered list.
- **Quiz and recall questions never do.** They stay open, typed answers, because producing an answer from memory is what builds it; picking from options only tests recognition. The user types the answer and a confidence rating (1 guess, 2 fairly sure, 3 certain) together.
