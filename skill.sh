#!/usr/bin/env bash

# Local skill registry
declare -A SKILLS=(
  [web-search]="skills/web-search/SKILL.md"
)

if [[ $# -eq 0 ]]; then
  echo "Usage: source ./skill.sh <skill-name>"
  echo "Available skills: ${!SKILLS[@]}"
else
  echo "${SKILLS[$1]}"
fi
