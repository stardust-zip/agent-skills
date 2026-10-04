# Agent skills

My skills and personas for Claude Code, Codex, OpenCode, Zed and Antigravity.

This repository is a generated mirror of `opencode/` in my home-manager config, published with `publish-skills`. Do not commit here; changes made here are overwritten on the next publish.

## Install (machines without home-manager)

```bash
git clone git@github.com:stardust-zip/agent-skills.git ~/agent-skills
~/agent-skills/install-skills.sh
```

The script symlinks every skill and persona into each tool's directory and never replaces anything it did not create. To update, run `git pull` in `~/agent-skills`, then rerun the script so added or removed skills are picked up.

## Work machine

On the work laptop, also run the `work-setup` skill (or `bash skills/software-engineering/work-setup/scripts/install.sh`). It creates `~/work-docs`, which switches the skills to writing Markdown outside work repositories, and installs a pre-push hook that blocks pushing Markdown.
