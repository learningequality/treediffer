Doctests walkthrough
====================


.. testsetup:: *

   import re
   import treediffer

The parrot module is a module about parrots.

Doctest example:

.. doctest::

   >>> 'Title Case'.lower()
   'title case'

Test-Output example:

.. doctest::

   'lower case'.upper()
   'LOWER CASE'


