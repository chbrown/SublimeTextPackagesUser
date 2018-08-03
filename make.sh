#!/usr/bin/env bash

for JSON_PATH in *.sublime-*; do
  >&2 printf 'Pretty-printing JSON file "%s" with jq\n' "$JSON_PATH"
  # Do trial run first and fail immediately,
  # to avoid truncating the file if it can't be parsed
  if jq . "$JSON_PATH" >/dev/null; then
    jq . "$JSON_PATH" | sponge "$JSON_PATH"
  fi
done

WORDLIST_PATH=~/Library/Spelling/LocalDictionary
if [[ -e $WORDLIST_PATH ]]; then
  PREFS_JSON_PATH=Preferences.sublime-settings
  >&2 printf 'Reading wordlist at "%s" (the macOS local dictionary) and merging with "added_words" in "%s"\n' $WORDLIST_PATH $PREFS_JSON_PATH
  # validate JSON first
  if jq . $PREFS_JSON_PATH >/dev/null; then
    # jq's 'unique' function always returns a sorted array
    jq --slurpfile words <(jq -R . $WORDLIST_PATH) '.added_words = (.added_words + $words | unique)' $PREFS_JSON_PATH | \
      sponge $PREFS_JSON_PATH
  fi
fi
