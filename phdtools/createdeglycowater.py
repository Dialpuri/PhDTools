import argparse
from phdtools.fetch import fetch_sf, fetch_mmcif
from phdtools.remove_glycans import remove_glycans
from phdtools.remove_waters import remove_waters
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Fetch a PDB file from RCSB.")
    parser.add_argument("pdb_id", type=str, help="PDB ID of the structure (e.g., 1abc)")

    args = parser.parse_args()
    
    deposited_path = f"{args.pdb_id}.cif"
    sf_path = f"{args.pdb_id}-sf.cif"
    glycan_removed_path = f"{args.pdb_id}-glycan_removed.cif"
    water_removed_path = f"{args.pdb_id}-glycan_water_removed.cif"

    deposited_path = fetch_mmcif(args.pdb_id, deposited_path)
    sf_path = fetch_sf(args.pdb_id, sf_path)
    remove_glycans(deposited_path, glycan_removed_path)
    remove_waters(glycan_removed_path, water_removed_path)

    command = f"servalcat refine_xtal_norefmac --model {water_removed_path} --hklin {sf_path} -s xray"
    subprocess.run(command.split(" "))