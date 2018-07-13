#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests related to enforce pppipam.AddressSpace' strictness (default)."""

import dataclasses
import unittest

from pppipam.pppipam import AddressSpace, StrictSupernetError


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

    def test_address_space_init_cannot_accept_positional_arguments(self):
        """init method as keyword only, without positional parameters."""
        no_positional_arguments = False
        try:
            AddressSpace(False)
        except TypeError:
            no_positional_arguments = True
        self.assertTrue(
            no_positional_arguments,
            "No positional argument should be accepted in __init__",
        )

    def test_address_space_cannot_describe_address_if_no_previous_net(self):
        """An address can only be described if a supernet exists."""
        address_space = AddressSpace(strict=True)
        no_previous_supernet = False
        try:
            address_space.describe(
                ip_parameter="203.0.113.128",
                description="a IPv4 test net address",
            )
        except StrictSupernetError:
            no_previous_supernet = True
        self.assertTrue(
            no_previous_supernet,
            "If strict address space, can describe address only "
            "if supernet already exists",
        )
