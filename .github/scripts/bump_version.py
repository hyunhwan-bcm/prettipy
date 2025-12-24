#!/usr/bin/env python3
"""
Script to bump version in pyproject.toml and __init__.py
"""
import re
import sys
from pathlib import Path


def get_current_version(file_path):
    """Get current version from file"""
    content = Path(file_path).read_text()
    if "pyproject.toml" in str(file_path):
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
    else:  # __init__.py
        match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
    
    if match:
        return match.group(1)
    raise ValueError(f"Version not found in {file_path}")


def bump_version(version, bump_type):
    """Bump version based on type (patch or minor)"""
    major, minor, patch = map(int, version.split('.'))
    
    if bump_type == 'patch':
        patch += 1
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return f"{major}.{minor}.{patch}"


def update_version_in_file(file_path, old_version, new_version):
    """Update version in file"""
    content = Path(file_path).read_text()
    
    if "pyproject.toml" in str(file_path):
        pattern = r'(version\s*=\s*")' + re.escape(old_version) + r'"'
        replacement = r'\g<1>' + new_version + '"'
    else:  # __init__.py
        pattern = r'(__version__\s*=\s*")' + re.escape(old_version) + r'"'
        replacement = r'\g<1>' + new_version + '"'
    
    new_content = re.sub(pattern, replacement, content)
    Path(file_path).write_text(new_content)


def main():
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <patch|minor|major>")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    if bump_type not in ['patch', 'minor', 'major']:
        print("Error: bump_type must be 'patch', 'minor', or 'major'")
        sys.exit(1)
    
    # File paths
    repo_root = Path(__file__).resolve().parents[2]
    pyproject_path = repo_root / "pyproject.toml"
    init_path = repo_root / "src" / "prettipy" / "__init__.py"
    
    # Get current version
    current_version = get_current_version(pyproject_path)
    print(f"Current version: {current_version}")
    
    # Bump version
    new_version = bump_version(current_version, bump_type)
    print(f"New version: {new_version}")
    
    # Update files
    update_version_in_file(pyproject_path, current_version, new_version)
    update_version_in_file(init_path, current_version, new_version)
    
    # Output new version for GitHub Actions (using GITHUB_OUTPUT env var)
    print(f"NEW_VERSION={new_version}")


if __name__ == "__main__":
    main()
