# -*- coding: utf-8 -*-
"""
===============================================================================
Mixin crystallography classes (:mod:`sknano.core.crystallography._mixins`)
===============================================================================

.. currentmodule:: sknano.core.crystallography._mixins

"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals
# from builtins import object
# from builtins import super
# from future.utils import with_metaclass

__docformat__ = 'restructuredtext en'

# from abc import ABCMeta, abstractproperty
# from enum import Enum

from sknano.core.math import Point

import numpy as np

__all__ = ['DirectLatticeMixin', 'ReciprocalLatticeMixin', 'UnitCellMixin',
           'Direct2DLatticeMixin', 'Direct3DLatticeMixin',
           'Reciprocal2DLatticeMixin', 'Reciprocal3DLatticeMixin']


class Direct2DLatticeMixin:
    """Mixin class for computing the 2D direct lattice parameters from \
        2D reciprocal lattice parameters."""
    @property
    def cos_gamma(self):
        """:math:`\\cos\\gamma`"""
        return np.around(np.acos(np.radians(self.gamma)), decimals=6)

    @property
    def sin_gamma(self):
        """:math:`\\sin\\gamma`"""
        return np.sqrt(1 - self.cos_gamma ** 2)

    @property
    def a1(self):
        """Lattice vector :math:`\\mathbf{a}_1=\\mathbf{a}`."""
        return self.b2.cross(self.b3) / self.cell_volume

    @property
    def a2(self):
        """Lattice vector :math:`\\mathbf{a}_2=\\mathbf{b}`."""
        return self.b3.cross(self.b1) / self.cell_volume


class Reciprocal2DLatticeMixin:
    """Mixin class for computing the 2D reciprocal lattice parameters from \
        2D direct lattice parameters."""
    @property
    def cos_gamma_star(self):
        """:math:`\\cos\\gamma^*`"""
        return np.around(np.acos(np.radians(self.gamma_star)), decimals=6)

    @property
    def sin_gamma_star(self):
        """:math:`\\sin\\gamma^*`"""
        return np.sqrt(1 - self.cos_gamma_star ** 2)

    @property
    def b1(self):
        """Reciprocal lattice vector :math:`\\mathbf{b}_1=\\mathbf{a}^{*}`."""
        return self.a2.cross(self.a3) / self.cell_volume

    @property
    def b2(self):
        """Reciprocal lattice vector :math:`\\mathbf{b}_2=\\mathbf{b}^{*}`."""
        return self.a3.cross(self.a1) / self.cell_volume


class Direct3DLatticeMixin:
    """Mixin class for computing the 3D direct lattice parameters from \
        reciprocal lattice parameters."""
    @property
    def cos_alpha(self):
        """:math:`\\cos\\alpha`"""
        return np.around(
            (self.cos_beta_star * self.cos_gamma_star - self.cos_alpha_star) /
            (self.sin_beta_star * self.sin_gamma_star), decimals=6)

    @property
    def cos_beta(self):
        """:math:`\\cos\\beta`"""
        return np.around(
            (self.cos_gamma * self.cos_alpha - self.cos_beta) /
            (self.sin_gamma * self.sin_alpha), decimals=6)

    @property
    def cos_gamma(self):
        """:math:`\\cos\\gamma`"""
        return np.around(
            (self.cos_alpha_star * self.cos_beta_star - self.cos_gamma_star) /
            (self.sin_alpha_star * self.sin_beta_star), decimals=6)

    @property
    def sin_alpha(self):
        """:math:`\\sin\\alpha`"""
        return np.sqrt(1 - self.cos_alpha ** 2)

    @property
    def sin_beta(self):
        """:math:`\\sin\\beta`"""
        return np.sqrt(1 - self.cos_beta ** 2)

    @property
    def sin_gamma(self):
        """:math:`\\sin\\gamma`"""
        return np.sqrt(1 - self.cos_gamma ** 2)

    @property
    def a1(self):
        """Lattice vector :math:`\\mathbf{a}_1=\\mathbf{a}`."""
        return self.b2.cross(self.b3) / self.cell_volume

    @property
    def a2(self):
        """Lattice vector :math:`\\mathbf{a}_2=\\mathbf{b}`."""
        return self.b3.cross(self.b1) / self.cell_volume

    @property
    def a3(self):
        """Lattice vector :math:`\\mathbf{a}_3=\\mathbf{c}`."""
        return self.b1.cross(self.b2) / self.cell_volume

DirectLatticeMixin = Direct3DLatticeMixin


class Reciprocal3DLatticeMixin:
    """Mixin class for computing the 3D reciprocal lattice parameters from \
        the direct lattice parameters."""
    @property
    def cos_alpha_star(self):
        """:math:`\\cos\\alpha^*`"""
        return np.around((self.cos_beta * self.cos_gamma - self.cos_alpha) /
                         (self.sin_beta * self.sin_gamma), decimals=6)

    @property
    def cos_beta_star(self):
        """:math:`\\cos\\beta^*`"""
        return np.around((self.cos_gamma * self.cos_alpha - self.cos_beta) /
                         (self.sin_gamma * self.sin_alpha), decimals=6)

    @property
    def cos_gamma_star(self):
        """:math:`\\cos\\gamma^*`"""
        return np.around((self.cos_alpha * self.cos_beta - self.cos_gamma) /
                         (self.sin_alpha * self.sin_beta), decimals=6)

    @property
    def sin_alpha_star(self):
        """:math:`\\sin\\alpha^*`"""
        return np.sqrt(1 - self.cos_alpha_star ** 2)

    @property
    def sin_beta_star(self):
        """:math:`\\sin\\beta^*`"""
        return np.sqrt(1 - self.cos_beta_star ** 2)

    @property
    def sin_gamma_star(self):
        """:math:`\\sin\\gamma^*`"""
        return np.sqrt(1 - self.cos_gamma_star ** 2)

    @property
    def b1(self):
        """Reciprocal lattice vector :math:`\\mathbf{b}_1=\\mathbf{a}^{*}`."""
        return self.a2.cross(self.a3) / self.cell_volume

    @property
    def b2(self):
        """Reciprocal lattice vector :math:`\\mathbf{b}_2=\\mathbf{b}^{*}`."""
        return self.a3.cross(self.a1) / self.cell_volume

    @property
    def b3(self):
        """Reciprocal lattice vector :math:`\\mathbf{b}_3=\\mathbf{c}^{*}`."""
        return self.a1.cross(self.a2) / self.cell_volume

ReciprocalLatticeMixin = Reciprocal3DLatticeMixin


class UnitCellMixin:
    """Mixin class for lattice unit cell."""
    @property
    def cell_matrix(self):
        """Matrix of `CrystalLattice` lattice row vectors. \
            Same as :attr:`CrystalLattice.ortho_matrix`\ .T."""
        return self.ortho_matrix.T

    @property
    def fractional_matrix(self):
        """Transformation matrix to convert from cartesian coordinates to \
            fractional coordinates."""
        return np.linalg.inv(self.ortho_matrix)

    @property
    def metric_tensor(self):
        """Metric tensor."""
        return self.ortho_matrix * self.ortho_matrix.T

    def fractional_to_cartesian(self, p):
        """Convert fractional coordinate to cartesian coordinate.

        Parameters
        ----------
        p : `Point`

        Returns
        -------
        `Point`

        """
        p = Point(p)
        c = self.orientation_matrix * self.ortho_matrix * \
            p.column_matrix + self.offset.column_matrix
        return p.__class__(c.A.flatten())

    def cartesian_to_fractional(self, p):
        """Convert cartesian coordinate to fractional coordinate.

        Parameters
        ----------
        p : `Point`

        Returns
        -------
        `Point`

        """
        p = Point(p)
        f = self.fractional_matrix * np.linalg.inv(self.orientation_matrix) * \
            (p - self.offset).column_matrix
        return p.__class__(f.A.flatten())

    def wrap_fractional_coordinate(self, p, epsilon=1e-6):
        """Wrap fractional coordinate to lie within unit cell.

        Parameters
        ----------
        p : `Point`

        Returns
        -------
        `Point`

        """
        p = Point(p)
        p = np.fmod(p, 1)
        p[np.where(p.__array__() < 0)] += 1
        p[np.where(p.__array__() > 1 - epsilon)] -= 1
        p[np.where(np.logical_or(
                   (p.__array__() > 1 - epsilon),
                   (p.__array__() < epsilon)))] = 0
        return p

    def wrap_cartesian_coordinate(self, p):
        """Wrap cartesian coordinate to lie within unit cell.

        Parameters
        ----------
        p : `Point`

        Returns
        -------
        `Point`

        """
        return self.fractional_to_cartesian(
            self.wrap_fractional_coordinate(
                self.cartesian_to_fractional(p)))