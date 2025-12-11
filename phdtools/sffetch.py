import argparse
from phdtools.fetch import fetch_sf


def main():
    parser = argparse.ArgumentParser(description="Fetch a SF file from RCSB.")
    parser.add_argument("pdb_id", type=str, help="PDB ID of the structure (e.g., 1abc)")
    parser.add_argument("-o", "--output", type=str, help="Output filename (optional)")

    args = parser.parse_args()

    try:
        saved_path = fetch_sf(args.pdb_id, args.output)
        print(f"SF file saved to: {saved_path}")
    except Exception as e:
        print(f"Error: {e}")
