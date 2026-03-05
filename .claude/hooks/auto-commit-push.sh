#!/bin/bash
# Auto-commit and push all changes in the infinite directory.
# Triggered by the Stop hook — runs every time Claude finishes a session.
set -euo pipefail

cd "$CLAUDE_PROJECT_DIR"

# Check if there's a git repo
if [ ! -d ".git" ]; then
    echo "No git repo found, skipping auto-commit."
    exit 0
fi

# Check if there are any changes to commit
HAS_DIFF=0
git diff --quiet HEAD 2>/dev/null || HAS_DIFF=1
git diff --cached --quiet 2>/dev/null || HAS_DIFF=1
UNTRACKED_FILES=$(git ls-files --others --exclude-standard)
[ -n "$UNTRACKED_FILES" ] && HAS_DIFF=1

if [ "$HAS_DIFF" -eq 0 ]; then
    echo "No changes to commit."
    exit 0
fi

# Count what changed
CHANGED=$(git diff --name-only HEAD 2>/dev/null | wc -l)
UNTRACKED=$(git ls-files --others --exclude-standard | wc -l)
TOTAL=$((CHANGED + UNTRACKED))

# Build a commit message from what changed
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
EXPLORATIONS=$(git diff --name-only HEAD 2>/dev/null | grep '^explorations/' | wc -l || true)
STORIES=$(git diff --name-only HEAD 2>/dev/null | grep '^stories/' | wc -l || true)
COLLECTIONS=$(git diff --name-only HEAD 2>/dev/null | grep '^collections/' | wc -l || true)
NEW_EXPLORATIONS=$(git ls-files --others --exclude-standard | grep '^explorations/' | wc -l || true)
NEW_STORIES=$(git ls-files --others --exclude-standard | grep '^stories/' | wc -l || true)
NEW_COLLECTIONS=$(git ls-files --others --exclude-standard | grep '^collections/' | wc -l || true)

SUMMARY_PARTS=()
E_TOTAL=$((EXPLORATIONS + NEW_EXPLORATIONS))
S_TOTAL=$((STORIES + NEW_STORIES))
C_TOTAL=$((COLLECTIONS + NEW_COLLECTIONS))
[ "$E_TOTAL" -gt 0 ] && SUMMARY_PARTS+=("${E_TOTAL} explorations")
[ "$S_TOTAL" -gt 0 ] && SUMMARY_PARTS+=("${S_TOTAL} stories")
[ "$C_TOTAL" -gt 0 ] && SUMMARY_PARTS+=("${C_TOTAL} collections")

if [ ${#SUMMARY_PARTS[@]} -gt 0 ]; then
    DETAILS=$(IFS=", "; echo "${SUMMARY_PARTS[*]}")
    MSG="Infinite Directory update: ${DETAILS} (${TIMESTAMP})"
else
    MSG="Infinite Directory update: ${TOTAL} files changed (${TIMESTAMP})"
fi

# Stage all changes
git add -A

# Commit
git commit -m "$(cat <<EOF
${MSG}

Auto-committed by Claude session hook.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"

echo "Committed: ${MSG}"

# Push if remote exists
if git remote | grep -q origin; then
    git push origin HEAD 2>&1 && echo "Pushed to origin." || echo "Push failed (no remote configured or auth issue)."
else
    echo "No remote 'origin' configured. Commit is local only."
    echo "To add a remote: git remote add origin <url>"
fi
