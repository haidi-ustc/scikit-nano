# -*- coding: utf-8 -*-
"""
==============================================================================
SWNT bundle structure class (:mod:`sknano.structures._swnt_bundle`)
==============================================================================

.. currentmodule:: sknano.structures._swnt_bundle

"""
from __future__ import absolute_import, division, print_function
__docformat__ = 'restructuredtext en'

#import numbers

import numpy as np

from sknano.core.math import Vector
from sknano.core.refdata import dVDW
from ._compute_funcs import compute_bundle_density
from ._mixins import NanotubeBundleMixin
from ._swnt import SWNT

__all__ = ['SWNTBundle']


class SWNTBundle(NanotubeBundleMixin, SWNT):

    def __init__(self, nx=1, ny=1, Lx=None, Ly=None, vdw_spacing=dVDW,
                 bundle_packing=None, bundle_geometry=None, **kwargs):

        super(SWNTBundle, self).__init__(**kwargs)

        self.nx = nx
        self.ny = ny

        self.r1 = Vector()
        self.r2 = Vector()

        self.vdw_spacing = vdw_spacing
        self.bundle_geometry = bundle_geometry
        self._bundle_packing = bundle_packing

        self.bundle_coords = []

        self.__compute_bundle_params()

    def compute_bundle_params(self):
        """Compute/update nanotube bundle parameters."""

        self.r1.x = self.dt + self.vdw_spacing
        if self.bundle_packing is None and \
                self.bundle_geometry in ('square', 'rectangle'):
            self._bundle_packing = 'ccp'
        elif self.bundle_packing is None and \
                self.bundle_geometry in ('triangle', 'hexagon'):
            self._bundle_packing = 'hcp'

        if self.bundle_packing in ('cubic', 'ccp'):
            self.r2.y = self.r1.x
        else:
            self.r2.x = self.r1.x * np.cos(2 * np.pi / 3)
            self.r2.y = self.r1.x * np.sin(2 * np.pi / 3)
            if self.bundle_packing is None:
                self._bundle_packing = 'hcp'

        if self.bundle_geometry == 'hexagon':
            nrows = max(self.nx, self.ny, 3)
            if nrows % 2 != 1:
                nrows += 1

            ntubes_per_end_rows = int((nrows + 1) / 2)

            row = 0
            ntubes_per_row = nrows
            while ntubes_per_row >= ntubes_per_end_rows:
                if row == 0:
                    for n in xrange(ntubes_per_row):
                        dr = n * self.r1
                        self.bundle_coords.append(dr)
                else:
                    for nx in xrange(ntubes_per_row):
                        for ny in (-row, row):
                            dr = Vector()
                            dr.x = abs(ny * self.r2.x)
                            dr.y = ny * self.r2.y
                            dr = nx * self.r1 + dr
                            self.bundle_coords.append(dr)
                row += 1
                ntubes_per_row = nrows - row

        elif self.bundle_geometry == 'rectangle':
            Lx = 10 * self.Lx
            for nx in xrange(self.nx):
                for ny in xrange(self.ny):
                    dr = nx * self.r1 + ny * self.r2
                    while dr.x < 0:
                        dr.x += Lx
                    self.bundle_coords.append(dr)

        elif self.bundle_geometry == 'square':
            pass
        elif self.bundle_geometry == 'triangle':
            pass
        else:
            for nx in xrange(self.nx):
                for ny in xrange(self.ny):
                    dr = nx * self.r1 + ny * self.r2
                    self.bundle_coords.append(dr)

    __compute_bundle_params = compute_bundle_params

    @property
    def bundle_mass(self):
        return self.Ntubes * self.tube_mass

    @property
    def bundle_density(self):
        return compute_bundle_density(self.n, self.m, d_vdw=self._vdw_spacing,
                                      bond=self.bond, element1=self.element1,
                                      element2=self.element2)

    @property
    def bundle_packing(self):
        return self._bundle_packing

    @bundle_packing.setter
    def bundle_packing(self, value):
        if value not in ('ccp', 'hcp'):
            raise ValueError('Expected value to be `hcp` or `ccp`')
        self._bundle_packing = value
        self.__compute_bundle_params()

    @bundle_packing.deleter
    def bundle_packing(self):
        del self._bundle_packing

    @property
    def Natoms_per_bundle(self):
        return self.Ntubes * self.Natoms_per_tube

    @SWNT.Ntubes.getter
    def Ntubes(self):
        return len(self.bundle_coords)
