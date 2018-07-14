PPPIPAM: Poor Person's Python IP Address Manager
===================================================

[![image - version](https://img.shields.io/pypi/v/pppipam.svg)](https://pypi.python.org/pypi/pppipam)

[![image - License: MIT](https://img.shields.io/pypi/l/pppipam.svg)](https://pypi.python.org/pypi/pppipam)

[![image - Python versions](https://img.shields.io/pypi/pyversions/pppipam.svg)](https://pypi.python.org/pypi/pppipam)

------------------------------------------------------------------------

**PPPIPAM** is a distribution package to provide a single IP address space manager for both IPv4 and IPv6 as a Python module for developers.


Installation
-----------

*PPPIPAM* can be installed using `pip`. It requires Python 3.7.0+ to use.

    $ pip install pppipam



Usage
-----------

    >>> from pppipam import AddressSpace



Features
--------

-   Single address space manager for both IPv4 and IPv6 networks and addresses.
-   Strict or loose address space description (if strict, must add delegated networks first).
-   Deleting IP objects can be done in cascade (e.g. removing a described network can remove all subnets and address).
-   Data can be exported as a `dict` containing all described IP instances and a nested network information according to address space's version.


Constraints
-----------

-   Source code must use only Python language and Python Standard Library.
