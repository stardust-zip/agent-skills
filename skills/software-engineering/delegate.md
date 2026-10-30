---
name: delegate
description: Hands a task to another coding-agent harness (Codex, Claude Code, OpenCode, pi, Copilot, Cursor) and brings its answer back - a second opinion, a review, a parallel subtask, or work better suited to another model. Use when the user asks to delegate, to have another agent or model do or check something, or for a cross-check by a different harness.
---

# Delegate to another harness

The other agent starts with none of your context. The task you send must stand on its own.

## 1. Pick the harness

Use the one the user named. Otherwise pick one that is not you; for a second opinion, prefer a different vendor. Check it is installed (`command -v <cmd>`):

| Harness | Command | herdr kind |
|---|---|---|
| Codex | `codex` | `codex` |
| Claude Code | `claude` | `claude` |
| OpenCode | `opencode` | `opencode` |
| pi | `pi` | `pi` |
| Copilot | `copilot` | `copilot` |
| Cursor | `cursor-agent` | `cursor` |

## 2. Write the task

Include: the goal, the files or paths involved, constraints, the exact form of the answer you want back, and "Do not commit, push or delete anything." Never include secrets or credentials.

For edits, record the parent checkout, its HEAD, and `git status --short` before starting. A new worktree contains committed files only. If the task depends on local changes, copy only the relevant tracked diff (`git diff HEAD -- <paths>`, including staged changes) and required untracked files into the worktree, then inspect the result. Do not copy secrets or unrelated work. Record this starting diff separately so the delegate's changes can be distinguished from inherited changes. Never stash, reset, or commit the user's work to prepare delegation.

Agree on file ownership and the expected validation. Keep editing agents isolated in worktrees. If the user has not authorized that topology, request a worktree explicitly before delegating edits; read-only delegation can proceed in a sibling pane. A general request to delegate does not itself request a worktree. If worktrees are declined, delegate a review or proposed patch instead of concurrent edits in the parent checkout.

## 3a. Inside herdr (`test "${HERDR_ENV:-}" = 1`)

The user can watch it in herdr's sidebar and take over. Load the `herdr` skill for command syntax and session rules. Its explicit-topology rule applies here too; this skill does not override it.

1. Make room, keeping the user's focus:
   - Read-only work (review, question, research): inspect `herdr pane layout --pane "$HERDR_PANE_ID"`; split right if wide or down if narrow. Use `herdr pane split --current --direction <right|down> --cwd "$PWD" --no-focus` and read `.result.pane.pane_id`.
   - Authorized editing worktree: `herdr worktree create --cwd "$PWD" --branch agent/<name> --no-focus`. Use `.result.root_pane.pane_id`, discover the returned checkout path, and tell the user the branch and path.
2. Start it: `herdr agent start <name> --kind <kind> --pane <pane-id>`. Names match `[a-z][a-z0-9_-]{0,31}`; reserve space for a random suffix to avoid collisions. If startup fails, inspect its error and pane before proceeding. A blocked startup is not ready to accept a prompt.
3. Send the task and wait: `herdr agent prompt <name> "<task>" --wait --timeout 900000`.
4. If it ends `blocked`, it is waiting on an approval or question. Read it with `herdr agent read <name> --source recent-unwrapped --lines 80`, then ask the user before answering for them.
5. Read the answer: `herdr agent read <name> --source recent-unwrapped --lines 200`. For a long answer, ask it to write to `/tmp/<name>.md` and reply with only the path, then read the file.
6. Leave its pane open so the user can continue there, unless they asked you to clean up.

If startup, prompting, or waiting returns a timeout, `agent_prompt_stalled`, or another error, inspect `herdr agent get <name>` and `herdr agent read <name> --source recent-unwrapped --lines 120` before acting. The task may already have been delivered: never blindly resend it or start a duplicate. If still working, wait again with a bounded timeout; if blocked, let the user handle the question or approval. An `unknown` state is not completion. Verify a settled result against the requested artifact or answer. If delivery remains uncertain, report the state and leave the agent available rather than retrying indefinitely.

## 3b. Outside herdr

Run the harness once, non-interactively, and capture what it prints. Start it in the background if your tool allows, since it can take minutes.

| Harness | One-shot command |
|---|---|
| Claude Code | `claude -p "<task>"` |
| Codex | `codex exec -C <dir> "<task>"`; add `-s workspace-write` only if it must edit files |
| OpenCode | `opencode run "<task>"` |
| pi | `pi -p "<task>"` |
| Copilot | `copilot -p "<task>"` |

For authorized code changes, give it a uniquely named worktree first (`git worktree add <path> -b agent/<name>`) and run it there. Apply the same parent-state and handoff rules as inside herdr. Capture output and the exit status; inspect artifacts after a failure before retrying.

## 4. Report back

Say which harness answered, then give its findings in your own words, separating what you checked from what you only relayed. If it changed code, review its diff yourself before presenting it, and point to the branch or worktree.

For edits, require the changed paths, validation commands/results, and remaining issues. Review the actual worktree diff, including untracked files, against its recorded starting state. Because delegates do not commit, their branch alone is not a handoff: preserve the patch or worktree path.

When integrating is within the user's request, transfer only the delegate's changes relative to that starting state. Check the parent for intervening edits first; use an inspected patch with `git apply --check` before applying, and transfer required new files deliberately. If the check fails, reconcile the overlap without overwriting parent work. Validate the combined result in the parent checkout and report any checks that could not run. Do not automatically cherry-pick an uncommitted branch or copy whole files over newer parent changes.

Keep the pane and worktree until the result has been reviewed and integrated. Remove only resources you created, only when cleanup was requested, and only after confirming no untransferred changes remain. Never force-remove a dirty worktree.
