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

## 3a. Inside herdr (`test "${HERDR_ENV:-}" = 1`)

The user can watch it in herdr's sidebar and take over. The `herdr` skill covers the commands in depth.

1. Make room, keeping the user's focus:
   - Read-only work (review, question, research): a pane next to yours, `herdr pane split --current --direction right --cwd "$PWD" --no-focus`. Use `.result.pane.pane_id`.
   - Work that changes code: its own git worktree, so you never edit the same files, `herdr worktree create --cwd "$PWD" --branch agent/<name>`. Use `.result.root_pane.pane_id`, and tell the user the branch name.
2. Start it: `herdr agent start <name> --kind <kind> --pane <pane-id>`. The name is lowercase `[a-z][a-z0-9_-]`, unique and descriptive, such as `codex-review`.
3. Send the task and wait: `herdr agent prompt <name> "<task>" --wait --timeout 900000`.
4. If it ends `blocked`, it is waiting on an approval or question. Read it with `herdr agent read <name> --source recent-unwrapped --lines 80`, then ask the user before answering for them.
5. Read the answer: `herdr agent read <name> --source recent-unwrapped --lines 200`. For a long answer, ask it to write to `/tmp/<name>.md` and reply with only the path, then read the file.
6. Leave its pane open so the user can continue there, unless they asked you to clean up.

## 3b. Outside herdr

Run the harness once, non-interactively, and capture what it prints. Start it in the background if your tool allows, since it can take minutes.

| Harness | One-shot command |
|---|---|
| Claude Code | `claude -p "<task>"` |
| Codex | `codex exec -C <dir> "<task>"`; add `-s workspace-write` only if it must edit files |
| OpenCode | `opencode run "<task>"` |
| pi | `pi -p "<task>"` |
| Copilot | `copilot -p "<task>"` |

For code changes, give it a worktree first (`git worktree add ../<repo>-<name> -b agent/<name>`) and run it there.

## 4. Report back

Say which harness answered, then give its findings in your own words, separating what you checked from what you only relayed. If it changed code, review its diff yourself before presenting it, and point to the branch or worktree.
