---
name: work-setup
description: Sets up a work machine so docs never reach the company Git host - creates ~/work-docs and installs a pre-push hook blocking Markdown. Use when setting up the work machine or when that hook blocked a push.
---

# Work Setup

The user's company forbids pushing docs (Markdown files) to its internal Git host. Committing locally is allowed, but a local commit can be pushed by accident. The user does work on a separate work machine and personal projects elsewhere, with the same skills on both.

Two parts work together:
- **`~/work-docs/`**: its existence marks a work machine. The skills `task-decoder`, `design-doc`, `api-docs` and `ds-ml-research` then write every Markdown file to `~/work-docs/<repo-name>/<path it would have had in the repo>` instead of into the repository. It is a Git repository with no remote, so the user still gets history.
- **The push guard**: a global `pre-push` hook that refuses a push if any commit being pushed adds or changes a `.md`, `.markdown` or `.mdx` file. It is the backstop for when a Markdown file ends up in a work repository anyway.

Never create `~/work-docs/` on a machine the user has not confirmed is a work machine: it switches every skill into work mode.

## Install

1. Confirm with the user that this is their work machine.
2. Check for a global `core.hooksPath` that is already set (`git config --global --get core.hooksPath`). If one exists, the installer stops rather than overwrite it. Show the user what is there and offer to merge the guard into that directory by hand.
3. Check whether the company already manages Git hooks on this machine (a company-installed hooks path, or tooling that sets one). If so, ask before installing.
4. Run:

   ```bash
   bash {skill-root}/scripts/install.sh
   ```

   It creates `~/work-docs` with `git init` (no remote), copies the hooks to `~/.config/git/work-hooks/`, and sets the global `core.hooksPath` there.
5. Verify in a throwaway repository: commit a `.md` file, push to a local bare remote, and confirm the push is blocked. Delete the throwaway repositories afterwards.

Do not add a remote to `~/work-docs`. If the user wants a backup, suggest one that stays inside company-approved storage, and let them decide.

## How the guard works, and its limits

- It checks every commit being pushed that the remote does not have yet, not just the final state, because a Markdown file added in one commit and deleted in a later one is still in the pushed history.
- Deleting a remote branch is always allowed.
- A global `core.hooksPath` makes Git ignore each repository's `.git/hooks/`. To keep per-repo hooks working, every other hook name in `~/.config/git/work-hooks/` links to `chain`, which runs the repository's own hook, and the guard runs the repository's `pre-push` after its own check.
- A repository that sets its own `core.hooksPath` (Husky does this) overrides the global one, so **the guard does not run there**. To check a repository: `git config --local --get core.hooksPath`. In such a repository, offer to add the guard to that repository's hook directory locally, without committing it.
- `git push --no-verify` skips all pre-push hooks, the guard included. That is deliberate, for files the company does allow; the user decides when to use it.
- Pushes made by tools that do not run Git hooks (some web UIs, some IDE integrations that use their own Git library) are not covered.

## When a push was blocked

The message lists each Markdown file and the commit that carries it. Help the user:
1. Copy the files to `~/work-docs/<repo-name>/<same path>`, and commit them there if they want history.
2. Remove them from the unpushed commits. If the Markdown commits are the most recent ones and contain nothing else, `git reset --soft` back to before them, unstage the Markdown files, and recommit. Otherwise use an interactive rebase, which the user runs themselves, since it needs an editor. Show the exact commands, and check `git log` with them first. Never rewrite commits that are already on the remote.
3. Push again.

## Uninstall

`git config --global --unset core.hooksPath`, then delete `~/.config/git/work-hooks/`. Leave `~/work-docs/` alone unless the user explicitly asks; it holds their docs.
