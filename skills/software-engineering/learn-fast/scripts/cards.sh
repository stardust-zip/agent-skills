#!/usr/bin/env bash
# Spaced-review cards for the learn-fast skill. Each topic folder holds one
# cards.tsv with the columns: id level box due question answer source.
# A card moves up a box when answered well and back to box 1 when missed;
# the box sets the days until it is due again (expanding intervals, the
# spacing effect). Dates are ISO (YYYY-MM-DD), so string order is date order.
set -euo pipefail

intervals=(0 1 3 7 16 35 75) # days, indexed by box 1..6
max_box=6
today=$(date +%F)
header=$'id\tlevel\tbox\tdue\tquestion\tanswer\tsource'

usage() {
  cat >&2 <<'EOF'
usage: cards.sh add <topic-dir> <level 1-4> <question> <answer> [source]
       cards.sh due <topic-dir>...          cards due today or earlier (no answers)
       cards.sh show <topic-dir> <id>        the answer and source of one card
       cards.sh grade <topic-dir> <id> again|hard|good
       cards.sh stats <topic-dir>...         total, due and per-box counts
EOF
  exit 2
}

field_ok() { [[ "$1" != *$'\t'* && "$1" != *$'\n'* ]]; }

card_file() {
  [ -f "$1/cards.tsv" ] || { echo "no cards in $1" >&2; exit 1; }
  printf '%s/cards.tsv' "$1"
}

cmd="${1:-}"
[ -n "$cmd" ] || usage
shift

case "$cmd" in
  add)
    [ $# -ge 4 ] || usage
    dir="$1" level="$2" question="$3" answer="$4" source="${5:-}"
    [[ "$level" =~ ^[1-4]$ ]] || { echo "level must be 1-4" >&2; exit 2; }
    for value in "$question" "$answer" "$source"; do
      field_ok "$value" || { echo "fields may not contain tabs or newlines" >&2; exit 2; }
    done
    mkdir -p "$dir"
    file="$dir/cards.tsv"
    [ -f "$file" ] || printf '%s\n' "$header" >"$file"
    id=$(awk -F'\t' 'NR > 1 && $1 + 0 > max { max = $1 + 0 } END { print max + 1 }' "$file")
    due=$(date -d "$today + ${intervals[1]} day" +%F)
    printf '%s\t%s\t1\t%s\t%s\t%s\t%s\n' "$id" "$level" "$due" "$question" "$answer" "$source" >>"$file"
    echo "added card $id (due $due)"
    ;;

  due)
    [ $# -ge 1 ] || usage
    for dir in "$@"; do
      [ -f "$dir/cards.tsv" ] || continue
      awk -F'\t' -v today="$today" -v topic="$(basename "$dir")" \
        'NR > 1 && $4 <= today { print topic "\t" $1 "\tlevel " $2 "\t" $5 }' "$dir/cards.tsv"
    done
    ;;

  show)
    [ $# -eq 2 ] || usage
    file=$(card_file "$1")
    awk -F'\t' -v id="$2" 'NR > 1 && $1 == id { print "answer: " $6; if ($7 != "") print "source: " $7; found = 1 }
      END { if (!found) { print "no card " id > "/dev/stderr"; exit 1 } }' "$file"
    ;;

  grade)
    [ $# -eq 3 ] || usage
    file=$(card_file "$1")
    id="$2" result="$3"
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
    for dir in "$@"; do
      [ -f "$dir/cards.tsv" ] || continue
      awk -F'\t' -v today="$today" -v topic="$(basename "$dir")" '
        NR > 1 { total++; boxes[$3]++; if ($4 <= today) due++ }
        END {
          line = sprintf("%s: %d cards, %d due", topic, total, due)
          for (b = 1; b <= 6; b++) line = line sprintf(", box%d=%d", b, boxes[b] + 0)
          print line
        }' "$dir/cards.tsv"
    done
    ;;

  *) usage ;;
esac
