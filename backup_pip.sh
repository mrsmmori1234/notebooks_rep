#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "========================================="
echo "🔄 Starting Bulk Pip Packages Upgrade..."
echo "========================================="

# 1. Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: 'pip' command not found. Are you sure the virtualenv is activated?"
    exit 1
fi

# 2. Fetch outdated packages
echo "🔍 Scanning for outdated packages..."
OUTDATED_PACKAGES=$(pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1)

if [ -z "$OUTDATED_PACKAGES" ]; then
    echo "✅ All packages are already up-to-date!"
    echo "========================================="
    exit 0
fi

# 3. Count packages to update
COUNT=$(echo "$OUTDATED_PACKAGES" | wc -l)
echo "📦 Found $COUNT packages to upgrade."
echo "-----------------------------------------"

# 4. Execute sequential upgrade via xargs
echo "$OUTDATED_PACKAGES" | xargs -n1 pip install -U

echo "-----------------------------------------"
echo "🎉 Bulk upgrade completed successfully!"
echo "========================================="