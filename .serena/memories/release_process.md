# Release Process

Follow this process when preparing and releasing a new version.

## 1) Determine Version Bump

From commits since last tag (`git describe --tags --abbrev=0`), determine SemVer bump:
- **major**: any commit with `BREAKING CHANGE` or `!:` in message
- **minor**: any `feat:` commit
- **patch**: only `fix:` (and other non-breaking changes)

Get last tag: `git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"`
Get commits since: `git log <LAST_TAG>..HEAD --no-merges --format="%H %s"`

## 2) Gather Changes

Collect and categorize commits:
```bash
git log <LAST_TAG>..HEAD --no-merges --format="%h %s"
```

For each significant commit:
- Read full message: `git log -1 --format="%B" <commit>`
- Extract PR number if present (`(#NNN)`)
- Categorize by conventional commit prefix per changelog_conventions.md
- Skip: `chore`, `docs`, `test`, `ci`, `style`, `build` unless they contain breaking changes

## 3) Update CHANGELOG.md

1. If `CHANGELOG.md` doesn't exist, create it with full header per changelog_conventions.md
2. Add new version section under header and before any existing version sections:
   ```markdown
   ## [<VERSION>] - <YYYY-MM-DD>
   ```
   (VERSION has no `v` prefix in heading; tags will have `v` prefix)
3. Add categorized entries (only include sections with entries)
4. Update compare links at bottom:
   ```markdown
   [Unreleased]: https://github.com/andreathar/Movies_Projects/compare/v<NEW>...HEAD
   [<VERSION>]: https://github.com/andreathar/Movies_Projects/compare/v<OLD>...v<NEW>
   ```

Date: `date +%Y-%m-%d`

## 4) Verify & Commit

1. Review entries for accuracy and completeness
2. Stage and commit:
   ```bash
   git add CHANGELOG.md
   git commit -m "docs: add CHANGELOG.md for v<NEW> release"
   ```
3. Create tag and push (or open PR):
   ```bash
   git tag -a v<NEW> -m "Release v<NEW>"
   git push origin main --tags
   ```

## 5) Automation Notes

- Prefer `scripts/bump_version.py` if it exists (Serena's pattern). Run with appropriate bump level.
- If script doesn't exist, follow manual steps above.
- After release, ensure [Unreleased] section remains at top (empty or with future items).

## 6) Validation

Before committing:
- Entries follow Keep a Changelog format
- No empty sections
- Version numbers correct (no `v` in [heading] but `v` in tag/compare URLs)
- Links are properly formatted
- Changes are user-focused