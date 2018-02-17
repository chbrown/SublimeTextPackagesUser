#!/usr/bin/env bash

for json in *.sublime-*; do
  >&2 printf 'Pretty-printing JSON file "%s" with jq\n' "$json"
  # Do trial run first and fail immediately,
  # to avoid truncating the file if it can't be parsed
  jq . "$json" >/dev/null && jq . "$json" | sponge "$json"
done
