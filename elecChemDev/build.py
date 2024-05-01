from tqdm import tqdm
import random
from ase.build.attach import attach_randomly
import ase.units
from aseMolec import anaAtoms as aa
from ase import Atoms

def attach_randomly_attempts(at1, at2, distance, Nattempts=100):
    attempt = 0
    while attempt < Nattempts:
        attempt += 1
        try:
            config = attach_randomly(at1, at2, distance)
            return config
        except RuntimeError:
            pass
    raise RuntimeError('Attach did not converge after '+str(attempt)+' attempts. Consider increasing Nattempts or Volume!')

def pack_mols(db, Nmols, dens=1.0, cell=[1,1,1], distance=2.0, Nattempts=200, fct=1):
    #compute total mass
    M = 0
    for at, N in zip(db, Nmols):
        M += at.get_masses().sum()*N

    #rescale volume to match target density
    config = Atoms('H', cell=cell, pbc=True) # start with dummy H atom
    densfact = (ase.units.m/1.0e2)**3/ase.units.mol
    V = M/dens*densfact
    scale = V/config.get_volume()
    config.cell *= scale**(1/3)

    #shuffle molecule collection
    col = []
    for at, N in zip(db, Nmols):
        for i in range(N):
            col.append(at)
    random.shuffle(col)
    
    #add molecules one by one
    for at in tqdm(col):
        config = attach_randomly_attempts(config, at, distance=distance, Nattempts=Nattempts)

    del config[0] # delete dummy H atom 
    aa.wrap_molecs([config], fct)
    config.center()
    
    return config
