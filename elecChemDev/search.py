from mp_api.client import MPRester
import warnings
from pandas import DataFrame
warnings.filterwarnings("ignore")

def get_elem_comb(elements):
    elements.sort(key=lambda element: element._atomic_mass, reverse=True)
    return "".join([el.symbol for el in elements])

class elyte(MPRester):
    def __init__(self):
        with open("api.key", "r") as keyFile:
            API_KEY = keyFile.readline().rstrip()
        super().__init__(API_KEY)
        self.docs = self.molecules.jcesr.search(nelements=(0,1000))
        
        
    def list_elem_combs(self):
        elem_combs = []
        for doc in self.docs:
            elem_combs.append(get_elem_comb(doc.elements))
        return sorted(list(set(elem_combs)))

            
# Natoms = len(doc.molecule._sites)
# if el_str in self.dict_by_elements:
#     self.dict_by_elements =  []
# else:
#     self.dict_by_elements.append()
    
    
# display(SVG(doc.svg))
# print(formula+':'+mpid)