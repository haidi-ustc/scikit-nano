# -*- coding: utf-8 -*-
"""
==============================================================================
Base structure classes (:mod:`sknano.structures._base`)
==============================================================================

.. currentmodule:: sknano.structures._base

"""
from __future__ import absolute_import, division, print_function
__docformat__ = 'restructuredtext en'

import numbers

from sknano.core.refdata import CCbond

__all__ = ['StructureBase']


class StructureBase(object):
    u"""Base class for creating interactive nanostructure objects.

    Parameters
    ----------
    n, m : int
        Chiral indices defining the nanotube chiral vector
        :math:`\\mathbf{C}_h = n\\mathbf{a}_1 + m\\mathbf{a}_2 = (n, m)`.
    element1, element2 : {str, int}, optional
        Element symbol or atomic number of basis
        :class:`~sknano.core.atoms.Atom` 1 and 2
    bond : float, optional
        Distance between nearest neighbor atoms (i.e., bond length).
        Must be in units of **\u212b**. Default value is
        the carbon-carbon bond length in graphite, approximately
        :math:`\\mathrm{a}_{\\mathrm{CC}} = 1.42` \u212b

    """
    def __init__(self, element1='C', element2='C', bond=CCbond, verbose=False,
                 **kwargs):

        self.element1 = element1
        self.element2 = element2

        if bond is None:
            bond = CCbond

        self.bond = bond
        self.verbose = verbose

        super(StructureBase, self).__init__(**kwargs)

    @property
    def bond(self):
        u"""Bond length in **\u212b**."""
        return self._bond

    @bond.setter
    def bond(self, value):
        u"""Set bond length in **\u212b**."""
        if not (isinstance(value, numbers.Real) or value > 0):
            raise TypeError('Expected a real, positive number.')
        self._bond = float(value)

    @bond.deleter
    def bond(self):
        del self._bond

    @property
    def element1(self):
        """Element symbol of :class:`~sknano.core.atoms.Atom` 1."""
        return self._element1

    @element1.setter
    def element1(self, value):
        """Set element symbol of :class:`~sknano.core.atoms.Atom` 1."""
        self._element1 = value

    @element1.deleter
    def element1(self):
        del self._element1

    @property
    def element2(self):
        """Element symbol of :class:`~sknano.core.atoms.Atom` 2."""
        return self._element2

    @element2.setter
    def element2(self, value):
        """Set element symbol of :class:`~sknano.core.atoms.Atom` 2."""
        self._element2 = value

    @element2.deleter
    def element2(self):
        del self._element2