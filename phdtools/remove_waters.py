import gemmi 
import argparse

def remove_waters(input: str, output:str):
    s = gemmi.read_structure(input)
    os = gemmi.Structure()
    os.cell = s.cell
    os.spacegroup_hm = s.spacegroup_hm
    om = gemmi.Model(s[0].num)
    
    for c in s[0]:
        oc = gemmi.Chain(c.name)
        for r in c: 
            t = gemmi.find_tabulated_residue(r.name)
            remove = t.is_water()
            if not remove: 
                oc.add_residue(r)
            else:
                print("Removing", c.name, r.name, r.seqid)
        om.add_chain(oc)
        
    os.add_model(om)
    os.make_mmcif_document().write_file(output)      

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    remove_waters(args.input, args.output)
    
    
    
if __name__ == "__main__":
    main()