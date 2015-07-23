Information
===========

This module was created to side-step a circular import situation when
the original interfaces module was needed by subclasses, which also
needed to be imported back into this original interface location.

External packages that require the core interfaces should not import
from here for future compatibility.
