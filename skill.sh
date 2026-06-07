#!/usr/bin/env bash

# Local skill registry
# Compatible with bash 3.2+ (macOS default)

SKILL_web_search="skills/web-search/SKILL.md"

if [[ $# -eq 0 ]]; then
  echo "Usage: source ./skill.sh <skill-name>"
  echo "Available skills: web-search"
else
  case "$1" in
    web-search)
      echo "$SKILL_web_search"
      ;;
    *)
      echo "Unknown skill: $1"
      echo "Available: web-search"
      exit 1
      ;;
  esac
fi
