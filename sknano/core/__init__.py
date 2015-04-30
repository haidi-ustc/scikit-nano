# -*- coding: utf-8 -*-
"""
===============================================================================
Core package code (:mod:`sknano.core`)
===============================================================================

.. currentmodule:: sknano.core

Contents
========
Core code for package development and general use.

Functions
----------

Iterator functions:

.. autosummary::
   :toctree: generated/

   cyclic_pairs
   take
   tabulate
   consume
   nth
   quantify
   padnone
   ncycles
   dotproduct
   flatten
   repeatfunc
   pairwise
   grouper
   roundrobin
   partition
   powerset
   unique_everseen
   unique_justseen
   iter_except
   first_true
   random_product
   random_permutation
   random_combination
   random_combination_with_replacement


Array functions:

.. autosummary::
   :toctree: generated/

   rezero_array

Meta functions/classes:

.. autosummary::
   :toctree: generated/

   check_type
   deprecated
   get_object_signature
   memoize
   method_function
   timethis
   methodfunc
   with_doc

I/O functions:

.. autosummary::
   :toctree: generated/

   get_fname
   get_fpath

String functions:

.. autosummary::
   :toctree: generated/

   pluralize

Classes
-------

.. autosummary::
   :toctree: generated/

   UserList

Sub-packages
-------------

* atoms (:mod:`sknano.core.atoms`)
* crystallography (:mod:`sknano.core.crystallography`)
* math (:mod:`sknano.core.math`)
* molecules (:mod:`sknano.core.molecules`)
* physics (:mod:`sknano.core.physics`)
* refdata (:mod:`sknano.core.refdata`)

"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals
__docformat__ = 'restructuredtext en'

from ._collections import *
from ._extras import *
from ._io import *
from ._itertools import *
from ._meta import *
from ._strings import *

__all__ = [s for s in dir() if not s.startswith('_')]
