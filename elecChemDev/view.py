import nglview as ngl

def view_atoms(config):
    view = ngl.show_ase(config)
    view.add_representation(repr_type='unitcell')
    view._set_size(w='100%', h='500px')
    return view