from vmdviz.tools import *
import sys
import argparse


def main():
    """simple script for producing rotation movies of the
    first and final configurations of a CACB trajectory, as
    well as a video of the full trajectory.
    """

    args = sys.argv[1:]
    options = argparser(args)
    print(options)

    # Data payload
    load_data = {'filetype' : options.simtype,
                 'filename' : options.simfile,
                 'stride' : options.stride,
                 'waitfor' : -1}

    # VDMmolecule creation
    model = VMDMolecule(options.pdbfile, style=[CG_STYLE, BONDS_STYLE],
                        load_data=load_data, flush_pdb_frame=True)

    # CA backbone bonds
    CA_selection = atomsel('name CA').index
    residues = [atomsel('resid {}'.format(i) +
                ' and (name CA or name CB)').index for i in range(1,11)]
    backbone_bonds = [(CA_selection[i], CA_selection[i+1])
                      for i in range(len(CA_selection[:-1]))]

    # CA-CB cbonds
    CA_CB_bonds = []
    for residue in residues:
        if len(residue) == 2:
            CA_CB_bonds.append(tuple(residue))

    generate_bonds(model.molid, backbone_bonds)
    generate_bonds(model.molid, CA_CB_bonds)

    axes.set_location('OFF')
    display.update()
    generate_rotation_movie(model, options.basename + "_init_rotate" +
                            "_step_{}".format(options.anglestep),
                            save_dir=options.savedir,
                            division=options.anglestep,
                            create_outfile=True, frame=0)
    generate_rotation_movie(model, options.basename + "_final_rotate" +
                            "_step_{}".format(options.anglestep),
                            save_dir=options.savedir,
                            division=options.anglestep,
                            create_outfile=True, frame=-1)
    generate_trajectory_movie(model, options.basename + "_traj" +
                              "_stride_{}".format(options.stride) +
                              "_step_{}".format(options.trajstep) +
                              "_smoothing_{}".format(options.smoothing),
                              save_dir=options.savedir,
                              start=0, stop=-1, step=options.trajstep,
                              smoothing=options.smoothing)


def argparser(args):
    parser = argparse.ArgumentParser(description='automated video production for '
                            'protein trajectory movies, creating rotation '
                            'movies for initial and final configurations '
                            'and full trajectory movie.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("pdbfile", help="PDB file to provide structure/topolgy")
    parser.add_argument("simfile", help="trajectory file")
    parser.add_argument("--simtype", help="trajectory type/file extension",
                        default='xtc')
    parser.add_argument("--savedir", help="directory in which to save movies",
                        default='.')
    parser.add_argument("--stride", help="frame stride for loading trajectory",
                        default=100, type=int)
    parser.add_argument("--basename", help="base file name for final movie files",
                        default='my_sim')
    parser.add_argument("--trajstep", help="frame step size for trajecotry movie rendering",
                        default=1, type=int)
    parser.add_argument("--anglestep", help="angle step size for rotation movie rendering",
                        default=1, type=int)
    parser.add_argument("--smoothing", help="smoothing window size for movie rendering",
                        default=0, type=int)
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
