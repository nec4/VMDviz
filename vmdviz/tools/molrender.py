from vmd import molecule as mol
from vmd import molrep
from vmd import display
from vmd import animate
from vmd import render
from vmd import axes
from vmd import topology
from vmd import atomsel
from vmd import trans
from vmd import graphics
from vmd import evaltcl
from collections.abc import Iterable
import os
import numpy as np
import subprocess


def dir_check(dirname):
    """Helper function to check if a directory exists or not,
    and ask the user if they would like to create it if it does
    not.

    Parameters
    ----------
    dirname : str
        Directory whose existence is to be queried.

    Returns
    -------
    Boolean
        The function returns True if the directory either already exists
        the user has authorized its creation when prompted. The function
        returns False if the directory does not exist and the user does
        not authorize its creation.
    """

    if not os.path.exists(dirname):
        print("Directory '{}' does not exist. Create it now? (y|n): ".format(dirname),
               end="")
        answer = input()
        print(answer)
        while(answer not in ['y', 'n']):
            print("Please enter (y|n): ")
            answer = input()
        if answer == 'y':
            os.mkdir(dirname)
            return True
        else:
            return False
    else:
        return True


def generate_bonds(molid, indices):
    """Generates bonds between backbone atoms of adjacent
    amino acids in teh molecule

    Parameters
    ----------
    molid : int
        Molecule id for which the bonds will be created
    indices : list of two-tuples
        List of index pairs that define the sites of the
        bonds. For example, indices=[(0,2),(2,3),(3,4)]
        produces bonds between sites 0 and 2, 2 and 3,
        and 3 and 4.
    """

    for pair in indices:
        topology.addbond(*pair)


def generate_rotation_movie(molecule, filename, save_dir='.', frame=0,
                            angle=360, division=1.0,
                            renderer='Tachyon', render_ext='dat'):
    """Function for generating movies where a static molecule frame is
    rotated through an angle. Individual files for each subrotation
    are generated, which can then be processed and combined into a
    movie file.

    Parameters
    ----------
    molecule : VMDMolecule
        Molecule for which the movie is made.
    filename : str
        The basename of the individual files for each subrotation
    save_dir : str (default='.')
        The directory in which generated files will be saved.
    frame : int (default=0)
        The trajectory frame that is rotated about.
    angle : float (default=360.0)
        The angle through which the molecule is rotated through.
    division : float (default=1.0)
        The angular (degree) for each subrotation.
    renderer : str (default='Tachyon')
        Program for rendering individual images. Must be a valid
        rendering program bundled with VMD. For available rendering
        programs, see:

            https://www.ks.uiuc.edu/Research/vmd/vmd-1.7.1/ug/node89.html
    render_ext : str (default='dat')
        filename extension for indivudally rendered files.
    """

    check = dir_check(save_dir)
    if not check:
        return None

    print("generating rotation movie...")
    if angle % division != 0:
        raise RuntimeError("Angle must be evenly divisble by dvision")
    else:
        if frame == -1:
            frame = mol.numframes(molecule.molid)  - 1
        mol.set_frame(molecule.molid, frame)
        display.update()
        sub_rotations = int(angle / division)
        current_angle = 0.0
        for i in range(0,sub_rotations):
            render.render(renderer, save_dir + '/' + filename +
                          '{:0>9}.{}'.format(int(i), render_ext))
            trans.rotate_scene('y', division)
            display.update()
            current_angle += division


def generate_trajectory_movie(molecule, filename, save_dir='.', start=0, stop=-1,
                              step=1, smoothing=0,
                              renderer='Tachyon', render_ext='dat'):
    """Function for generating movies of molecular trajectories

    Parameters
    ----------
    molecule : VMDMolecule
        Molecule for which the movie is made.
    filename : str
        The basename of the individual files for each subrotation
    save_dir : str (default='.')
        The directory in which generated files will be saved.
    start : int (default=0)
        The starting frame
    stop : float (default=360.0)
        The ending frame
    step : float (default=1.0)
        The the step stride of the loaded frames
    smoothing : int (default=0)
        Size of smoothing window in frames to be applied to all
        representations of the VMDMolecule
    renderer : str (default='Tachyon')
        Program for rendering individual images. Must be a valid
        rendering program bundled with VMD. For available rendering
        programs, see:

            https://www.ks.uiuc.edu/Research/vmd/vmd-1.7.1/ug/node89.html

    render_ext : str (default='dat')
        filename extension for indivudally rendered files.
    """

    # Perform checks
    check = dir_check(save_dir)
    if not check:
        return None

    if stop < 0:
        if stop != -1:
           raise ValueError("negative values for 'stop' can only be -1, "
                            "in which case the stop frame is the final "
                            "loaded frame.")
    num_loaded_frames = mol.numframes(molecule.molid)
    # explicitly switch 'stop' to the last frame index
    if stop == -1:
        stop = num_loaded_frames - 1

    if smoothing > 0:
        reps = molrep.num(molecule.molid)
        for i in range(reps):
           molrep.set_smoothing(molecule.molid, i, smoothing)

    print("generating '{}' trajectory movie...".format(filename))
    frames = np.arange(start, stop, step)
    mol.set_frame(molecule.molid, start)
    current_frame = start
    display.update()
    for i in frames:
        mol.set_frame(molecule.molid, i)
        display.update()
        render.render(renderer, save_dir + '/' + filename +
                      '_{:0>9}.{}'.format(int(i), render_ext))


def init_display(display_options, axes_options):
    """Function for initializing VMD scene options

    Parameters
    ----------
    display_options : dict
        scene/display options for VMD. These are specified as key-value
        pairs for each attribute in the VMD display options list. For
        this complete list, see the following:

            https://www.ks.uiuc.edu/Research/vmd/current/ug/node126.html

    """

    display.set(**display_options)
    if 'set_location' in axes_options.keys():
        axes.set_location(axes_options['set_location'])
    display.update()


class VMDMolecule():
    """Class for wrapping VMD molecule functionalities

    Parameters
    ----------
    pdb_file : str
        Specifies the PDB file from which topological and
        coordinate data is loaded.
    load_data : dict (default=None)
        Specifies trajectory loading routine according to
        VMD's read function options:

            filetype (str) – File type of coordinate data
            filename (str) – Path to coordinate data
            first (int) – First frame to read. Defaults to 0 (first frame)
            last (int) – Last frame to read, or -1 for the end. Defaults to -1
            stride (int) – Frame stride. Defaults to 1 (read all frames)
            waitfor (int) – Number of frames to load before returning.
                Defaults to 1, then loads asyncronously in background.
                Set to -1 to load all frames
            volsets (list of int) – Indices of volumetric datasets to read
                in from the file. Invalid indices will be ignored.

        where each option is specified by key-value pair. For example, to
        load a Gromacs XTC file from file 'traj_001.xtc' with a stride
        of 10, load_data should be passed as:

            load_data = {'filetype' : 'xtc',
                         'filename' : 'traj_001.xtc',
                         'stride' : 10}

    styles : dict or list of dict (default=None)
        Dictionary(ies) used to specify VMD representations of the
        molecule. Key-value pairs correspond to the options in VMD's
        addrep function:

            style : str, (like 'NewCartoon')
            color : str, Coloring method (like 'ColorID 1' or 'Type')
            selection: str, Atoms to apply representation to
            material: str, Material for represenation (like ‘Opaque’)

        For example, to have the molecule represented using a Van der
        Waals style with bead size 4 angstroms and colors determined
        by sequence index, styles should be:

            styles = {'style' : 'VDW 4.0',
                      'color' : 'index'}

    name : str (default='my_molecule')
        Specifies the name of the molecule.
    flush_pdb_frame : Boolean (default=False)
        If True, the coordinate frame accompanying the PDB file will be
        deleted. This is useful if trajectory data does not have a
        have a starting configuration that is the same as the PDB
        structure.
    align : Boolean (default=True)
        If True, all frames of loaded trajectory data will be aligned
        to the configuration in the first trajectory frame.
    """

    def __init__(self, pdb_file, load_data=None, style=None,
                 name='my_molecule', flush_pdb_frame=False,
                 align=True, center=True):
        self.molid = mol.new(name)
        mol.rename(self.molid, name)
        self.name = name
        mol.read(self.molid, 'pdb', pdb_file, beg=0, end=0, skip=1, waitfor=-1)
        self.all_atoms = atomsel("all")

        if flush_pdb_frame:
            mol.delframe(self.molid) # flush trivial frame

        if load_data:
            self.load_data(load_data, align=align)
        if style:
            # delete the default representation
            molrep.delrep(self.molid, 0)
            for rep in style:
                molrep.addrep(self.molid, **rep)


    def load_data(self, load_data, align=True):
        """Method for loading trajectory data

        Parameters
        ----------
        load_data : dict
           dictionary of VMD read routine options. See
           VMDMolecule.__init__() docs.
        """

        if not isinstance(load_data, dict):
            raise ValueError("load_data must be a dictionary with "
                             "key-value pairs corresponding to VMD "
                             "read command options.")
        else:
            mol.read(self.molid, **load_data)
            if align:
                self.self_align()
            print("{} frames loaded.".format(mol.numframes(self.molid)))
            evaltcl("display resetview")

    def self_align(self):
        """Method for align trajectory frames to the initial frame
        to prevent the molecule from drifting out of focus during the
        simulation visualiation. This method can only be called after
        trajectory frames have been loaded into the VMDMolecule.
        """
        print("Self aligning molecule...")
        mol.set_frame(self.molid,0)
        base_selection = atomsel('all', frame=0)
        current_selection =  atomsel('all')
        for i in range(mol.numframes(self.molid)):
            mol.set_frame(self.molid, i)
            current_selection.update()
            trans_matrix = current_selection.fit(base_selection)
            current_selection.move(trans_matrix)
            display.update()
