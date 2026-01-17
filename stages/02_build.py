#!/usr/bin/env python3
"""
Process Guide to PHARMACOLOGY TSV files into Parquet format.
"""

from pathlib import Path
import pandas as pd

def load_tsv(path: Path) -> pd.DataFrame:
    """Load a TSV file with proper encoding handling."""
    # Read first line to check if it's a comment
    with open(path, 'r', encoding='utf-8') as f:
        first_line = f.readline()

    # Skip first line if it contains version info
    skiprows = 1 if '# GtoPdb Version' in first_line else 0

    try:
        return pd.read_csv(path, sep='\t', encoding='utf-8', low_memory=False,
                          skiprows=skiprows)
    except UnicodeDecodeError:
        return pd.read_csv(path, sep='\t', encoding='latin-1', low_memory=False,
                          skiprows=skiprows)

def main():
    download_path = Path("download")
    brick_path = Path("brick")
    brick_path.mkdir(exist_ok=True)

    # Process each TSV file
    files_processed = 0
    total_records = 0

    for tsv_file in sorted(download_path.glob("*.tsv")):
        print(f"Processing {tsv_file.name}...")
        try:
            df = load_tsv(tsv_file)

            # Standardize column names - lowercase with underscores
            df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]

            # Convert object columns to string for parquet compatibility
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str)

            # Save as parquet
            output_name = tsv_file.stem + ".parquet"
            output_path = brick_path / output_name
            df.to_parquet(output_path, index=False)

            print(f"  -> {output_name}: {len(df):,} records, {len(df.columns)} columns")
            files_processed += 1
            total_records += len(df)

        except Exception as e:
            print(f"  Error processing {tsv_file.name}: {e}")

    print(f"\nProcessed {files_processed} files with {total_records:,} total records")

if __name__ == "__main__":
    main()
