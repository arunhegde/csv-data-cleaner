# Feature request: Optional case-insensitive duplicate detection

## User need
Exports sometimes contain repeated email addresses with different capitalization. The existing deduplication is case-sensitive.

## Proposed behavior
Add `--dedupe-ignore-case` as an opt-in option. When used with `--dedupe-by`, compare the specified fields using Unicode `casefold()` while preserving the original cleaned output values. Without the flag, keep current case-sensitive behavior.

## Acceptance criteria
1. `Ada@Example.com` and `ada@example.com` count as duplicates with the new flag.
2. The first row's cleaned original value is preserved.
3. Multiple dedupe columns work.
4. Without the flag, capitalization differences remain distinct.
5. The flag without `--dedupe-by` produces a clear usage error or is explicitly documented as a no-op; decide before implementation.

## Suggested tests
Case variants; non-ASCII casefold; two-column key; first-row preservation; default regression; empty values.

## Scope
Estimated 10–25 production lines.
