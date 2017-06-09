#!/usr/bin/env python

"""Command line utilities for simple Meraxes / 21cmFAST based tasks."""

import click

__author__ = "Simon Mutch"
__date__ = "2015-10-09"
__version__ = 0.1

@click.group()
def komodo():
    pass

@komodo.command()
@click.argument('fname', type=click.STRING)
@click.option('--weight', '-w', type=click.Choice(['volume', 'mass']),
              default='volume')
def xHI_evo(fname, weight):
    from dragons import meraxes
    from astropy.table import Table
    from astropy import units as U, log

    log.setLevel('WARNING')
    meraxes.io.set_little_h(fname)
    snaplist, zlist, lbtime = meraxes.io.read_snaplist(fname)
    xhi = meraxes.io.read_global_xH(fname, snaplist, weight=weight, quiet=True)
    tab = Table((snaplist, zlist, lbtime, xhi),
                names=('snapshot', 'redshift', 'lookback_time', 'xHI'))
    tab['lookback_time'].unit = U.Myr
    tab.pprint(max_lines=-1, max_width=-1)

@komodo.command()
@click.argument('fname', type=click.STRING)
def snaplist(fname):
    from dragons import meraxes
    from astropy.table import Table
    from astropy import units as U, log

    log.setLevel('WARNING')
    meraxes.io.set_little_h(fname)
    snaplist, zlist, lbtime = meraxes.io.read_snaplist(fname)
    tab = Table((snaplist, zlist, lbtime),
                names=('snapshot', 'redshift', 'lookback_time'))
    tab['lookback_time'].unit = U.Myr
    tab.pprint(max_lines=-1, max_width=-1)

@komodo.command()
@click.argument('fname', type=click.STRING)
def gitref(fname):
    from dragons import meraxes

    ref, diff = meraxes.io.read_git_info(fname)
    print(ref.decode('utf-8'))
    if diff:
        print('===')
        print(diff.decode('utf-8'))

@komodo.command()
@click.argument('direc', type=click.Path())
@click.option('--exec_only', is_flag=True, help="Only copy executable.")
def newrun(direc, exec_only):
    from pathlib import Path
    import os
    import shutil

    flist = ('../bin/meraxes', '../input/input.par', '../input/snaplist.txt')
    if exec_only:
        flist = [flist[0],]
    if all(Path(f).exists() for f in flist):
        meraxes_dir = Path('.')
    else:
        meraxes_dir = os.environ['MERAXES_DIR']/Path('src')

    direc = Path(direc)
    if not direc.exists():
        direc.mkdir()

    for f in (meraxes_dir/Path(f) for f in flist):
        shutil.copy(str(f), str(direc/f.name))

@komodo.command()
@click.argument('z', nargs=-1, type=click.FLOAT)
@click.option('--snaplist', is_flag=True, help="Create meraxes snaplist"
              " compatible output")
@click.option('--alist', type=click.Path(exists=True),
              help="Meraxes compatible expansion factor list")
def select_snaps(z, snaplist=False, alist=None):
    import numpy as np
    from astropy.table import Table
    from pathlib import Path

    if alist is None:
        alist = str(Path(__file__).parent / Path('data/tiamat_alist.txt'))

    exp_factor = np.loadtxt(alist)

    if not hasattr(z, '__iter__'):
        z = [z]

    z = np.array(z, float)
    z_avail = 1.0 / exp_factor - 1.0

    nearest_snaps = np.ones(z.size, int) * -1
    nearest_zs = np.ones(z.size) * -1
    for ii, v in enumerate(z):
        nearest_snaps[ii] = np.argmin(np.abs(z_avail - v))
        nearest_zs[ii] = z_avail[nearest_snaps[ii]]

    if not snaplist:
        tab = Table((z, nearest_zs, nearest_snaps),
                    names=('requested', 'nearest', 'snapshot'))
        tab.pprint(max_lines=-1, max_width=-1)
    else:
        line = " ".join(["{:d}".format(snap) for snap in nearest_snaps])
        print(line)

    return nearest_snaps, nearest_zs

@komodo.command()
@click.argument('fname', type=click.Path(exists=True))
def galaxy_props(fname):
    from dragons import meraxes
    from astropy.table import Table
    import h5py as h5

    def _get_gal_dtype(k, v):
        if isinstance(v, h5.Group):
            try:
                return v['Galaxies'].dtype
            except KeyError:
                pass

    def _get_format_str(dtype, name):
        dt = dtype[name]
        shape = dt.shape
        if len(shape) > 0:
            return ' '.join((dt.subdtype[0].str, str(shape)))
        else:
            return dt.str

    # find a galaxy structure, get the dtype and also grab the h conversions
    with h5.File(fname) as fd:
        gal_dtype = fd.visititems(_get_gal_dtype)
        h_conv = dict(fd['HubbleConversions'].attrs.items())

    # grab the units too
    units = meraxes.read_units(fname)

    # print a table
    props = gal_dtype.names
    formats = [_get_format_str(gal_dtype, prop) for prop in props]
    tab = Table((props, [h_conv[p] for p in props], [units[p] for p in props], formats),
                names=('property', 'h conversion', 'unit', 'dtype'))
    tab.pprint(max_lines=-1, max_width=-1)


if __name__ == "__main__":
    komodo()
