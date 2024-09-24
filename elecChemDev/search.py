from mp_api.client import MPRester
from pymatgen.io.ase import AseAtomsAdaptor
from ase import Atoms
from aseMolec import extAtoms as ea
import pandas as pd
from IPython.display import SVG
import warnings

warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', 100)

class elyte(MPRester):
    def __init__(self, path='api.key'):
        with open(path, "r") as keyFile:
            API_KEY = keyFile.readline().rstrip()
        super().__init__(API_KEY)
        self.docs = self.molecules.jcesr.search(nelements=(0,1000))
        col = {
            'elemComb': [],
            'natoms': [],
            'formula': [],
            'mass': [],
            'charge': [],
            'spin': [],
            'mpid': [],
            'svg': [],
            'hash': [],
            'Atoms': []
        }
        for doc in self.docs:
            at = Atoms(AseAtomsAdaptor.get_atoms(doc.molecule))
            ea.hash_atoms([at])
            col['elemComb'].append("".join(sorted(set(at.get_chemical_symbols()))))
            col['natoms'].append(len(at))
            col['formula'].append(at.get_chemical_formula())
            col['mass'].append(at.get_masses().sum())
            col['charge'].append(doc.molecule._charge)
            col['spin'].append(doc.molecule._spin_multiplicity)
            col['mpid'].append(doc.task_id) #for some reason, not unique
            col['svg'].append(doc.svg)
            col['hash'].append(at.info['uid'])
            col['Atoms'].append(at)
        self.df = pd.DataFrame(col).sort_values(by=['elemComb', 'natoms', 'mass', 'charge', 'spin']).drop_duplicates(subset=['hash']).set_index('hash')
        
    def get_molecs(self, hashes, field):
        col = []
        for hash in hashes:
            col.append(self.df.loc[hash][field])
        return col
            
    def show_pics(self, hashes):
        svgs = self.get_molecs(hashes, field='svg')
        display(*[SVG(svg) for svg in svgs])


class elode(MPRester):
    def __init__(self, path='api.key', elem=['Li', 'Ni', 'Mn', 'Co', 'O']):
        with open(path, "r") as keyFile:
            API_KEY = keyFile.readline().rstrip()
        super().__init__(API_KEY)
        self.docs = self.materials.search(elements=elem)
        col = {
            'elemComb': [],
            'natoms': [],
            'formula': [],
            'mass': [],
            'charge': [],
            'mpid': [],
            'hash': [],
            'Atoms': []
        }
        for doc in self.docs:
            at = Atoms(AseAtomsAdaptor.get_atoms(doc.structure))
            ea.hash_atoms([at])
            col['elemComb'].append("".join(sorted(set(at.get_chemical_symbols()))))
            col['natoms'].append(len(at))
            col['formula'].append(at.get_chemical_formula())
            col['mass'].append(at.get_masses().sum())
            col['charge'].append(doc.structure._charge)
            col['mpid'].append(doc.material_id) #for some reason, not unique
            col['hash'].append(at.info['uid'])
            col['Atoms'].append(at)
        self.df = pd.DataFrame(col).sort_values(by=['elemComb', 'natoms', 'mass', 'charge']).drop_duplicates(subset=['hash']).set_index('hash')

    def get_material(self, hash, field):
        return self.df.loc[hash][field]
