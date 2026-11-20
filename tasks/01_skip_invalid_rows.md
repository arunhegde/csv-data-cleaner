# Feature request: Skip invalid rows and report rejections

## User need
When importing customer exports, a single missing required value currently prevents all rows from being cleaned. Users sometimes need the valid records while retaining an auditable list of rejected records.

## Proposed behavior
Add an opt-in `--skip-invalid-rows` flag and optional `--rejects PATH` output. With the flag, rows failing required-value validation or CSV row-shape validation are skipped; valid rows continue through trimming and deduplication. The rejection report should contain original row number and a short reason. Preserve the current fail-fast behavior by default.

## Acceptance criteria
1. Default behavior is unchanged: invalid data causes an error and no cleaned output is created.
2. With `--skip-invalid-rows`, valid rows are written and invalid rows are excluded.
3. A rejection report, if requested, includes row number and reason.
4. Invalid records do not affect duplicate tracking.
5. Zero valid rows still produce a header-only output.
6. Reject report paths cannot overwrite the input or cleaned output.
7. CLI displays processed, rejected, and duplicate counts.

## Suggested tests
Mixed valid/invalid rows; all invalid rows; malformed extra columns; blank required field; duplicates around invalid rows; report path conflicts; no reject report; default mode regression.

## Implementation notes
Aim for a small, backward-compatible change. Estimate 30–60 production lines, subject to design and tests. Avoid using this task unless it is a real feature you intend to maintain and your task rules permit your own repository.
