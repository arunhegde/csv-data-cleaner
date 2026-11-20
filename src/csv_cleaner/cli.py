"""Command line entry point."""
import argparse
import sys
from .cleaner import clean_file, CleaningError


def main(argv=None):
    parser = argparse.ArgumentParser(description="Clean and validate a CSV file")
    parser.add_argument("input", help="Source CSV path")
    parser.add_argument("output", help="Destination CSV path")
    parser.add_argument("--required", action="append", default=[], metavar="COLUMN")
    parser.add_argument("--dedupe-by", action="append", default=[], metavar="COLUMN")
    args = parser.parse_args(argv)
    try:
        count, duplicates = clean_file(
            args.input, args.output, args.required, args.dedupe_by
        )
    except (CleaningError, OSError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {count} rows; removed {duplicates} duplicates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
