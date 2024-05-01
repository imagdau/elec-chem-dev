from setuptools import setup, find_packages

setup(
    name='elecChemDev',
    version='1.0.0',
    url='https://github.com/imagdau/elec-chem-dev.git',
    author='Ioan-Bogdan Magdau',
    author_email='Ioan.Magdau@newcastle.ac.uk',
    description='Simple package for constructing all-atom simulations for electrochemical devices and interfaces',
    packages=find_packages(),
    install_requires=[
        "ipywidgets~=7.7.0",
        "nglview~=2.7.7",
        "mp_api",
        "pymatgen",
        "ase",
        "aseMolec @ git+https://github.com/imagdau/aseMolec.git",
        "tqdm"
    ]
)

