# Kora Icon Theme - Versioning System

## Overview

This repository uses an automated versioning system that follows the format: `MAJOR.MINOR.PATCH.BUILD`

- **MAJOR**: Significant changes, breaking compatibility
- **MINOR**: New features, significant additions
- **PATCH**: Bug fixes, minor improvements
- **BUILD**: Auto-incremented for every commit to main

## How It Works

### Automatic Version Bumping

Every push to the `main` or `master` branch automatically:
1. Increments the BUILD number
2. Creates a new RPM package
3. Creates a GitHub release with the RPM attached
4. Tags the commit with the new version

**Example flow:**
```
v1.6.5.14 (current) → push commit → v1.6.5.15 (automatic)
v1.6.5.15 → push commit → v1.6.5.16 (automatic)
... continues infinitely
```

### Manual Version Bumps

For significant changes, you can manually bump major, minor, or patch versions:

#### Option 1: Using the Helper Script
```bash
# Major version bump (1.6.5.x → 2.0.0.1)
./bump-version.sh major

# Minor version bump (1.6.5.x → 1.7.0.1)
./bump-version.sh minor

# Patch version bump (1.6.5.x → 1.6.6.1)
./bump-version.sh patch
```

#### Option 2: Manual Git Tag
```bash
# Create a new version tag
git tag -a v1.7.0.1 -m "Minor version bump: Added new icon set"
git push origin v1.7.0.1
```

**Note:** Manual version bumps reset the BUILD number to 1.

## Installation from Releases

Each release includes a pre-built RPM package (binary only, no source RPMs). 

### Quick Installation (Latest Version)

```bash
# Direct installation with dnf5 - one command!
sudo dnf5 -y install $(curl -s https://api.github.com/repos/phantomcortex/kora/releases/latest | grep "browser_download_url.*\.rpm" | cut -d '"' -f 4)
```

### Alternative Installation Methods

```bash
# Download first, then install
curl -LO $(curl -s https://api.github.com/repos/phantomcortex/kora/releases/latest | grep "browser_download_url.*\.rpm" | cut -d '"' -f 4)
sudo dnf5 -y install ./kora-icon-theme-*.rpm

# Install specific version
VERSION=1.6.5.15
sudo dnf5 -y install https://github.com/phantomcortex/kora/releases/download/v${VERSION}/kora-icon-theme-${VERSION}-1.fc42.noarch.rpm
```

## Workflow Configuration

The GitHub Actions workflow (`.github/workflows/build-rpm.yml`) handles:
- Automatic version detection and incrementing
- RPM package building
- Release creation and asset uploads
- Version persistence across builds

## Version Persistence

The system tracks versions through GitHub releases:
- Each commit queries the latest release to get the last BUILD number
- The BUILD number is incremented and used for the new release
- This ensures continuous, sequential versioning

## Troubleshooting

### Version Not Incrementing
- Ensure the workflow has permission to create releases
- Check that `GITHUB_TOKEN` is available in the workflow
- Verify the repository has at least one release (or the system starts at 1.6.5.1)

### Manual Override
If you need to set a specific version, create a tag:
```bash
git tag -a v1.6.5.252 -m "Setting specific version"
git push origin v1.6.5.252
```

## Benefits

1. **Zero Maintenance**: No need to edit files for version bumps
2. **Continuous Delivery**: Every commit creates a installable release
3. **Version History**: All versions are tracked in GitHub releases
4. **Flexible**: Supports both automatic and manual version management
5. **RPM Integration**: Version automatically flows into RPM metadata

## Files Involved

- `.github/workflows/build-rpm.yml` - Main workflow with versioning logic
- `kora-icon-theme.spec` - RPM spec with `__VERSION__` placeholder
- `bump-version.sh` - Optional helper for manual version bumps
- GitHub Releases - Version persistence storage
