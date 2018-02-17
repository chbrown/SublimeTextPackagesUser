#!/usr/bin/env bash

for json in *.sublime-*; do
  >&2 printf 'Pretty-printing JSON file "%s" with jq\n' "$json"
  # Do trial run first and fail immediately,
  # to avoid truncating the file if it can't be parsed
  jq . "$json" >/dev/null && jq . "$json" | sponge "$json"
done

wordlist=~/Library/Spelling/LocalDictionary
if [[ -e $wordlist ]]; then
  prefs=Preferences.sublime-settings
  >&2 printf 'Reading wordlist at "%s" (the macOS local dictionary) and merging with "added_words" in "%s"\n' "$wordlist" "$prefs"
  jq . "$prefs" >/dev/null && \
    jq --slurpfile words <(jq -R . "$wordlist") '.added_words = (.added_words + $words | unique)' "$prefs" | \
    sponge "$prefs"
fi
