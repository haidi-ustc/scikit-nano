# -*- coding: utf-8 -*-
"""
============================================================================
Base class for structure data atom (:mod:`sknano.core._atom`)
============================================================================

.. currentmodule:: sknano.core._atom

"""
from __future__ import absolute_import, division, print_function
__docformat__ = 'restructuredtext en'

from collections import OrderedDict

import numpy as np

from .refdata import atomic_masses, atomic_mass_symbol_map, \
    atomic_numbers, atomic_number_symbol_map, element_symbols
from ._luts import xyz
from ._npcoremath import Point

__all__ = ['Atom']


class Atom(object):
    """Base class for structure data atom.

    Parameters
    ----------
    element : {str, int}, optional
        A string representation of the element symbol or an integer specifying
        an element atomic number :math:`\\boldsymbol{Z}`.
    x, y, z : float, optional
        :math:`x, y, z` coordinates of `Atom`.

    """

    def __init__(self, element=None, m=None, x=None, y=None, z=None):

        self._r = Point(np.array([x, y, z]))
        #self._dr = Vector(np.zeros(3))

        self._m = None
        self._symbol = None
        self._Z = None

        if isinstance(element, (int, float)):
            self._Z = int(element)
            idx = self._Z - 1
            try:
                self._symbol = element_symbols[idx]
                self._m = atomic_masses[self._symbol]
            except KeyError:
                print('unrecognized element number: {}'.format(element))
        elif isinstance(element, (str, unicode)):
            self._symbol = element
            try:
                self._Z = atomic_numbers[self._symbol]
                self._m = atomic_masses[self._symbol]
            except KeyError:
                print('Unrecognized atomic symbol: {}'.format(element))
        else:
            self._symbol = None
            self._Z = None
            if m is not None and isinstance(m, (int, float)):
                try:
                    if isinstance(m, float):
                        self._symbol = atomic_mass_symbol_map[m]
                    elif isinstance(m, int):
                        self._symbol = atomic_number_symbol_map[int(m / 2)]
                    self._Z = atomic_numbers[self._symbol]
                    self._m = atomic_masses[self._symbol]
                except KeyError:
                    self._symbol = None
                    self._Z = None
                    self._m = m
            else:
                self._m = 0

        self._attributes = ['symbol', 'Z', 'm', 'r']

    def __repr__(self):
        """Return string representation of atom."""
        return "Atom(element={!r}, m={!r}, x={!r}, y={!r}, z={!r})".format(
            self.element, self.m, self.x, self.y, self.z)

    @property
    def Z(self):
        """Atomic number :math:`Z`.

        Returns
        -------
        int
            Atomic number :math:`Z`.
        """
        return self._Z

    @property
    def element(self):
        """Element symbol.

        Returns
        -------
        str
            Element symbol.
        """
        return self.symbol

    @property
    def symbol(self):
        """Element symbol.

        Returns
        -------
        str
            Element symbol.
        """
        return self._symbol

    @property
    def m(self):
        """Atomic mass :math:`m_a` in atomic mass units.

        Returns
        -------
        float
            Atomic mass :math:`m_a` in atomic mass units.
        """
        return self._m

    @property
    def x(self):
        """:math:`x`-coordinate in units of **Angstroms**.

        Returns
        -------
        float
            :math:`x`-coordinate in units of **Angstroms**.

        """
        return self._r.x

    @x.setter
    def x(self, value=float):
        """Set `Atom` :math:`x`-coordinate in units of **Angstroms**.

        Parameters
        ----------
        value : float
            :math:`x`-coordinate in units of **Angstroms**.

        """
        self._r.x = value

    @property
    def y(self):
        """:math:`y`-coordinate in units of **Angstroms**.

        Returns
        -------
        float
            :math:`y`-coordinate in units of **Angstroms**.

        """
        return self._r.y

    @y.setter
    def y(self, value=float):
        """Set `Atom` :math:`y`-coordinate in units of **Angstroms**.

        Parameters
        ----------
        value : float
            :math:`y`-coordinate in units of **Angstroms**.

        """
        self._r.y = value

    @property
    def z(self):
        """:math:`z`-coordinate in units of **Angstroms**.

        Returns
        -------
        float
            :math:`z`-coordinate in units of **Angstroms**.

        """
        return self._r.z

    @z.setter
    def z(self, value=float):
        """Set `Atom` :math:`z`-coordinate in units of **Angstroms**.

        Parameters
        ----------
        value : float
            :math:`z`-coordinate in units of **Angstroms**.

        """
        self._r.z = value

    @property
    def r(self):
        """:math:`x, y, z` coordinates of `Atom` in units of **Angstroms**.

        Returns
        -------
        ndarray
            3-element ndarray of [:math:`x, y, z`] coordinates of `Atom`.

        """
        return self._r

    @r.setter
    def r(self, value=np.ndarray):
        """Set :math:`x, y, z` coordinates of `Atom`.

        Parameters
        ----------
        value : array_like
            3-element array of :math:`x, y, z`-coordinates in units of
            **Angstroms**.

        """
        self._r = value

    def get_coords(self, as_dict=False):
        """Return atom coords.

        Parameters
        ----------
        as_dict : bool, optional

        Returns
        -------
        coords : :py:class:`python:~collections.OrderedDict` or ndarray

        """
        coords = self.r
        if as_dict:
            return OrderedDict(zip(xyz, self.r))
        else:
            return coords

    def rezero_coords(self, epsilon=1.0e-10):
        """Re-zero position coordinates near zero.

        Set position coordinates with absolute value less than `epsilon` to
        zero.

        Parameters
        ----------
        epsilon : float
            smallest allowed absolute value of any :math:`x,y,z` component.

        """
        self._r.rezero_coords(epsilon=epsilon)