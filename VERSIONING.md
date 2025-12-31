# Automatic Versioning and Release System

This repository uses automated GitHub workflows to manage version bumping and releases.

## Overview

The versioning system follows semantic versioning (MAJOR.MINOR.PATCH) with the following automation:

### 1. Automatic Patch Version Bump (0.0.1) on PR Merge

When a pull request is merged to the `main` or `master` branch:
- The patch version is automatically incremented by 0.0.1 (e.g., 0.2.0 → 0.2.1)
- Changes are committed back to the main branch with message: `chore: bump version to X.X.X [skip ci]`
- A git tag is created (e.g., `v0.2.1`)
- The tag is pushed to the repository

**Workflow:** `.github/workflows/version-bump-pr.yml`

### 2. Manual Release Creation with Minor Version Bump (0.1.0)

To create a new release with a minor version bump:
1. Go to the "Actions" tab in GitHub
2. Select "Create Release with Version Bump" workflow
3. Click "Run workflow"
4. Optionally add release notes
5. Click "Run workflow" button

This will:
- Bump the minor version by 0.1.0 and reset patch to 0 (e.g., 0.2.5 → 0.3.0)
- Commit the version changes
- Create a git tag (e.g., `v0.3.0`)
- Create a GitHub Release with:
  - Automatically generated changelog from commits
  - Optional custom release notes
  - Link to the tag

**Workflow:** `.github/workflows/create-release.yml`

## Version Management Script

The version bumping is handled by `.github/scripts/bump_version.py`, which:
- Reads the current version from `pyproject.toml`
- Updates the version in both `pyproject.toml` and `src/prettipy/__init__.py`
- Supports three bump types: `patch`, `minor`, and `major`

### Manual Version Bump (for testing)

You can manually test the version bump script:

```bash
# Bump patch version (0.0.1)
python .github/scripts/bump_version.py patch

# Bump minor version (0.1.0)
python .github/scripts/bump_version.py minor

# Bump major version (1.0.0)
python .github/scripts/bump_version.py major
```

## Version Locations

The version is maintained in two files:
1. `pyproject.toml`: `version = "X.X.X"`
2. `src/prettipy/__init__.py`: `__version__ = "X.X.X"`

Both files are automatically updated in sync by the version bump script.

## Workflow Permissions

Both workflows require the `contents: write` permission to:
- Commit version changes back to the repository
- Create and push git tags
- Create GitHub releases (for the release workflow)

## Skipping CI

Version bump commits include `[skip ci]` in the commit message to prevent triggering CI workflows unnecessarily, avoiding infinite loops.

## Tags and Releases

- **Tags:** Automatically created for every version bump (format: `vX.X.X`)
- **Releases:** Only created through the manual "Create Release" workflow
- **Changelog:** Automatically generated from git commits between tags
