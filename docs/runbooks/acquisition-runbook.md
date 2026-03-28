# Acquisition Runbook

`UTSP-31`

## Inputs

- `config/repository_selection_criteria.json`
- optional checked-out repositories for raw scraping

## Steps

1. Discover repositories with `discover`.
2. Apply the license gate with `enforce-license-policy`.
3. Apply repository quality scoring with `score-discovery`.
4. Scrape selected repositories with `scrape-repo`.

## Outputs

- discovery manifest
- license-filtered manifest
- quality-scored manifest
- raw source/test pair manifest
