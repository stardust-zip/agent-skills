#!/usr/bin/env bash
# Finds notes in the archived bronze-notebook that match a topic, so a
# learn-fast session can use them as source material. Read-only: it never
# changes the archive. Journal and literature notes are skipped (private
# diary entries and creative writing are not study material).
set -euo pipefail

archive="${BRONZE_NOTEBOOK_DIR:-$HOME/projects/gitea/gitkeeper/bronze-notebook}"
skip='^(jour|literature|freak)-'

[ $# -ge 1 ] || { echo "usage: bronze.sh <term>... (all terms must match)" >&2; exit 2; }
[ -d "$archive" ] || { echo "no archive at $archive (set BRONZE_NOTEBOOK_DIR)" >&2; exit 1; }

for note in "$archive"/*.md; do
  name=$(basename "$note" .md)
  [[ "$name" =~ $skip ]] && continue
  # Match against the file name and the frontmatter only, not the body.
  head=$(awk 'NR == 1 && $0 != "---" { exit } NR > 1 && $0 == "---" { exit } NR > 1 { print }' "$note")
  haystack="$name $head"
  matched=1
  for term in "$@"; do
    grep -qiF -- "$term" <<<"$haystack" || { matched=0; break; }
  done
  [ "$matched" = 1 ] || continue
  summary=$(awk -F': *' '$1 == "summary" { sub(/^summary: */, ""); gsub(/"/, ""); print; exit }' <<<"$head")
  printf '%s\t%s\n' "$name" "${summary:0:140}"
done
