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
        for data in (
            ("203.0.113.128", "a IPv4 test net address"),
            ("2000::", "A 6 characts short IPv6 address"),
            ("192.0.2.192", "another IPv4 test net address"),
            ("fe80::abcd", "an IPv6 link-local address"),
            ("10.123.45.67", "A private IPv4 address"),
            ("2001:db8:abcd::1234", "An IPv6 address in doc range"),
        ):
            with self.subTest(data=data):
                no_previous_supernet = False
                try:
                    address_space.describe(
                        ip_parameter=data[0],
                        description=data[1],
                    )
                except StrictSupernetError:
                    no_previous_supernet = True
                self.assertTrue(
                    no_previous_supernet,
                    "If strict address space, can describe address only "
                    "if supernet already exists",
                )

    def test_delegated_network_no_empty_arguments(self):
        """New delegated network method with no empty argument list."""
        for strict in (False, True):
            with self.subTest(strict=strict):
                address_space = AddressSpace(strict=strict)
                no_empty_arguments = False
                try:
                    address_space.describe_new_delegated_network()
                except TypeError:
                    no_empty_arguments = True
                self.assertTrue(
                    no_empty_arguments,
                    "Empty arguments should not be accepted in "
                    "describe_new_delegated_network",
                )

    def test_delegated_network_keyword_only_no_positional_args(self):
        """New delegated network must use keyword-only args."""
        for strict in (False, True):
            with self.subTest(strict=strict):
                address_space = AddressSpace(strict=strict)
                no_positional_arguments = False
                try:
                    address_space.describe_new_delegated_network(
                        "2001:db8::/32", "IPv6 documentation network space"
                    )
                except TypeError:
                    no_positional_arguments = True
                self.assertTrue(
                    no_positional_arguments,
                    "No positional argument should be accepted in "
                    "describe_new_delegated_network",
                )
