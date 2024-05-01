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
        "mp_api~=0.41.2",
        "pymatgen~=2024.3.1",
        "ase~=3.22.1",
        "aseMolec @ git+https://github.com/imagdau/aseMolec.git",
        "tqdm~=4.66.2"
    ]
)

