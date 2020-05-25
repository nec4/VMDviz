# VMDviz
### Python automation for creating molecular trajectory movies 

---

### About

[VMD](https://www.ks.uiuc.edu/Research/vmd/) is a powerful and flexible
molecular visualization and analysis program, traditionally scriptable through
Tcl.
[vmd-python](https://vmd.robinbetz.com/) provides a set of python 3 bindings
for (most) VMD functions and subroutines. This package uses vmd-python to create
automated movie productions for molecular trajectories through two steps:

1. Individual frame manipulation and rendering through vmd-python commands
2. Image collation/movie production through
[ImageMagick](https://imagemagick.org/index.php)

### Dependencies

All dependencies should be available through your favorite package manager.

1. vmd-python 3.0+
2. vmd
3. numpy
4. ImageMagick

### Installation

1. `git clone https://github.com/nec4/vmdviz/ .`
2. `cd vmdviz`
3. `python setup.py install`

### Usage

For script info, run:

`$ vmdviz -h`

### Help

For help on a particular function/class, please run `help(function/class)`, or
see docstrings in source.

### TODO

1. Expand rendering options (current default is Tachyon, bundled with VMD)
2. Generalize rendering options in shell scripts
3. Reorganize representation options 
