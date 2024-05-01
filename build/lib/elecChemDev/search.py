from mp_api.client import MPRester
import warnings
import pandas as pd
from pymatgen.io.ase import AseAtomsAdaptor
from ase import Atoms

warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', 100)

class elyte(MPRester):
    def __init__(self):
        with open("api.key", "r") as keyFile:
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
            'Atoms': []
        }
        for doc in self.docs:
            at = Atoms(AseAtomsAdaptor.get_atoms(doc.molecule))
            col['elemComb'].append("".join(sorted(set(at.get_chemical_symbols()))))
            col['natoms'].append(len(at))
            col['formula'].append(at.get_chemical_formula())
            col['mass'].append(at.get_masses().sum())
            col['charge'].append(doc.molecule._charge)
            col['spin'].append(doc.molecule._spin_multiplicity)
            col['mpid'].append(doc.task_id)
            col['svg'].append(doc.svg)
            col['Atoms'].append(at)

        self.df = pd.DataFrame(col).sort_values(by=['elemComb', 'natoms', 'mass', 'charge', 'spin'])
        