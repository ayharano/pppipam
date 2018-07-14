#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests related to data export of pppipam.AddressSpace."""

import ipaddress
import unittest

from pppipam.pppipam import AddressSpace


class AddressSpace_default_export_TestCase(unittest.TestCase):
    """Tests related to AddressSpace's data export."""

    def setUp(self):
        self.address_spaces = AddressSpace()

    def test_address_space_export_for_default_instance(self):
        """Default instance should evaluate to True."""
        exported_data = self.address_spaces.export_data()
        self.assertTrue(
            exported_data,
            "exported data should truth evaluate to True"
        )

    def test_address_space_export_for_default_instance_should_be_dict(self):
        """Default instance should return dict with default values."""
        exported_data = self.address_spaces.export_data()
        self.assertIsInstance(
            exported_data,
            dict,
            "exported data should be a dict"
        )

    def test_address_space_export_for_default_instance_should_have_keys(self):
        """Default instance should return dict with keys."""
        exported_data = self.address_spaces.export_data()
        for key in ("description", "nested_ip_object"):
            with self.subTest(key=key):
                self.assertIn(
                    key,
                    exported_data,
                    "exported data should have specific key"
                )

    def test_address_space_export_for_default_instance_exact_keys(self):
        """Default instance should return dict with keys."""
        exported_data = self.address_spaces.export_data()
        keys = set({"description", "nested_ip_object"})
        self.assertEqual(
            keys,
            set(exported_data),
            "exported data should have exactly required keys"
        )


class AddressSpace_more_data_export_TestCase(unittest.TestCase):
    """Actual-like data for AddressSpace's data export."""

    def setUp(self):
        """Export AddressSpace's data."""
        self.delegated_tuples = (
            ("2001:db8::/32", "IPv6 documentation network space"),
            ("203.0.113.0/24", "one of IPv4 test net"),
            ("fdab:cdef:1234::/48", "an IPv6 unique-local net"),
            ("192.0.2.0/24", "another IPv4 test net"),
        )
        self.subnet_tuples = (
            ("2001:db8::/48", "zeroed doc subnet"),
            ("2001:db8:1234::/48", "digit doc subnet"),
            ("2001:db8:abcd::/48", "letter doc subnet"),
            ("203.0.113.0/26", "a 1/4 test subnet"),
            ("203.0.113.128/27", "1/8 subnet"),
            ("fdab:cdef:1234:5678::/64", "digit unique local subnet"),
            ("fdab:cdef:1234:abcd::/64", "letter unique local subnet"),
            ("192.0.2.64/26", "another 1/4 test subnet"),
            ("192.0.2.128/25", "1/2 of a test subnet"),
        )
        self.address_tuples = (
            ("2001:db8:9876:5432:10::", "direct IPv6 doc address"),
            ("203.0.113.200", "direct address of a IPv4 test net"),
            ("fdab:cdef:1234:c001::abcd", "direct IPv6 unique-local address"),
            ("192.0.2.12", "direct address of another IPv4 test net"),
            ("2001:db8::123", "digit address of zeroed doc subnet"),
            ("2001:db8::abc", "letter address of zeroed doc subnet"),
            ("2001:db8:1234::abc:123", "mixed address of digit doc subnet"),
            ("2001:db8:1234::f00:ba", "letter address of digit doc subnet"),
            ("2001:db8:abcd:abcd::abcd", "abcd address of letter doc subnet"),
            ("2001:db8:abcd:1234:1234::", "1234 address of letter doc subnet"),
            ("203.0.113.0", "first address of a 1/4 test subnet"),
            ("203.0.113.63", "last address of a 1/4 test subnet"),
            ("203.0.113.130", " almost at begining of 1/8 subnet"),
            ("203.0.113.150", " almost at the end of 1/8 subnet"),
            ("fdab:cdef:1234:5678::1234:5678", "12345678 address"),
            ("fdab:cdef:1234:5678::abcd:abcd", "abcdabcd address"),
            ("fdab:cdef:1234:abcd::7654:321", "reverse number address"),
            ("fdab:cdef:1234:abcd::fe:dcba", "reverse letter address"),
            ("192.0.2.64", "first of another 1/4 test subnet"),
            ("192.0.2.127", "last of another 1/4 test subnet"),
            ("192.0.2.200", "200 of 1/2 of a test subnet"),
            ("192.0.2.234", "234 of 1/2 of a test subnet"),
        )

        self.exported = dict()
        exported_description = self.exported.setdefault("description", dict())
        for net_tuple in (*self.delegated_tuples, *self.subnet_tuples):
            as_network = ipaddress.ip_network(net_tuple[0])
            exported_description[as_network] = net_tuple[1]
        for address_tuple in self.address_tuples:
            as_address = ipaddress.ip_address(address_tuple[0])
            exported_description[as_address] = address_tuple[1]

        self.exported["nested_ip_objects"] = {
            4: {
                ipaddress.ip_network("203.0.113.0/24"): {
                    ipaddress.ip_address("203.0.113.200"): dict(),
                    ipaddress.ip_network("203.0.113.0/26"): {
                        ipaddress.ip_address("203.0.113.0"): dict(),
                        ipaddress.ip_address("203.0.113.63"): dict(),
                    },
                    ipaddress.ip_network("203.0.113.128/27"): {
                        ipaddress.ip_address("203.0.113.130"): dict(),
                        ipaddress.ip_address("203.0.113.150"): dict(),
                    },
                },
                ipaddress.ip_network("192.0.2.0/24"): {
                    ipaddress.ip_address("192.0.2.12"): dict(),
                    ipaddress.ip_network("192.0.2.64/26"): {
                        ipaddress.ip_address("192.0.2.64"): dict(),
                        ipaddress.ip_address("192.0.2.127"): dict(),
                    },
                    ipaddress.ip_network("192.0.2.128/25"): {
                        ipaddress.ip_address("192.0.2.200"): dict(),
                        ipaddress.ip_address("192.0.2.234"): dict(),
                    },
                },
            },
            6: {
                ipaddress.ip_network("2001:db8::/32"): {
                    ipaddress.ip_address("2001:db8:9876:5432:10::"): dict(),
                    ipaddress.ip_network("2001:db8::/48"): {
                        ipaddress.ip_address("2001:db8::123"): dict(),
                        ipaddress.ip_address("2001:db8::abc"): dict(),
                    },
                    ipaddress.ip_network("2001:db8:1234::/48"): {
                        ipaddress.ip_address("2001:db8:1234::abc:123"): dict(),
                        ipaddress.ip_address("2001:db8:1234::f00:ba"): dict(),
                    },
                    ipaddress.ip_network("2001:db8:abcd::/48"): {
                        ipaddress.ip_address("2001:db8:abcd:abcd::abcd"):
                            dict(),
                        ipaddress.ip_address("2001:db8:abcd:1234:1234::"):
                            dict(),
                    },
                },
                ipaddress.ip_network("fdab:cdef:1234::/48"): {
                    ipaddress.ip_address("fdab:cdef:1234:c001::abcd"): dict(),
                    ipaddress.ip_network("fdab:cdef:1234:5678::/64"): {
                        ipaddress.ip_address("fdab:cdef:1234:5678::1234:5678"):
                            dict(),
                        ipaddress.ip_address("fdab:cdef:1234:5678::abcd:abcd"):
                            dict(),
                    },
                    ipaddress.ip_network("fdab:cdef:1234:abcd::/64"): {
                        ipaddress.ip_address("fdab:cdef:1234:abcd::7654:321"):
                            dict(),
                        ipaddress.ip_address("fdab:cdef:1234:abcd::fe:dcba"):
                            dict(),
                    },
                },
            },
        }

        self.address_spaces = dict()

        for strict in (False, True):
            self.address_spaces[strict] = AddressSpace(strict_=strict)
            for delegated_data in self.delegated_tuples:
                self.address_spaces[strict].describe_new_delegated_network(
                    network_parameter=delegated_data[0],
                    description=delegated_data[1],
                )
            for subnet_data in self.subnet_tuples:
                self.address_spaces[strict].describe(
                    ip_parameter=subnet_data[0],
                    description=subnet_data[1],
                )
            for address_data in self.address_tuples:
                self.address_spaces[strict].describe(
                    ip_parameter=address_data[0],
                    description=address_data[1],
                )

    def test_more_data_export(self):
        pass
        # actual_exported_data = address_space.export_data()
        # self.assertTrue(
        #     actual_exported_data, "should be evaluated as True"
        # )
        # self.assertEquals(
        #     exported["description"],
        #     actual_exported_data["description"],
        #     "exported description data should match",
        # )
