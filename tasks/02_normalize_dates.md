# Feature request: Normalize specified date columns

## User need
CSV exports use multiple common date formats. Users need consistent ISO dates before importing into other systems.

## Proposed behavior
Add repeatable `--date-column COLUMN` and optional `--input-date-format FORMAT` flags. For named columns, parse nonblank values using an explicitly supplied format and output ISO `YYYY-MM-DD`. Preserve blank values. Fail with a clear row/column error for invalid dates. Keep date columns untouched when not requested.

## Acceptance criteria
1. `--date-column joined --input-date-format %d/%m/%Y` converts `14/02/2026` to `2026-02-14`.
2. Empty values remain empty.
3. Bad date values report row and column and prevent output creation.
4. Unknown date columns are rejected.
5. Multiple date columns work.
6. Existing cleanup without date flags is unchanged.

## Suggested tests
Leap day; invalid date; empty date; two date columns; format mismatch; no flag; unknown column.

## Scope
Estimated 20–45 production lines. Prefer Python's `datetime.strptime` rather than adding dependencies.
