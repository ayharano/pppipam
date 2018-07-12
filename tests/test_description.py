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
        for parameters in (
            ('123.123.123.123', "123 is nice"),
            ('203.0.113.129', "Second subnet gateway"),
            ('192.0.2.123', "123 is nice, test net"),
            ('2001:db8::abcd:ef12', "ipv6 doc address"),
            ('2000::', "first global address for now"),
            ('fe80::', "even link-local?"),
        ):
            with self.subTest(parameters=parameters):
                self.assertIs(
                    self.address_space.describe(
                        ip_parameter=parameters[0],
                        description=parameters[1],
                    ),
                    True,
                )

    def test_describe_network(self):
        """Add valid IP network with non-empty str description."""
        for parameters in (
                ("10.0.0.0/16", "a private IPv4 network"),
                ("203.0.113.128/25", "part of a test net"),
                ("0.0.0.0/0", "whole IPv4 address space as network"),
                ("2001:db8:1234:5678::/64", "a documentation IPv6 network"),
                ("fe80::/64", "IPv6 link-local network"),
                ("fd01:2345:6789::/48",
                 "a ~random~ IPv6 unique-local network"),
                ("::/0", "whole IPv6 address space as network"),
        ):
            with self.subTest(parameters=parameters):
                self.assertIs(
                    self.address_space.describe(
                        description=parameters[1],
                        ip_parameter=parameters[0],
                    ),
                    True,
                )

    def test_describe_ip_parameter_not_valid_typeerror(self):
        """Invalid IP parameter should raise TypeError."""
        invalid_ip_parameter = False
        try:
            self.address_space.describe(
                description="parameter as none",
                ip_parameter=None,
            )
        except TypeError:
            invalid_ip_parameter = True
        self.assertTrue(
            invalid_ip_parameter,
            "Invalid IP parameter should raise TypeError"
        )
        invalid_ip_parameter = False
        try:
            self.address_space.describe(
                description="parameter as non-zero int",
                ip_parameter=123,
            )
        except TypeError:
            invalid_ip_parameter = True
        self.assertTrue(
            invalid_ip_parameter,
            "Invalid IP parameter should raise TypeError"
        )

    def test_describe_description_not_str_typeerror(self):
        """Non-str description should raise TypeError."""
        for non_str in (None, 123, set([1, 2, 3])):
            with self.subTest(non_str=non_str):
                non_str_description = False
                try:
                    self.address_space.describe(
                        ip_parameter='123.123.123.123',
                        description=non_str,
                    )
                except TypeError:
                    non_str_description = True
                self.assertTrue(
                    non_str_description,
                    "Non str description should raise TypeError",
                )

    def test_describe_empty_str_valueerror(self):
        """Empty str description should raise ValueError."""
        empty_str_description = False
        try:
            self.address_space.describe(
                ip_parameter='123.123.123.123',
                description="",
            )
        except ValueError:
            empty_str_description = True
        self.assertTrue(
            empty_str_description,
            "Empty str description should raise ValueError",
        )
