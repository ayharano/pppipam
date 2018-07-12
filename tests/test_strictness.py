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

    def test_address_space_strict_cannot_be_assigned_to(self):
        """AddressSpace's strict member cannot be assigned."""
        address_space = AddressSpace()
        cannot_be_assigned = False
        try:
            address_space.strict = False
        except AttributeError:
            cannot_be_assigned = True
        self.assertTrue(
            cannot_be_assigned,
            "AddressSpace instance' strict cannot be assigned",
        )

    def test_address_space_default_strict_should_be_true(self):
        """Default value for AddressSpace's strict member should be True."""
        address_space = AddressSpace()
        self.assertIs(
            address_space.strict,
            True,
            "AddressSpace's default strict value expected to be True.",
        )
