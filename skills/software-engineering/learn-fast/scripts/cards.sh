#!/usr/bin/env bash
# Spaced review for the learn-fast and note-coach skills.
#
# Cards: one TSV per topic (cards/<topic>.tsv) with the columns
# id level box due question answer source. A card moves up a box when
# answered well and back to box 1 when missed; the box sets the days until
# it is due again (expanding intervals, the spacing effect). A missed card
# stays due today, so the same review can ask it once more.
#
# Questions and answers may span lines and hold tabs (code): they are stored
# escaped (\n, \t, \\) so each card stays one TSV row, and `ask` and `show`
# print them back as written. `due` lists them escaped, one card per line.
#
# Dates are ISO (YYYY-MM-DD), so string order is date order. "Today" is the
# machine's local date, or the date in $NOTEBOOK_TZ when set (cloud sessions
# run on UTC).
set -euo pipefail

intervals=(0 1 3 7 16 35 75) # card days, indexed by box 1..6
max_box=6
[ -z "${NOTEBOOK_TZ:-}" ] || export TZ="$NOTEBOOK_TZ"
today=$(date +%F)
header=$'id\tlevel\tbox\tdue\tquestion\tanswer\tsource'

usage() {
  cat >&2 <<'EOF'
usage: cards.sh add <cards.tsv> <level 1-4> <question> <answer> [source]
       cards.sh due <cards.tsv>...           cards due today or earlier (no answers)
       cards.sh ask <cards.tsv> <id>          the full question of one card
       cards.sh show <cards.tsv> <id>         the answer and source of one card
       cards.sh grade <cards.tsv> <id> again|hard|good
       cards.sh stats <cards.tsv>...          total, due and per-box counts
EOF
  exit 2
}

# escape <text>: one TSV-safe line; unescape is its inverse, in awk.
escape() {
  local s="${1//\\/\\\\}"
  s="${s//$'\t'/\\t}"
  printf '%s' "${s//$'\n'/\\n}"
}
unescape='function unescape(s,   out, c, i) {
  out = ""
  for (i = 1; i <= length(s); i++) {
    c = substr(s, i, 1)
    if (c == "\\" && i < length(s)) {
      c = substr(s, ++i, 1)
      c = c == "n" ? "\n" : c == "t" ? "\t" : c
    }
    out = out c
  }
  return out
}'

need_file() { [ -f "$1" ] || { echo "no cards file $1" >&2; exit 1; }; }

topic_of() { basename "$1" .tsv; }

cmd="${1:-}"
[ -n "$cmd" ] || usage
shift

case "$cmd" in
  add)
    [ $# -ge 4 ] || usage
    file="$1" level="$2" question="$3" answer="$4" source="${5:-}"
    [[ "$level" =~ ^[1-4]$ ]] || { echo "level must be 1-4" >&2; exit 2; }
    question=$(escape "$question") answer=$(escape "$answer") source=$(escape "$source")
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

  ask)
    [ $# -eq 2 ] || usage
    need_file "$1"
    awk -F'\t' -v id="$2" "$unescape"'
      NR > 1 && $1 == id { print unescape($5); found = 1 }
      END { if (!found) { print "no card " id > "/dev/stderr"; exit 1 } }' "$1"
    ;;

  show)
    [ $# -eq 2 ] || usage
    need_file "$1"
    awk -F'\t' -v id="$2" "$unescape"'
      NR > 1 && $1 == id { print "answer: " unescape($6); if ($7 != "") print "source: " unescape($7); found = 1 }
      END { if (!found) { print "no card " id > "/dev/stderr"; exit 1 } }' "$1"
    ;;

  grade)
    [ $# -eq 3 ] || usage
    file="$1" id="$2" result="$3"
    need_file "$file"
    box=$(awk -F'\t' -v id="$id" 'NR > 1 && $1 == id { print $3 }' "$file")
    [ -n "$box" ] || { echo "no card $id" >&2; exit 1; }
    case "$result" in
      again) box=1 days=0 ;; # due again today
      hard) days=${intervals[$box]} ;; # stays in its box
      good) box=$((box < max_box ? box + 1 : max_box)) days=${intervals[$box]} ;;
      *) usage ;;
    esac
    due=$(date -d "$today + $days day" +%F)
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

  *) usage ;;
esac
