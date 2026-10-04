#!/usr/bin/env bash
# Spaced review for the learn-fast and note-coach skills.
#
# Cards: one TSV per topic (cards/<topic>.tsv) with the columns
# id level box due question answer source. A card moves up a box when
# answered well and back to box 1 when missed; the box sets the days until
# it is due again (expanding intervals, the spacing effect).
#
# Notes: learning notes (frontmatter `type: learning`) come due for a
# rewrite from memory based on their status and `last_reviewed` date.
#
# Dates are ISO (YYYY-MM-DD), so string order is date order.
set -euo pipefail

intervals=(0 1 3 7 16 35 75) # card days, indexed by box 1..6
max_box=6
declare -A note_interval=([seed]=3 [growing]=14 [green]=45) # note days, by status
today=$(date +%F)
header=$'id\tlevel\tbox\tdue\tquestion\tanswer\tsource'

usage() {
  cat >&2 <<'EOF'
usage: cards.sh add <cards.tsv> <level 1-4> <question> <answer> [source]
       cards.sh due <cards.tsv>...           cards due today or earlier (no answers)
       cards.sh show <cards.tsv> <id>         the answer and source of one card
       cards.sh grade <cards.tsv> <id> again|hard|good
       cards.sh stats <cards.tsv>...          total, due and per-box counts
       cards.sh notes-due <notes-dir>         learning notes due for a rewrite from memory
       cards.sh notes-stale <notes-dir> [days] learning notes not reviewed for days (default 60)
EOF
  exit 2
}

field_ok() { [[ "$1" != *$'\t'* && "$1" != *$'\n'* ]]; }

need_file() { [ -f "$1" ] || { echo "no cards file $1" >&2; exit 1; }; }

topic_of() { basename "$1" .tsv; }

# frontmatter <file> <key>: the value of a top-level key in the YAML frontmatter.
frontmatter() {
  awk -v key="$2" '
    NR == 1 && $0 != "---" { exit }
    NR > 1 && $0 == "---" { exit }
    NR > 1 && index($0, key ":") == 1 { sub("^" key ":[ \t]*", ""); gsub(/["'\'']/, ""); print; exit }
  ' "$1"
}

cmd="${1:-}"
[ -n "$cmd" ] || usage
shift

case "$cmd" in
  add)
    [ $# -ge 4 ] || usage
    file="$1" level="$2" question="$3" answer="$4" source="${5:-}"
    [[ "$level" =~ ^[1-4]$ ]] || { echo "level must be 1-4" >&2; exit 2; }
    for value in "$question" "$answer" "$source"; do
      field_ok "$value" || { echo "fields may not contain tabs or newlines" >&2; exit 2; }
    done
    mkdir -p "$(dirname "$file")"
    [ -f "$file" ] || printf '%s\n' "$header" >"$file"
    id=$(awk -F'\t' 'NR > 1 && $1 + 0 > max { max = $1 + 0 } END { print max + 1 }' "$file")
    due=$(date -d "$today + ${intervals[1]} day" +%F)
    printf '%s\t%s\t1\t%s\t%s\t%s\t%s\n' "$id" "$level" "$due" "$question" "$answer" "$source" >>"$file"
    echo "added card $id (due $due)"
    ;;

  due)
    [ $# -ge 1 ] || usage
    for file in "$@"; do
      [ -f "$file" ] || continue
      awk -F'\t' -v today="$today" -v topic="$(topic_of "$file")" \
        'NR > 1 && $4 <= today { print topic "\t" $1 "\tlevel " $2 "\t" $5 }' "$file"
    done
    ;;

  show)
    [ $# -eq 2 ] || usage
    need_file "$1"
    awk -F'\t' -v id="$2" 'NR > 1 && $1 == id { print "answer: " $6; if ($7 != "") print "source: " $7; found = 1 }
      END { if (!found) { print "no card " id > "/dev/stderr"; exit 1 } }' "$1"
    ;;

  grade)
    [ $# -eq 3 ] || usage
    file="$1" id="$2" result="$3"
    need_file "$file"
    box=$(awk -F'\t' -v id="$id" 'NR > 1 && $1 == id { print $3 }' "$file")
    [ -n "$box" ] || { echo "no card $id" >&2; exit 1; }
    case "$result" in
      again) box=1 ;;
      hard) ;; # stays in its box
      good) box=$((box < max_box ? box + 1 : max_box)) ;;
      *) usage ;;
    esac
    due=$(date -d "$today + ${intervals[$box]} day" +%F)
    tmp=$(mktemp "$file.XXXXXX")
    awk -F'\t' -v OFS='\t' -v id="$id" -v box="$box" -v due="$due" \
      'NR > 1 && $1 == id { $3 = box; $4 = due } { print }' "$file" >"$tmp"
    mv "$tmp" "$file"
    echo "card $id: box $box, due $due"
    ;;

  stats)
    [ $# -ge 1 ] || usage
    for file in "$@"; do
      [ -f "$file" ] || continue
      awk -F'\t' -v today="$today" -v topic="$(topic_of "$file")" '
        NR > 1 { total++; boxes[$3]++; if ($4 <= today) due++ }
        END {
          line = sprintf("%s: %d cards, %d due", topic, total, due)
          for (b = 1; b <= 6; b++) line = line sprintf(", box%d=%d", b, boxes[b] + 0)
          print line
        }' "$file"
    done
    ;;

  notes-due)
    [ $# -eq 1 ] || usage
    for note in "$1"/*.md; do
      [ -f "$note" ] || continue
      [ "$(frontmatter "$note" type)" = learning ] || continue
      status=$(frontmatter "$note" status)
      last=$(frontmatter "$note" last_reviewed)
      [ -n "$last" ] || last=$(frontmatter "$note" created)
      days="${note_interval[$status]:-3}"
      due=$(date -d "${last:-$today} + $days day" +%F 2>/dev/null) || due="$today"
      if [[ "$due" < "$today" || "$due" == "$today" ]]; then
        printf '%s\t%s\tlast reviewed %s\n' "$(basename "$note" .md)" "${status:-seed}" "${last:-never}"
      fi
    done
    ;;

  notes-stale)
    [ $# -ge 1 ] || usage
    days="${2:-60}"
    cutoff=$(date -d "$today - $days day" +%F)
    for note in "$1"/*.md; do
      [ -f "$note" ] || continue
      [ "$(frontmatter "$note" type)" = learning ] || continue
      last=$(frontmatter "$note" last_reviewed)
      [ -n "$last" ] || last=$(frontmatter "$note" created)
      if [ -z "$last" ] || [[ "$last" < "$cutoff" ]]; then
        printf '%s\tlast reviewed %s\n' "$(basename "$note" .md)" "${last:-never}"
      fi
    done
    ;;

  *) usage ;;
esac
