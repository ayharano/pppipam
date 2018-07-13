#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests related to enforce pppipam.AddressSpace' strictness (default)."""

import dataclasses
import unittest

from pppipam.pppipam import (
    AddressSpace, StrictSupernetError, SameDelegationAsNewError
)


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
        address_space = AddressSpace(strict_=True)
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
                address_space = AddressSpace(strict_=strict)
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
                address_space = AddressSpace(strict_=strict)
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

    def test_delegated_network_into_address_space(self):
        """Inserts a network without supernet present in address space."""
        for strict in (False, True):
            with self.subTest(strict_=strict):
                address_space = AddressSpace(strict_=strict)
                for data in (
                    ("2001:db8::/32", "IPv6 documentation network space"),
                    ("203.0.113.0/24", "one of IPv4 test net"),
                    ("fdab:cdef:1234::/48", "an IPv6 unique-local net"),
                    ("192.0.2.0/24", "another IPv4 test net"),
                    ("::/0", "whole IPv6 address space"),
                    ("0.0.0.0/0", "whole IPv4 address space"),
                ):
                    with self.subTest(data=data):
                        self.assertTrue(
                            address_space.describe_new_delegated_network(
                                network_parameter=data[0],
                                description=data[1],
                            ),
                            "Describe a network without a previous inserted "
                            "supernet",
                        )

    def test_delegated_network_cannot_describe_subnet_as_new(self):
        """Inserting delegation with present supernet must raise exception."""
        for strict in (False, True):
            with self.subTest(strict=strict):
                address_space = AddressSpace(strict_=strict)
                for data in (
                    ("2001:db8::/32", "2001:db8::/48"),
                    ("203.0.113.0/24", "203.0.113.0/27"),
                    ("fdab:cdef:1234::/48", "fdab:cdef:1234:5678::/64"),
                    ("192.0.2.0/24", "192.0.2.128/26"),
                    ("::/0", "::ab00/126"),
                    ("0.0.0.0/0", "10.0.0.0/8"),
                ):
                    with self.subTest(data=data):
                        self.assertTrue(
                            address_space.describe_new_delegated_network(
                                network_parameter=data[0],
                                description="actual delegation",
                            ),
                            "Describe a network without a previous inserted "
                            "supernet",
                        )
                        supernet_detected = False
                        try:
                            address_space.describe_new_delegated_network(
                                network_parameter=data[1],
                                description="trying subnet as delegated",
                            )
                        except StrictSupernetError:
                            supernet_detected = True
                        self.assertTrue(
                            supernet_detected,
                            "If inserting delegated network, no supernet "
                            "should be present, for strict and non strict "
                            "address spaces"
                        )

    def test_delegated_network_cannot_insert_same_as_new(self):
        """Inserting delegation with same net must raise exception."""
        for net in (
            "2001:db8::/32", "2001:db8::/48", "203.0.113.0/24",
            "203.0.113.0/27", "fdab:cdef:1234::/48",
            "fdab:cdef:1234:5678::/64", "192.0.2.0/24",
            "192.0.2.128/26", "::/0", "::ab00/126",
            "0.0.0.0/0", "10.0.0.0/8",
        ):
            with self.subTest(net=net):
                for strict in (False, True):
                    with self.subTest(strict=strict):
                        address_space = AddressSpace(strict_=strict)
                        self.assertTrue(
                            address_space.describe_new_delegated_network(
                                network_parameter=net,
                                description="actual delegation",
                            ),
                            "Describe a network without a previous inserted "
                            "supernet",
                        )
                        same_net = False
                        try:
                            address_space.describe_new_delegated_network(
                                network_parameter=net,
                                description="trying to insert same as new",
                            )
                        except SameDelegationAsNewError:
                            same_net = True
                        self.assertTrue(
                            same_net,
                            "Cannot insert same delegation as new more than "
                            "once",
                        )

    def test_address_space_cannot_describe_net_if_no_previous_supernet(self):
        """A network can only be described if a supernet exists."""
        address_space = AddressSpace(strict_=True)
        for data in (
            ("203.0.113.0/24", "an IPv4 test net"),
            ("2000::/3", "Current loose global IPv6 network"),
            ("192.0.2.0/24", "another IPv4 test net"),
            ("fe80::/64", "IPv6 link-local network"),
            ("10.123.0.0/16", "A private IPv4 address"),
            ("2001:db8:ab00::/40", "An IPv6 network in doc range"),
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
                    "If strict address space, can describe networks only "
                    "if supernet already exists",
                )
