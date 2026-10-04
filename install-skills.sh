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

# Skills and personas that only make sense on my personal machines.
personal_only=(add-nix-package youtuber fiction-cowriter fiction-reviewer obsidian-writer)
is_personal() { [[ " ${personal_only[*]} " == *" $(basename "$1" .md) "* ]]; }

# work-only/ holds skills home-manager does not deploy (lean-code replaces
# ponytail where third-party skills are not allowed).
skill_sources=()
for file in "$skills"/*.md; do
  is_personal "$file" || skill_sources+=("$file")
done
for dir in "$skills"/*/ "$src"/work-only/*/; do
  if [ -f "$dir/SKILL.md" ]; then skill_sources+=("${dir%/}"); fi
done

persona_sources=()
for persona in "$personas"/*.md; do
  is_personal "$persona" || persona_sources+=("$persona")
done

# Earlier versions linked OpenCode's whole skills folder; it now gets
# per-skill links like every other tool.
old="$HOME/.config/opencode/skills/software-engineering"
if ours "$old"; then rm "$old"; fi

# Remove links an earlier run made for anything now in personal_only.
for dir in "${skill_dirs[@]}" "$HOME/.config/opencode/skills" "$HOME/.claude/agents" "$HOME/.config/opencode/agents"; do
  for name in "${personal_only[@]}"; do
    for path in "$dir/$name" "$dir/$name/SKILL.md" "$dir/$name.md"; do
      if ours "$path"; then rm "$path"; fi
    done
    rmdir "$dir/$name" 2>/dev/null || true
  done
done

for dir in "${skill_dirs[@]}" "$HOME/.config/opencode/skills"; do
  prune "$dir"
  for skill in "${skill_sources[@]}"; do
    install_skill "$dir" "$skill"
  done
done

for persona in "${persona_sources[@]}"; do
  install_skill "$HOME/.agents/skills" "$persona"
done

# Claude Code and OpenCode read personas as sub-agents.
for dir in "$HOME/.claude/agents" "$HOME/.config/opencode/agents"; do
  prune "$dir"
  for persona in "${persona_sources[@]}"; do
    link "$persona" "$dir/$(basename "$persona")"
  done
done

echo "Linked ${#skill_sources[@]} skills and ${#persona_sources[@]} personas from $src"
