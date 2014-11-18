# -*- coding: utf-8 -*-
"""
===============================================================================
Atom sub-class for POAV analysis (:mod:`sknano.core.atoms._poav_atom`)
===============================================================================

An `Atom` sub-class for POAV analysis.

.. currentmodule:: sknano.core.atoms._poav_atom

"""
from __future__ import absolute_import, division, print_function
__docformat__ = 'restructuredtext en'

import functools
import operator

import numpy as np

from sknano.core.math import vector as vec

from ._kdtree_atom import KDTAtom

__all__ = ['POAV', 'POAV1', 'POAV2', 'POAVR', 'POAVAtomMixin', 'POAVAtom']


class POAV(object):
    """Base class for POAV analysis.

    Parameters
    ----------
    sigma_bonds : `~sknano.core.atoms.Bonds`
        `~sknano.core.atoms.Bonds` instance.

    """
    def __init__(self, sigma_bonds):
        self.bonds = sigma_bonds
        self.b1 = self.bonds[0].vector
        self.b2 = self.bonds[1].vector
        self.b3 = self.bonds[2].vector

        self._v1 = self.b1
        self._v2 = self.b2
        self._v3 = self.b3

        self._T = vec.scalar_triple_product(self.V1, self.V2, self.V3) / 6

        self._pyramidalization_angles = None
        self._sigma_pi_angles = None
        self._misalignment_angles = None

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def v3(self):
        return self._v3

    @property
    def t(self):
        return vec.scalar_triple_product(self.v1, self.v2, self.v3)

    @property
    def vpi(self):
        return (self.reciprocal_v1 +
                self.reciprocal_v2 +
                self.reciprocal_v3) / self.t

    @property
    def Vpi(self):
        return self.vpi.unit_vector

    @property
    def reciprocal_v1(self):
        return vec.cross(self.v2, self.v3)

    @property
    def reciprocal_v2(self):
        return vec.cross(self.v3, self.v1)

    @property
    def reciprocal_v3(self):
        return vec.cross(self.v1, self.v2)

    @property
    def V1(self):
        return self.b1.unit_vector

    @property
    def V2(self):
        return self.b2.unit_vector

    @property
    def V3(self):
        return self.b3.unit_vector

    @property
    def R1(self):
        return self.b1.length

    @property
    def R2(self):
        return self.b2.length

    @property
    def R3(self):
        return self.b3.length

    @property
    def T(self):
        return self._T

    @property
    def A(self):
        return self.vpi.magnitude

    @property
    def H(self):
        return 3 * self.T / self.A

    @property
    def sigma_pi_angles(self):
        return self._sigma_pi_angles

    @sigma_pi_angles.setter
    def sigma_pi_angles(self, value):
        if not isinstance(value, list):
            raise TypeError('Expected a number')
        self._sigma_pi_angles = value

    @property
    def pyramidalization_angles(self):
        """Return the pyramidalization angle :math:`\\theta_P`"""
        return self._pyramidalization_angles

    @pyramidalization_angles.setter
    def pyramidalization_angles(self, value):
        if not isinstance(value, list):
            raise TypeError('Expected a number')
        self._pyramidalization_angles = value

    @property
    def misalignment_angles(self):
        return self._misalignment_angles

    @misalignment_angles.setter
    def misalignment_angles(self, value):
        if not isinstance(value, list):
            raise TypeError('Expected a number')
        self._misalignment_angles = value

    def todict(self, rad2deg=False):
        #return dict(sigma_pi_angles=self.sigma_pi_angles,
        #            pyramidalization_angles=self.pyramidalization_angles,
        #            misalignment_angles=self.misalignment_angles,
        #            T=self.T, H=self.H, A=self.A)
        sigma_pi_angles = self.sigma_pi_angles
        pyramidalization_angles = self.pyramidalization_angles
        misalignment_angles = self.misalignment_angles
        if rad2deg:
            sigma_pi_angles = np.degrees(sigma_pi_angles)
            pyramidalization_angles = np.degrees(pyramidalization_angles)
            misalignment_angles = np.degrees(misalignment_angles)

        return dict(bond1=self.b1.length,
                    bond2=self.b2.length,
                    bond3=self.b3.length,
                    sigma_pi_angle1=sigma_pi_angles[0],
                    sigma_pi_angle2=sigma_pi_angles[1],
                    sigma_pi_angle3=sigma_pi_angles[2],
                    pyramidalization_angle1=pyramidalization_angles[0],
                    pyramidalization_angle2=pyramidalization_angles[1],
                    pyramidalization_angle3=pyramidalization_angles[2],
                    misalignment_angle1=misalignment_angles[0],
                    misalignment_angle2=misalignment_angles[1],
                    misalignment_angle3=misalignment_angles[2],
                    T=self.T, H=self.H, A=self.A)


class POAV1(POAV):
    """:class:`POAV` sub-class for POAV1 analysis."""

    def __init__(self, *args):
        super(POAV1, self).__init__(*args)

        self._v1 = self.V1
        self._v2 = self.V2
        self._v3 = self.V3

    @property
    def m(self):
        cos2sigmapi = np.cos(np.mean(self.sigma_pi_angles))**2
        return 2 * cos2sigmapi / (1 - 3 * cos2sigmapi)

    @property
    def n(self):
        return 3 * self.m + 2

    def todict(self, rad2deg=False):
        super_dict = super(POAV1, self).todict(rad2deg=rad2deg)
        super_dict.update(dict(m=self.m, n=self.n))
        return super_dict


class POAV2(POAV):
    """:class:`POAV` sub-class for POAV2 analysis."""

    def __init__(self, *args):
        super(POAV2, self).__init__(*args)

        bond_angles = self.bonds.angles
        bond_angle_pairs = self.bonds.bond_angle_pairs

        vi = []
        for bond, pair in zip(self.bonds, bond_angle_pairs):
            cosa = np.cos(bond_angles[np.in1d(self.bonds, pair, invert=True)])
            vi.append(cosa * bond.vector.unit_vector)

        self._v1 = vi[0]
        self._v2 = vi[1]
        self._v3 = vi[2]

        self.cosa12 = np.cos(bond_angles[0])
        self.cosa13 = np.cos(bond_angles[1])
        self.cosa23 = np.cos(bond_angles[2])

        self._T = \
            -functools.reduce(operator.mul, np.cos(bond_angles), 1) * self.T

    @property
    def n1(self):
        return -self.cosa23 / (self.cosa12 * self.cosa13)

    @property
    def n2(self):
        return -self.cosa13 / (self.cosa12 * self.cosa23)

    @property
    def n3(self):
        return -self.cosa12 / (self.cosa23 * self.cosa13)

    @property
    def m(self):
        s1 = 1 / (1 + self.n1)
        s2 = 1 / (1 + self.n2)
        s3 = 1 / (1 + self.n3)
        return 1 / sum([s1, s2, s3]) - 1

    def todict(self, rad2deg=False):
        super_dict = super(POAV2, self).todict(rad2deg=rad2deg)
        super_dict.update(dict(m=self.m, n1=self.n1, n2=self.n2, n3=self.n3))
        return super_dict


class POAVR(POAV):
    """:class:`POAV` sub-class for POAVR analysis."""

    def __init__(self, *args):
        super(POAVR, self).__init__(*args)

        vi = []
        for R, V in zip([self.R1, self.R2, self.R3],
                        [self.V1, self.V2, self.V3]):
            vi.append(R * V)

        self._v1 = vi[0]
        self._v2 = vi[1]
        self._v3 = vi[2]
        self._T = self.R1 * self.R2 * self.R3 * self.T


class POAVAtomMixin(object):
    """Mixin class for `POAVAtom`."""
    @property
    def POAV1(self):
        """:class:`~sknano.utils.analysis.POAV1` instance."""
        return self._POAV1

    @POAV1.setter
    def POAV1(self, value):
        """Set :class:`~sknano.utils.analysis.POAV1` instance."""
        if not isinstance(value, POAV1):
            raise TypeError('Expected a `POAV1` instance.')
        self._POAV1 = value

    @property
    def POAV2(self):
        """:class:`~sknano.utils.analysis.POAV2` instance."""
        return self._POAV2

    @POAV2.setter
    def POAV2(self, value):
        """Set :class:`~sknano.utils.analysis.POAV2` instance."""
        if not isinstance(value, POAV2):
            raise TypeError('Expected a `POAV2` instance.')
        self._POAV2 = value

    @property
    def POAVR(self):
        """:class:`~sknano.utils.analysis.POAVR` instance."""
        return self._POAVR

    @POAVR.setter
    def POAVR(self, value):
        """Set :class:`~sknano.utils.analysis.POAVR` instance."""
        if not isinstance(value, POAVR):
            raise TypeError('Expected a `POAVR` instance.')
        self._POAVR = value


class POAVAtom(POAVAtomMixin, KDTAtom):
    """An `Atom` sub-class for POAV analysis."""
    _atomattrs = KDTAtom._atomattrs + ['POAV1', 'POAV2', 'POAVR']

    def __init__(self, **kwargs):
        super(POAVAtom, self).__init__(**kwargs)
        self._POAV1 = None
        self._POAV2 = None
        self._POAVR = None
