# CSV Data Cleaner

A small Python application for cleaning and validating CSV files.

## Features
- Read UTF-8 CSV files with headers
- Trim surrounding whitespace
- Validate required columns and values
- Remove duplicates by selected columns (case-sensitive)
- Export cleaned CSV
- CLI and Python API with pytest tests

## Install
```bash
python -m pip install -e '.[dev]'
```

## Usage
```bash
csv-cleaner examples/customers.csv cleaned.csv --required id --dedupe-by id
python -m pytest -q
```

## Python API
```python
from csv_cleaner import clean_rows
rows, duplicates = clean_rows([{'id': ' 1 ', 'name': ' Ada '}], ['id', 'name'], required=['id'])
```

## Future improvements
- Skip invalid rows and optionally write a rejection report
- Normalize selected date columns
- Optional case-insensitive duplicate detection

These improvements are not implemented in the baseline.
