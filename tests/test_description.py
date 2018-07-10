#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for description methods of pppipam.AddressSpace instances."""

import unittest
from pppipam.pppipam import AddressSpace


class AddressSpace_description_TestCase(unittest.TestCase):
    """Tests for description related methods."""

    def setUp(self):
        """Set up test fixtures with new AddressSpace."""
        self.address_space = AddressSpace()

    def test_address_space_as_AddressSpace(self):
        """Validate if address_space is instance of AddressSpace."""
        self.assertIsInstance(self.address_space, AddressSpace)

    def test_describe_address(self):
        """Add valid IP address with non-empty str description."""
        pass
