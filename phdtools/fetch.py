import requests


def fetch_pdb(pdb_id: str, out_path: str = None) -> str:
    pdb_id = pdb_id.lower()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch PDB file: {pdb_id}")

    if out_path is None:
        out_path = f"{pdb_id}.pdb"

    with open(out_path, "w") as f:
        f.write(response.text)

    return out_path

def fetch_mmcif(pdb_id: str, out_path: str = None) -> str:
    pdb_id = pdb_id.lower()
    url = f"https://files.rcsb.org/download/{pdb_id}.cif"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch PDB file: {pdb_id}")

    if out_path is None:
        out_path = f"{pdb_id}.cif"

    with open(out_path, "w") as f:
        f.write(response.text)

    return out_path


def fetch_sf(pdb_id: str, out_path: str = None) -> str:
    pdb_id = pdb_id.lower()
    url = f"https://files.rcsb.org/download/{pdb_id}-sf.cif"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch PDB file: {pdb_id}")

    if out_path is None:
        out_path = f"{pdb_id}.cif"

    with open(out_path, "w") as f:
        f.write(response.text)

    return out_path
