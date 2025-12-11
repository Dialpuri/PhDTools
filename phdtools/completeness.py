#!/usr/bin/env python3

"""
Assess the completeness of a structure by comparing it to a reference structure.
Assumes that csymmatch has been used first to account for any origin shifts.
Outputs a JSON file with total, built and sequenced protein and nucleic acid residues.
Protein completeness is assessed using N, CA and C.
Nucleic completeness is assessed using C1', C2', C3', C4' and O4'.
For a reference residue to be classed as built,
all the atoms must be within a 1A radius of the same atom in the built structure.
For the residue to be classed as sequenced it must also be the same type.
"""

import argparse
import functools
import json
from dataclasses import dataclass
import dataclasses
from typing import Dict
import gemmi
import numpy as np


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("structure")
    parser.add_argument("reference")
    parser.add_argument("--output", default="completeness.json", required=False)
    parser.add_argument("--radius", type=float, default=2.0)
    return parser.parse_args()


def _main():
    args = _parse_args()
    structure = gemmi.read_structure(args.structure)
    reference = gemmi.read_structure(args.reference)

    search = gemmi.NeighborSearch(structure, max_radius=args.radius)
    search.populate(include_h=False)

    matching = functools.partial(_matching_residue, structure, search, args.radius)

    stats = _calculate_stats(reference, matching)
    print(stats)
    print(100*stats.nucleic_built/stats.nucleic_total)
    with open(args.output, "w") as stream:
        json.dump(dataclasses.asdict(stats), stream, indent=4)


def calculate_completeness_from_string(reference: str, structure: str, radius: float) -> Dict[str, float]:
    structure = gemmi.read_structure(str(structure))
    reference = gemmi.read_structure(str(reference))

    search = gemmi.NeighborSearch(structure, max_radius=radius)
    search.populate(include_h=False)

    matching = functools.partial(_matching_residue, structure, search, radius)

    stats = _calculate_stats(reference, matching)
    return dataclasses.asdict(stats)


@dataclass
class Stats:
    protein_total: int = 0
    protein_built: int = 0
    protein_sequenced: int = 0
    nucleic_total: int = 0
    nucleic_built: int = 0
    nucleic_sequenced: int = 0


def _calculate_stats(reference, matching):
    stats = Stats()

    for chain in reference[0]:
        for residue in chain:
            info = gemmi.find_tabulated_residue(residue.name)
            # print("Looking at", chain.name, residue.name)
            # if info.is_amino_acid():
            #     atoms = {"N", "CA", "C"}
            #     if any(name not in residue for name in atoms):
            #         continue

            #     stats.protein_total += 1

            #     if matching(residue, atoms, same_type=False):
            #         stats.protein_built += 1

            #     if matching(residue, atoms, same_type=True):
            #         stats.protein_sequenced += 1

            if info.is_nucleic_acid():
                atoms = {"C1'", "C2'", "C3'", "C4'", "O4'", "C5'", "O5'", "P"}
                # atoms = {"P", "O5'", "C5'", "C4'", "C3'", "O3'"}

                if any(name not in residue for name in atoms):
                    # print(f"Missing atoms in {residue.name}")
                    continue

                stats.nucleic_total += 1

                if matching(chain, residue, atoms, same_type=False):
                    stats.nucleic_built += 1
                

                # if residue.name != "U" or "O2" in residue:  # UNK is U in Nautilus
                #     if matching(chain, residue, atoms, same_type=True):
                #         stats.nucleic_sequenced += 1
    return stats


def _matching_residue(structure, search, radius, chain, residue, atoms, same_type):
    x = [
        _matching_atom(structure, search, radius, residue, name, same_type)
        for name in atoms
    ]
    # if not all(x):
        # print("Missing ", chain.name, residue.seqid, residue.name)
        # for yi, y in enumerate(x):
        #     if not y:
        #         print(list(atoms)[yi])
        # print()
        
    return all(x)


def _matching_atom(structure, search, radius, residue, name, same_type):
    for atom_alt in residue[name]:
        for mark in search.find_atoms(atom_alt.pos, "\0", radius=radius):
            cra = mark.to_cra(structure[0])
            if cra.atom.name == name:
                if not same_type or cra.residue.name == residue.name:
                    return True
    return False


if __name__ == "__main__":
    _main()
