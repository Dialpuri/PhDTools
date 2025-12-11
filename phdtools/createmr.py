import argparse
from phdtools.fetch import fetch_sf, fetch_mmcif
from phdtools.remove_na import remove_na
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Fetch a PDB file from RCSB.")
    parser.add_argument("pdb_id", type=str, help="PDB ID of the structure (e.g., 1abc)")

    args = parser.parse_args()
    
    deposited_path = f"{args.pdb_id}.cif"
    sf_path = f"{args.pdb_id}-sf.cif"
    removed_path = f"{args.pdb_id}-naremoved.cif"
    
    deposited_path = fetch_mmcif(args.pdb_id, deposited_path)
    sf_path = fetch_sf(args.pdb_id, sf_path)
    remove_na(deposited_path, removed_path)
    
    command = f"servalcat refine_xtal_norefmac --model {removed_path} --hklin {sf_path} -s xray"
    subprocess.run(command.split(" "))