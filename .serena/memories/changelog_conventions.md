# Changelog Conventions

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## CHANGELOG.md Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

## [Unreleased]

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```

## Version Links (when releasing)
At the bottom, add version comparison links:
```markdown
[Unreleased]: https://github.com/andreathar/Movies_Projects/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/andreathar/Movies_Projects/compare/v0.9.0...v1.0.0
```

## Rules for Entries

1. **Date format**: `YYYY-MM-DD` for released versions (not for Unreleased)
2. **Categorize correctly**:
- `feat:` commits → **Added**
- `fix:` commits → **Fixed** 
- `security`/`sec:` → **Security**
- `refactor:` with behavior change or `perf:` → **Changed**
- `BREAKING CHANGE` or `!:` in commit → often **Changed** or **Removed**; note breaking changes clearly
- `deprecate:` → **Deprecated**
- `remove:` → **Removed**

3. **Skip these** (unless explicitly requested or breaking): `chore:`, `docs:`, `test:`, `ci:`, `style:`, `build:` that don't affect behavior
4. **Write user-focused descriptions**: Focus on what the user gains, not implementation details. Link PR numbers when available (e.g., `(#123)`).
5. **One change per line**: Be concise but clear.
6. **Keep entries in [Unreleased]** during development; only move to version section on release.
7. **Don't invent version numbers** - derive from git tags and SemVer rules.
8. **If no entries for a section**, omit the section entirely (don't create empty sections).