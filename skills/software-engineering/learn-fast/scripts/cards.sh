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
#
# Reviews: each grade adds a line to .review-log next to the cards (date, topic,
# id, level, result, box), so `history` can show whether reviews happen and
# what they retain. The cards themselves keep only the current box and date.
set -euo pipefail

intervals=(0 1 3 7 16 35 75) # card days, indexed by box 1..6
max_box=6
[ -z "${NOTEBOOK_TZ:-}" ] || export TZ="$NOTEBOOK_TZ"
today=$(date +%F)
header=$'id\tlevel\tbox\tdue\tquestion\tanswer\tsource'

usage() {
  cat >&2 <<'EOF'
usage: A <cards> argument is a cards folder or any number of .tsv files.
       cards.sh add <cards.tsv> <level 1-4> <question> <answer> [source]
       cards.sh due <cards>...                cards due today or earlier, oldest first, topics mixed (no answers)
       cards.sh ask <cards.tsv> <id>          the full question of one card
       cards.sh show <cards.tsv> <id>         the answer and source of one card
       cards.sh grade <cards.tsv> <id> again|hard|good
       cards.sh stats <cards>...              total, due and per-box counts
       cards.sh history <cards-folder> [days] reviews and results per topic (default 30 days)
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

# card_files <cards>...: the .tsv files in the given folders and files. Taking a
# folder keeps callers off globs, which zsh refuses when nothing matches.
card_files() {
  local arg
  for arg in "$@"; do
    if [ -d "$arg" ]; then
      find "$arg" -maxdepth 1 -name '*.tsv' | sort
    elif [ -f "$arg" ]; then
      printf '%s\n' "$arg"
    fi
  done
}

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
    # Each topic's cards oldest first, then one from each topic in turn, so a
    # review that stops early doesn't starve the topics that sort last.
    card_files "$@" | while IFS= read -r file; do
      awk -F'\t' -v OFS='\t' -v today="$today" -v topic="$(topic_of "$file")" \
        'NR > 1 && $4 <= today { print $4, topic, $1, "level " $2, $5 }' "$file" |
        sort -s -t $'\t' -k1,1 |
        awk -F'\t' -v OFS='\t' '{ print NR, $2, $3, $4, $5 }'
    done | sort -s -n -k1,1 | cut -f2-
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
    level=$(awk -F'\t' -v id="$id" 'NR > 1 && $1 == id { print $2 }' "$file")
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$today" "$(topic_of "$file")" "$id" "$level" "$result" "$box" \
      >>"$(dirname "$file")/.review-log"
    echo "card $id: box $box, due $due"
    ;;

  stats)
    [ $# -ge 1 ] || usage
    card_files "$@" | while IFS= read -r file; do
      awk -F'\t' -v today="$today" -v topic="$(topic_of "$file")" '
        NR > 1 { total++; boxes[$3]++; if ($4 <= today) due++ }
        END {
          line = sprintf("%s: %d cards, %d due", topic, total, due)
          for (b = 1; b <= 6; b++) line = line sprintf(", box%d=%d", b, boxes[b] + 0)
          print line
        }' "$file"
    done
    ;;

  history)
    [ $# -ge 1 ] || usage
    log="$1/.review-log" days="${2:-30}"
    [ -f "$log" ] || { echo "no reviews yet"; exit 0; }
    since=$(date -d "$today - $days day" +%F)
    awk -F'\t' -v since="$since" -v days="$days" '
      $1 >= since {
        reviews[$2]++; results[$2, $5]++; total++; all[$5]++
        if (!($1 in active)) { active[$1] = 1; active_days++ }
      }
      END {
        printf "last %d days: %d reviews on %d days, good=%d hard=%d again=%d\n",
          days, total, active_days, all["good"], all["hard"], all["again"]
        for (t in reviews)
          printf "%s: %d reviews, good=%d hard=%d again=%d\n",
            t, reviews[t], results[t, "good"], results[t, "hard"], results[t, "again"]
      }' "$log"
    ;;

  *) usage ;;
esac
