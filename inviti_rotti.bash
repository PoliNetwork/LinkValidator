#!/bin/env bash

< <(rg -n 'https?://t.me/(joinchat/)?[A-Za-z0-9_-]+') mapfile -t matches

regex_parse_match='([^:]+:[0-9]+):.*"?(https?://t.me/(joinchat/)?[A-Za-z0-9_-]+)'
regex_bad_invite=$'(^|\n)[[:space:]]*<meta property="og:title" content="Join group chat on Telegram"'

(( ${#matches[@]} >= 1 )) \
    || exit

printf 'Checking %d URL%c...\n' "${#matches[@]}" "${matches[1]+s}"

declare -A already_checked

es=0
for match in "${matches[@]}"; do
    [[ $match =~ $regex_parse_match ]] \
        || continue
    file_and_linenumber=${BASH_REMATCH[1]} url=${BASH_REMATCH[2]}

    case ${already_checked[$url]} in
        1) echo "$file_and_linenumber: $url" ;&
        2) continue ;;
    esac

    page=$(curl -sS "$url") || {
        echo "WARN: questo URL è malformato: _${url}_"
        es=1
        continue
    }

    if [[ $page =~ $regex_bad_invite ]]; then
        echo "$file_and_linenumber: $url"
        already_checked[$url]=1 es=1
    else
        already_checked[$url]=2
    fi

    sleep "${1:-0.1}" 2> /dev/null || {
        echo "$0: ERROR: _${1}_ non è un tempo valido." >&2
        exit 2
    }
done

exit "$es"
