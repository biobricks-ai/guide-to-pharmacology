#!/usr/bin/env python3
"""
Download Guide to PHARMACOLOGY (GtoPdb) data.
Source: https://www.guidetopharmacology.org/
License: CC BY-SA 4.0
Version: 2026.2
"""

from pathlib import Path
import requests

BASE_URL = "https://www.guidetopharmacology.org/DATA"

# Key files to download
FILES = [
    "targets_and_families.tsv",
    "ligands.tsv",
    "ligand_id_mapping.tsv",
    "interactions.tsv",
    "approved_drug_detailed_interactions.tsv",
    "approved_drug_primary_target_interactions.tsv",
    "peptides.tsv",
    "ligand_physchem_properties.tsv",
    "endogenous_ligand_pairings_all.tsv",
    "GtP_to_UniProt_mapping.tsv",
    "GtP_to_HGNC_mapping.tsv",
]

def download_file(url: str, dest: Path) -> bool:
    """Download a file from URL to destination."""
    print(f"Downloading {url}...")
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        print(f"  Saved to {dest} ({len(resp.content):,} bytes)")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    download_path = Path("download")
    download_path.mkdir(exist_ok=True)

    success_count = 0
    for filename in FILES:
        url = f"{BASE_URL}/{filename}"
        dest = download_path / filename
        if download_file(url, dest):
            success_count += 1

    print(f"\nDownloaded {success_count}/{len(FILES)} files")

if __name__ == "__main__":
    main()
