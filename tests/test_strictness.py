#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests related to enforce pppipam.AddressSpace' strictness (default)."""

import dataclasses
import unittest

from pppipam.pppipam import AddressSpace


class AddressSpace_strictness_TestCase(unittest.TestCase):
    """Tests related to AddressSpace strictness."""

    def test_address_space_strict(self):
        """Retrieve AddressSpace's strict member."""
        address_space = AddressSpace()
        self.assertIsInstance(
            address_space.strict,
            bool,
            "AddressSpace instance expected to have "
            "a strict boolean member"
        )
