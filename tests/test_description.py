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

    def test_describe_keyword_only_no_empty_arguments(self):
        """describe method as keyword only, without default parameters."""
        no_empty_arguments = False
        try:
            self.address_space.describe()
        except TypeError:
            no_empty_arguments = True
        self.assertTrue(
            no_empty_arguments,
            "Empty arguments should not be accepted in describe",
        )

    def test_describe_keyword_only_no_positional_arguments(self):
        """describe method as keyword only, without positional parameters."""
        no_positional_arguments = False
        try:
            self.address_space.describe("203.0.113.128", "test net address")
        except TypeError:
            no_positional_arguments = True
        self.assertTrue(
            no_positional_arguments,
            "No positional argument should be accepted in describe",
        )

    def test_describe_address(self):
        """Add valid IP address with non-empty str description."""
        self.assertIs(
            self.address_space.describe(
                address='123.123.123.123',
                description="123 is nice"
            ),
            True,
        )
        self.assertIs(
            self.address_space.describe(
                address='203.0.113.129',
                description="Second subnet gateway"
            ),
            True,
        )
        self.assertIs(
            self.address_space.describe(
                address='192.0.2.123',
                description="123 is nice, test net"
            ),
            True,
        )
        self.assertIs(
            self.address_space.describe(
                address='2001:db8::abcd:ef12',
                description="ipv6 doc address"
            ),
            True,
        )
        self.assertIs(
            self.address_space.describe(
                address='2000::',
                description="first global address for now"
            ),
            True,
        )
        self.assertIs(
            self.address_space.describe(
                address='fe80::',
                description="even link-local?"
            ),
            True,
        )
