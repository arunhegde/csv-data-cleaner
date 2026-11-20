"""Small, dependency-free CSV cleaning pipeline."""
import csv
from pathlib import Path


class CleaningError(ValueError):
    """Input data cannot be cleaned under the requested constraints."""


def clean_rows(rows, fieldnames, required=(), dedupe_by=()):
    """Return (cleaned_rows, duplicates_removed).

    Baseline policy: reject the entire operation if any required value is missing.
    """
    if not fieldnames:
        raise CleaningError("CSV must have a header")
    unknown = (set(required) | set(dedupe_by)) - set(fieldnames)
    if unknown:
        raise CleaningError(f"Unknown columns: {', '.join(sorted(unknown))}")

    cleaned = []
    seen = set()
    duplicates = 0
    for line_number, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            raise CleaningError(f"Malformed CSV row at line {line_number}")
        normalized = {name: value.strip() for name, value in row.items()}
        missing = [name for name in required if not normalized[name]]
        if missing:
            raise CleaningError(
                f"Missing required value at line {line_number}: {', '.join(missing)}"
            )
        if dedupe_by:
            key = tuple(normalized[name] for name in dedupe_by)
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
        cleaned.append(normalized)
    return cleaned, duplicates


def clean_file(input_path, output_path, required=(), dedupe_by=()):
    """Clean input CSV and write output only after successful validation."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    if input_path.resolve() == output_path.resolve():
        raise CleaningError("Input and output paths must differ")
    with input_path.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fieldnames = reader.fieldnames
        rows, duplicates = clean_rows(reader, fieldnames, required, dedupe_by)
    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows), duplicates
