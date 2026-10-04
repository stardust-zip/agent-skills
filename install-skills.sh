#!/usr/bin/env bash
# Links my skills and personas into every AI tool's skill directory, for
# machines without home-manager (the work laptop). Mirrors the layout the
# Nix modules in programs/ produce. Everything is a symlink into this
# checkout, so `git pull` updates all tools at once; rerun this script after
# a pull that adds or removes a skill.
#
# Never touches an existing file or directory that is not a link into this
# checkout, so skills installed by anything else are left alone.
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)"
skills="$src/skills/software-engineering"
personas="$src/agents"

skill_dirs=(
  "$HOME/.claude/skills"
  "$HOME/.codex/skills"
  "$HOME/.gemini/antigravity-cli/skills"
  "$HOME/.agents/skills" # Zed; also gets personas, as it has no sub-agents
)

ours() { [ -L "$1" ] && [[ "$(readlink "$1")" == "$src"/* ]]; }

# link <target> <path>
link() {
  if ours "$2"; then
    ln -sfn "$1" "$2"
  elif [ -e "$2" ] || [ -L "$2" ]; then
    echo "skipped (exists, not managed by this script): $2"
    return
  else
    mkdir -p "$(dirname "$2")"
    ln -s "$1" "$2"
  fi
}

# install_skill <dir> <source>: a folder skill is linked whole; a single
# .md skill becomes <dir>/<name>/SKILL.md.
install_skill() {
  local name
  if [ -d "$2" ]; then
    link "$2" "$1/$(basename "$2")"
  else
    name="$(basename "$2" .md)"
    if [ -e "$1/$name" ] && ! [ -d "$1/$name" ]; then
      echo "skipped (exists, not managed by this script): $1/$name"
      return
    fi
    link "$2" "$1/$name/SKILL.md"
  fi
}

# Remove links into this checkout whose target is gone (a skill deleted
# upstream), then the empty <name>/ folders they leave behind.
prune() {
  [ -d "$1" ] || return 0
  find "$1" -maxdepth 2 -type l | while read -r path; do
    if ours "$path" && ! [ -e "$path" ]; then
      rm "$path"
      rmdir "$(dirname "$path")" 2>/dev/null || true
    fi
  done
}

# Skills that only make sense on my home-manager machines.
personal_only=(add-nix-package)

skill_sources=()
for file in "$skills"/*.md; do
  [[ " ${personal_only[*]} " == *" $(basename "$file" .md) "* ]] || skill_sources+=("$file")
done
for dir in "$skills"/*/; do
  if [ -f "$dir/SKILL.md" ]; then skill_sources+=("${dir%/}"); fi
done

for dir in "${skill_dirs[@]}"; do
  prune "$dir"
  for skill in "${skill_sources[@]}"; do
    install_skill "$dir" "$skill"
  done
done

for persona in "$personas"/*.md; do
  install_skill "$HOME/.agents/skills" "$persona"
done

# Claude Code and OpenCode read personas as sub-agents.
for dir in "$HOME/.claude/agents" "$HOME/.config/opencode/agents"; do
  prune "$dir"
  for persona in "$personas"/*.md; do
    link "$persona" "$dir/$(basename "$persona")"
  done
done

# OpenCode finds skills recursively under its skills directory.
prune "$HOME/.config/opencode/skills"
link "$skills" "$HOME/.config/opencode/skills/software-engineering"

echo "Linked ${#skill_sources[@]} skills and $(ls "$personas"/*.md | wc -l) personas from $src"
