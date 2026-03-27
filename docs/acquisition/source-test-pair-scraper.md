# Source/Test Pair Scraper

`UTSP-13`

This document describes the raw repository scraper that converts a checked-out
repository snapshot into source/test pair records.

## Goal

Extract likely `TypeScript` source modules and their matching `Jest` test files
while preserving file paths and repository provenance.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli scrape-repo \
  --repo-root path/to/repository \
  --repository-name owner/repo \
  --repository-url https://github.com/owner/repo \
  --revision <commit-sha> \
  --output data/raw/source_test_pairs.json
```

## Pairing Logic

The current implementation:

- scans the repository for `.ts` and `.tsx` source files
- excludes obvious test files and declaration files from source candidates
- scans separately for `*.test.ts`, `*.spec.ts`, `*.test.tsx`, and `*.spec.tsx`
- ranks test candidates by basename match and path locality
- stores up to three likely test paths per source module

## Raw Manifest Shape

The raw output manifest preserves:

- repository name
- repository URL
- repository revision
- source file path
- matched test file paths

That keeps downstream curation traceable back to a specific repository snapshot.

## Acceptance Mapping

This ticket is done when:

- source modules can be paired with likely Jest test files
- file paths and repository provenance are preserved
- raw extracted examples are stored in a documented manifest format
