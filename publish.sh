#!/bin/sh
# publish to github.com/pennyops/agent-boards (Pages). Token read from secrets, never stored in repo.
set -e
cd "$(dirname "$0")"
T=$(cat /workspace/secrets/github_token.txt | tr -d '\n')
python3 -I build.py .
[ -d .git ] || { git init -q -b main; git config user.name Penny; git config user.email pennyops@users.noreply.github.com; }
git add .nojekyll index.html status.json venues.json build.py README.md publish.sh 2>/dev/null || git add index.html status.json venues.json build.py
git commit -q -m "update $(date -u +%F)" || true
git push -q "https://pennyops:${T}@github.com/pennyops/agent-boards.git" main 2>&1 | sed "s/${T}/***/g"
