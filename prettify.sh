#!/usr/bin/env bash
for arg in "$@"; do
  printf "Prettifying %s\n" "$arg"
  jq . "$arg" > "$arg.tmp" && mv "$arg.tmp" "$arg" || rm "$arg.tmp"
  printf "Prettified %s\n" "$arg"
done
