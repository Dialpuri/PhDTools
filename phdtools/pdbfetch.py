import argparse
from phdtools.fetch import fetch_pdb, fetch_mmcif


def main():
    parser = argparse.ArgumentParser(description="Fetch a PDB file from RCSB.")
    parser.add_argument("pdb_id", type=str, help="PDB ID of the structure (e.g., 1abc)")
    parser.add_argument("-o", "--output", type=str, help="Output filename (optional)")
    parser.add_argument("-t", "--type", type=str, help="File Type (CIF or PDB), default CIF", default='cif', choices=['cif', 'pdb'])

    args = parser.parse_args()

    try:
        if args.type == "cif":
            saved_path = fetch_mmcif(args.pdb_id, args.output)
        elif args.type == "pdb":
            saved_path = fetch_pdb(args.pdb_id, args.output)
        else:
            raise RuntimeError(f"Unknown type: {args.type}")
        print(f"PDB file saved to: {saved_path}")
    except Exception as e:
        print(f"Error: {e}")
