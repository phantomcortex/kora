#!/bin/bash
# bump-version.sh - Helper script for major/minor version bumps
# Usage: ./bump-version.sh [major|minor|patch]

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 [major|minor|patch]"
    echo ""
    echo "Creates a git tag for a version bump:"
    echo "  major - Bumps major version (1.0.0 -> 2.0.0)"
    echo "  minor - Bumps minor version (1.0.0 -> 1.1.0)"
    echo "  patch - Bumps patch version (1.0.0 -> 1.0.1)"
    echo ""
    echo "Note: Build number will reset to 1 for any manual version bump"
    exit 1
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Get bump type
BUMP_TYPE=${1:-patch}

# Validate bump type
if [[ ! "$BUMP_TYPE" =~ ^(major|minor|patch)$ ]]; then
    echo -e "${RED}Error: Invalid bump type '$BUMP_TYPE'${NC}"
    usage
fi

# Get the latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v1.6.5.0")

# Parse current version
if [[ $LATEST_TAG =~ v([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
    MAJOR=${BASH_REMATCH[1]}
    MINOR=${BASH_REMATCH[2]}
    PATCH=${BASH_REMATCH[3]}
    BUILD=${BASH_REMATCH[4]}
else
    echo -e "${YELLOW}Warning: Could not parse version from tag '$LATEST_TAG'${NC}"
    echo "Using default: 1.6.5.1"
    MAJOR=1
    MINOR=6
    PATCH=5
    BUILD=1
fi

# Calculate new version based on bump type
case $BUMP_TYPE in
    major)
        NEW_MAJOR=$((MAJOR + 1))
        NEW_MINOR=0
        NEW_PATCH=0
        NEW_BUILD=1
        ;;
    minor)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$((MINOR + 1))
        NEW_PATCH=0
        NEW_BUILD=1
        ;;
    patch)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$MINOR
        NEW_PATCH=$((PATCH + 1))
        NEW_BUILD=1
        ;;
esac

NEW_VERSION="${NEW_MAJOR}.${NEW_MINOR}.${NEW_PATCH}.${NEW_BUILD}"
NEW_TAG="v${NEW_VERSION}"

echo -e "${GREEN}Current version:${NC} ${LATEST_TAG#v}"
echo -e "${GREEN}New version:${NC}     ${NEW_VERSION}"
echo ""

# Confirm with user
read -p "Create tag ${NEW_TAG} and push? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Create annotated tag
echo -e "${YELLOW}Creating tag ${NEW_TAG}...${NC}"
git tag -a "$NEW_TAG" -m "Version bump: ${BUMP_TYPE} release ${NEW_VERSION}"

# Push tag to remote
echo -e "${YELLOW}Pushing tag to remote...${NC}"
git push origin "$NEW_TAG"

echo -e "${GREEN}✓ Successfully created and pushed tag ${NEW_TAG}${NC}"
echo ""
echo "The GitHub workflow will automatically:"
echo "  1. Build the RPM with version ${NEW_VERSION}"
echo "  2. Create a release with the RPM attached"
echo "  3. Future commits will auto-increment from ${NEW_VERSION}"
