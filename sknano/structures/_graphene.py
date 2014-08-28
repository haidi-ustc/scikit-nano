# -*- coding: utf-8 -*-
"""
===============================================================================
Graphene structure classes (:mod:`sknano.structures._graphenes`)
===============================================================================

.. currentmodule:: sknano.structures._graphenes

"""
from __future__ import absolute_import, division, print_function
__docformat__ = 'restructuredtext en'

#import itertools

import numpy as np

from ..core.atoms import Atom
from ..core.math import Vector
from ..core.refdata import CCbond, dVDW, grams_per_Da

edge_types = {'armchair': 'AC', 'zigzag': 'ZZ'}

__all__ = ['GraphenePrimitiveCell', 'Graphene', 'BilayerGraphene']


class GraphenePrimitiveCell(object):
    """Class for generating interactive Graphene primitive unit cell.

    Parameters
    ----------
    bond : float, optional
        bond length between nearest-neighbor atoms in **Angstroms**.

    """
    def __init__(self, bond=CCbond, **kwargs):
        self._bond = bond
        self._a = np.sqrt(3) * self._bond

        self._a1 = Vector(nd=2)
        self._a2 = Vector(nd=2)

        self._a1.x = self._a2.x = np.sqrt(3) / 2 * self._a
        self._a1.y = 1 / 2 * self._a
        self._a2.y = -self._a1.y

        self._b1 = Vector(nd=2)
        self._b2 = Vector(nd=2)

        self._b1.x = self._b2.x = 1 / np.sqrt(3) * 2 * np.pi / self._a
        self._b1.y = 2 * np.pi / self._a
        self._b2.y = -self._b1.y

    @property
    def a(self):
        """Length of graphene unit cell vector."""
        return self._a

    @property
    def a1(self):
        """:math:`a_1` unit vector."""
        return self._a1

    @property
    def a2(self):
        """:math:`a_2` unit vector."""
        return self._a2

    @property
    def b1(self):
        """:math:`b_1` reciprocal lattice vector."""
        return self._b1

    @property
    def b2(self):
        """:math:`b_2` reciprocal lattice vector."""
        return self._b2


class Graphene(object):
    """Class for generating interactive Graphene objects.

    Parameters
    ----------
    length : float, optional
        Length of graphene sheet in **nanometers**
    width : float, optional
        Width of graphene sheet in **nanometers**
    edge : {'AC', 'armchair', 'ZZ', 'zigzag'}, optional
        **A**\ rm\ **C**\ hair or **Z**\ ig\ **Z**\ ag edge along
        the `length` of the sheet.
    element1, element2 : {str, int}, optional
        Element symbol or atomic number of basis
        :class:`~sknano.core.atoms.Atom` 1 and 2
    bond : float, optional
        bond length between nearest-neighbor atoms in **Angstroms**.
    nlayers : int, optional
        Number of graphene layers.
    layer_spacing : float, optional
        Distance between layers in **Angstroms**.
    stacking_order : {'AA', 'AB'}, optional
        Stacking order of graphene layers
    verbose : bool, optional
        verbose output

    Notes
    -----
    For now, the graphene structure is generated using a
    conventional unit cell, not the primitive unit cell.

    .. todo::

       Add notes on unit cell calculation.

    """

    def __init__(self, length=None, width=None, edge=None, element1='C',
                 element2='C', bond=CCbond, nlayers=1, layer_spacing=dVDW,
                 layer_rotation_angles=None, stacking_order='AB',
                 verbose=False):

        self._length = length
        self._width = width
        if edge in ('armchair', 'zigzag'):
            edge = edge_types[edge]
        elif edge not in ('AC', 'ZZ'):
            print('unrecognized edge parameter: {}\n'.format(edge) +
                  'choosing one at random...\n')
            edge = np.random.choice(['AC', 'ZZ'])
            print('the randomly chosen edge type is: {}'.format(edge))
        self._edge = edge

        self._element1 = element1
        self._element2 = element2

        if bond is None:
            bond = CCbond

        self._bond = bond

        self._verbose = verbose

        self._Nx = 0
        self._Ny = 0

        self._layer_mass = None
        self._Natoms = 0
        self._Natoms_per_layer = None

        self._nlayers = nlayers
        self._layer_spacing = layer_spacing
        self._layer_rotation_angles = layer_rotation_angles
        self._stacking_order = stacking_order

        self._layer_shift = Vector()

        if nlayers > 1 and stacking_order == 'AB':
            if edge == 'AC':
                self._layer_shift.y = self._bond
            else:
                self._layer_shift.x = self._bond

        if edge == 'AC':
            # Set up the unit cell with the armchair edge aligned
            # along the `y`-axis.
            self._cell.x = np.sqrt(3) * bond
            self._cell.y = 3 * bond
        else:
            # Set up the unit cell with the zigzag edge aligned
            # along the `y`-axis.
            self._cell.x = 3 * bond
            self._cell.y = np.sqrt(3) * bond

        self._Nx = int(np.ceil(10 * self._width / self._cell.x))
        self._Ny = int(np.ceil(10 * self._length / self._cell.y))

    def __repr__(self):
        retstr = 'Graphene(length={!r}, width={!r}, edge={!r}, ' + \
            'element1={!r}, element2={!r}, bond={!r}, nlayers={!r}, ' + \
            'layer_spacing={!r}, layer_rotation_angles={!r}, ' + \
            'stacking_order={!r})'
        return retstr.format(self.length, self.width, self.edge, self.element1,
                             self.element2, self.bond, self.nlayers,
                             self.layer_spacing, self.layer_rotation_angles,
                             self.stacking_order)

    def compute_layer_params(self):
        pass

    @property
    def Natoms(self):
        """Number of :class:`~sknano.core.atoms.Atom`\ s in
        **unit cell**."""
        return self._Natoms

    @property
    def Natoms_per_layer(self):
        """Number of :class:`~sknano.core.atoms.Atom`\ s in
        **layer**."""
        return self._Natoms_per_layer

    @classmethod
    def compute_Natoms_per_layer(cls, n=None, m=None, element1=None,
                                 element2=None, **kwargs):
        return 0

    @property
    def length(self):
        """Graphene layer length in **nanometers**."""
        return self._length

    @length.setter
    def length(self, value):
        """Set graphene layer length in **nanometers**."""
        self._length = value
        self.compute_layer_params()

    @property
    def width(self):
        """Graphene layer width in **nanometers**."""
        return self._width

    @width.setter
    def width(self, value):
        """Set graphene layer width in **nanometers**."""
        self._width = value
        self.compute_layer_params()

    @property
    def bond(self):
        """Bond length in **Angstroms**."""
        return self._bond

    @bond.setter
    def bond(self, value):
        """Set bond length in **Angstroms**."""
        self._bond = float(value)
        self.compute_layer_params()

    @property
    def edge(self):
        """Graphene edge type along length."""
        return self._edge

    @edge.setter
    def edge(self, value):
        """Set Graphene edge type along length."""
        self._edge = value
        self.compute_layer_params()

    @property
    def element1(self):
        """Element symbol of :class:`~sknano.core.atoms.Atom` 1."""
        return self._element1

    @element1.setter
    def element1(self, value):
        """Set element symbol of :class:`~sknano.core.atoms.Atom` 1."""
        self._element1 = value
        self.compute_layer_params()

    @property
    def element2(self):
        """Element symbol of :class:`~sknano.core.atoms.Atom` 2."""
        return self._element2

    @element2.setter
    def element2(self, value):
        """Set element symbol of :class:`~sknano.core.atoms.Atom` 2."""
        self._element2 = value
        self.compute_layer_params()

    @property
    def layer_mass(self):
        """Graphene layer mass in grams."""
        return self._layer_mass

    @property
    def nlayers(self):
        return self._nlayers

    @nlayers.setter
    def nlayers(self, value):
        self._nlayers = value

    @property
    def layer_spacing(self):
        return self._layer_spacing

    @layer_spacing.setter
    def layer_spacing(self, value):
        self._layer_spacing = value

    @property
    def layer_rotation_angles(self):
        return self._layer_rotation_angles

    @layer_rotation_angles.setter
    def layer_rotation_angles(self, value):
        self._layer_rotation_angles = value

    @classmethod
    def compute_layer_mass(cls, n=None, m=None, width=None, length=None,
                           edge=None, element1=None, element2=None):
        """Compute graphene layer mass in **grams**.

        Parameters
        ----------
        n, m : int, optional
        width, length : float, optional
        edge : {'AC', 'ZZ'}
        element1, element2 : str, optional

        Returns
        -------
        mass : float

        """
        Natoms_per_layer = Graphene.compute_Natoms_per_layer(
            n=n, m=m, element1=element1, element2=element2)

        if element1 is None:
            element1 = 'C'
        if element2 is None:
            element2 = 'C'

        atom1 = Atom(element1)
        atom2 = Atom(element2)

        mass = Natoms_per_layer * (atom1.m + atom2.m) / 2

        return mass


class BilayerGraphene(Graphene):
    def __init__(self, layer_rotation_angle=None, deg2rad=True, **kwargs):

        if layer_rotation_angle is not None and deg2rad:
            layer_rotation_angle = np.radians(layer_rotation_angle)
        kwargs['layer_rotation_angles'] = layer_rotation_angle
        kwargs['nlayers'] = 2

        super(BilayerGraphene, self).__init__(**kwargs)
        self._layer_rotation_angle = self._layer_rotation_angles

    @property
    def layer_rotation_angle(self):
        return self._layer_rotation_angle

    @layer_rotation_angle.setter
    def layer_rotation_angle(self, value):
        self._layer_rotation_angle = value