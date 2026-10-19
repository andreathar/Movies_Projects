# Release Process

Mechanical steps are implemented in `scripts/changelog.py` (stdlib only, no network, writes
files only when asked). The rules live in `mem:changelog_conventions`. Do not hand-copy the
commit list: run the script, then review its output.

```bash
# categorize commits since the last tag (or an explicit reference) without writing
.venv/bin/python scripts/changelog.py list [--since REF] [--json]

# merge missing entries into the [Unreleased] section (idempotent)
.venv/bin/python scripts/changelog.py write [--since REF]

# move [Unreleased] into a dated version section and refresh compare links
.venv/bin/python scripts/changelog.py release 0.2.0 [--date YYYY-MM-DD]

# structural check (exit 1 with --strict)
.venv/bin/python scripts/changelog.py check [--strict]
```

## 1) Determine the bump

`git describe --tags --abbrev=0` gives the last released tag. From the commits since it:
**major** on any breaking change (`!:` or a `BREAKING CHANGE:` footer), **minor** on any `feat`,
**patch** otherwise. The script applies that mapping to pick the section, not the number: the
number is the agent's (or Andre's) decision and is passed to `release`.

## 2) Update [Unreleased]

Run `write`. Before the first tag exists there is no natural reference, so pass `--since <ref>`
once for the initial seed; afterwards the last tag is used automatically.

Normalisation is by exact bullet text, so `write` is idempotent as long as you do not reword an
entry in place. If you must reword, do it after `release` (the block then leaves `[Unreleased]`)
or stop re-running `write` over the same range.

## 3) Release

Run `release <version>`; it moves the entries, dates the section and rewrites the compare links
from `git remote get-url origin`. It never commits, tags or pushes.

Then, separately and only with the applicable authorization:

```bash
git add CHANGELOG.md && git commit -m "docs: add CHANGELOG.md for v<version> release"
git tag -a v<version> -m "Release v<version>"
```

Creating the tag matters: the next `write` uses the last tag as its range, so releasing without
tagging makes the already released commits look unreleased again.

## 4) Checks before delivering

- `.venv/bin/python scripts/changelog.py check --strict`
- `.venv/bin/python -m unittest discover -s tests -p "test_changelog.py"`

## Boundaries

No commit, tag, push or version claim is implied by generating a changelog. Changelog wording is
a management artefact, not artistic acceptance; a released version describes what shipped, it
does not approve it.
