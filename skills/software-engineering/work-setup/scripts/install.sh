#!/usr/bin/env bash
# Sets up a work machine: ~/work-docs as a local Git repository with no
# remote, and a global pre-push hook that blocks pushing Markdown files.
set -euo pipefail

skill_root="$(cd "$(dirname "$0")/.." && pwd)"
docs="$HOME/work-docs"
hooks="${XDG_CONFIG_HOME:-$HOME/.config}/git/work-hooks"
names=(applypatch-msg pre-applypatch post-applypatch pre-commit pre-merge-commit
  prepare-commit-msg commit-msg post-commit pre-rebase post-checkout post-merge
  post-rewrite pre-auto-gc push-to-checkout sendemail-validate)

current="$(git config --global --get core.hooksPath || true)"
if [ -n "$current" ] && [ "$current" != "$hooks" ]; then
  echo "ERROR: core.hooksPath is already set globally to $current." >&2
  echo "Not overwriting it. Merge $skill_root/hooks/pre-push into that directory by hand." >&2
  exit 1
fi

mkdir -p "$docs"
if [ ! -d "$docs/.git" ]; then
  git -C "$docs" init -q
  echo "Created $docs as a local Git repository (no remote)."
fi

mkdir -p "$hooks"
install -m 755 "$skill_root/hooks/pre-push" "$hooks/pre-push"
install -m 755 "$skill_root/hooks/chain" "$hooks/chain"
for name in "${names[@]}"; do
  ln -sf chain "$hooks/$name"
done
git config --global core.hooksPath "$hooks"
echo "Installed the Markdown push guard in $hooks (global core.hooksPath)."
