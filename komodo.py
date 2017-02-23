#!/usr/bin/env python

"""Command line utilities for simple Meraxes / 21cmFAST based tasks."""

import numpy as np
from dragons import meraxes
import click
from astropy.table import Table
from astropy import units as U, log
from pathlib import Path
import os
import shutil

__author__ = "Simon Mutch"
__date__ = "2015-10-09"
__version__ = 0.1

@click.group()
def komodo():
    pass

@komodo.command()
@click.argument('fname', type=click.STRING)
def xHI_evo(fname):
    log.setLevel('WARNING')
    meraxes.io.set_little_h(fname)
    snaplist, zlist, lbtime = meraxes.io.read_snaplist(fname)
    xhi = meraxes.io.read_global_xH(fname, snaplist, quiet=True)
    tab = Table((snaplist, zlist, lbtime, xhi),
                names=('snapshot', 'redshift', 'lookback_time', 'xHI'))
    tab['lookback_time'].unit = U.Myr
    tab.pprint(max_lines=-1, max_width=-1)

@komodo.command()
@click.argument('fname', type=click.STRING)
def snaplist(fname):
    log.setLevel('WARNING')
    meraxes.io.set_little_h(fname)
    snaplist, zlist, lbtime = meraxes.io.read_snaplist(fname)
    tab = Table((snaplist, zlist, lbtime),
                names=('snapshot', 'redshift', 'lookback_time'))
    tab['lookback_time'].unit = U.Myr
    tab.pprint(max_lines=-1, max_width=-1)

@komodo.command()
@click.argument('direc', type=click.Path())
@click.option('--exec_only', type=click.BOOL, default=False,
              help="Only copy executable.")
def newrun(direc, exec_only):
    flist = ('../bin/meraxes', '../input/input.par', '../input/snaplist.txt')
    if exec_only:
        flist = flist[0]
    if all(Path(f).exists() for f in flist):
        meraxes_dir = Path('.')
    else:
        meraxes_dir = os.environ['MERAXES_DIR']/Path('src')

    direc = Path(direc)
    if not direc.exists():
        direc.mkdir()

    for f in (meraxes_dir/Path(f) for f in flist):
        shutil.copy(str(f), str(direc/f.name))


if __name__ == "__main__":
    komodo()