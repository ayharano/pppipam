#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for description methods of pppipam.AddressSpace instances."""

import ipaddress
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

    def test_describe_no_empty_arguments(self):
        """describe method with no empty argument list."""
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
            ("123.123.123.123", "123 is nice"),
            ("203.0.113.129", "Second subnet gateway"),
            ("192.0.2.123", "123 is nice, test net"),
            ("2001:db8::abcd:ef12", "ipv6 doc address"),
            ("2000::", "first global address for now"),
            ("fe80::", "even link-local?"),
        ):
            with self.subTest(parameters=parameters):
                self.assertIs(
                    self.address_space.describe(
                        ip_parameter=parameters[0], description=parameters[1]
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
            ("fd01:2345:6789::/48", "a ~random~ IPv6 unique-local network"),
            ("::/0", "whole IPv6 address space as network"),
        ):
            with self.subTest(parameters=parameters):
                self.assertIs(
                    self.address_space.describe(
                        description=parameters[1], ip_parameter=parameters[0]
                    ),
                    True,
                )

    def test_describe_ip_parameter_not_valid_typeerror(self):
        """Invalid IP parameter should raise TypeError."""
        for invalid_ in (None, 123, set([3, 2, 1])):
            with self.subTest(invalid_=invalid_):
                invalid_ip_parameter = False
                try:
                    self.address_space.describe(
                        description="invalid ip parameter",
                        ip_parameter=invalid_,
                    )
                except TypeError:
                    invalid_ip_parameter = True
                self.assertTrue(
                    invalid_ip_parameter,
                    "Invalid IP parameter should raise TypeError",
                )

    def test_describe_description_not_str_typeerror(self):
        """Non-str description should raise TypeError."""
        for non_str in (None, 123, set([1, 2, 3])):
            with self.subTest(non_str=non_str):
                non_str_description = False
                try:
                    self.address_space.describe(
                        ip_parameter="123.123.123.123", description=non_str
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
                ip_parameter="123.123.123.123", description=""
            )
        except ValueError:
            empty_str_description = True
        self.assertTrue(
            empty_str_description,
            "Empty str description should raise ValueError",
        )

    def test_description_no_empty_arguments(self):
        """description method with no empty argument list."""
        no_empty_arguments = False
        try:
            self.address_space.description()
        except TypeError:
            no_empty_arguments = True
        self.assertTrue(
            no_empty_arguments,
            "Empty arguments should not be accepted in description",
        )

    def test_description_ip_parameter_not_valid_typeerror(self):
        """Invalid IP parameter should raise TypeError."""
        for invalid_ in (None, 123, set([2, 3, 1])):
            with self.subTest(invalid_=invalid_):
                invalid_ip_parameter = False
                try:
                    self.address_space.description(ip_parameter=invalid_)
                except TypeError:
                    invalid_ip_parameter = True
                self.assertTrue(
                    invalid_ip_parameter,
                    "Invalid IP parameter should raise TypeError",
                )

    def test_describe_then_description(self):
        """describe then description of IP object should return same str."""
        for describe_pair in (
            ("203.0.113.128/25", "should be the same"),
            ("2001:db8::2018:7:12", "hey! an IPv6 Address"),
            ("0.0.0.0", "address 0 for ipv4"),
        ):
            with self.subTest(describe_pair=describe_pair):
                self.address_space.describe(
                    description=describe_pair[1], ip_parameter=describe_pair[0]
                )
                self.assertEqual(
                    self.address_space.description(describe_pair[0]),
                    describe_pair[1],
                )

    def test_describe_network_then_empty_address_description(self):
        """describe an IP network and retrieve empty str description of
           an address if it is in network range and
           not explicitly described."""
        for data in (
            ("192.0.2.0/24", "a ipv4 test net", "192.0.2.128"),
            ("192.0.2.0/24", "same net, new address", "192.0.2.192"),
            ("10.0.0.0/8", "a large private net", "10.123.45.67"),
            ("fe80::/64", "link-local net", "fe80::ab:cdef"),
            ("2001:db8:abcd::/48", "ipv6 doc net", "2001:db8:abcd::123"),
            ("abcd::/16", "currently outside global ipv6", "abcd:123::abc"),
        ):
            with self.subTest(data=data):
                self.address_space.describe(
                    ip_parameter=data[0], description=data[1]
                )
                self.assertEqual(
                    self.address_space.description(data[2]), str("")
                )

    def test_describe_network_then_empty_subnet_description(self):
        """describe an IP network and retrieve empty str description of
           an subnet if it is in network range and
           not explicitly described."""
        for data in (
            ("192.0.2.0/24", "a ipv4 test net", "192.0.2.0/25"),
            ("192.0.2.0/24", "same net, new subnet", "192.0.2.128/25"),
            ("10.0.0.0/8", "a large private net", "10.123.0.0/16"),
            ("fe80::/64", "link-local net", "fe80::/126"),
            ("2001:db8:abcd::/48", "ipv6 doc net", "2001:db8:abcd:123::/64"),
            ("abcd::/16", "currently outside global ipv6", "abcd:123::/32"),
        ):
            with self.subTest(data=data):
                self.address_space.describe(
                    ip_parameter=data[0], description=data[1]
                )
                self.assertEqual(
                    self.address_space.description(data[2]), str("")
                )

    def test_valid_address_not_in_any_net_should_return_none(self):
        """description should return None if a valid address is
           not described and not in any network."""
        for existing_net in (
            ipaddress.IPv4Network("192.0.2.0/24"),
            ipaddress.ip_network("203.0.113.0/25"),
            "10.0.0.0/16",
            "fe80::/64",
            ipaddress.ip_network("2001:db8::/48"),
            ipaddress.IPv6Network("0:abcd::/32"),
        ):
            self.address_space.describe(
                description="dull description", ip_parameter=existing_net
            )

        for outside_address in (
            "192.0.3.128",
            ipaddress.ip_address("203.0.113.128"),
            ipaddress.IPv4Address("10.128.0.0"),
            "0.0.0.0",
            ipaddress.ip_address("fe80:123::abcd"),
            ipaddress.IPv6Address("2001:db8:abcd::"),
            "::",
        ):
            with self.subTest(outside_address=outside_address):
                self.assertIs(
                    self.address_space.description(outside_address), None
                )

    def test_valid_networks_not_as_any_subnet_should_return_none(self):
        """description should return None if a valid network is
           not described and not subnet of any network."""
        for existing_net in (
            ipaddress.IPv4Network("192.0.2.0/24"),
            ipaddress.ip_network("203.0.113.0/25"),
            "10.0.0.0/16",
            "fe80::/64",
            ipaddress.ip_network("2001:db8::/48"),
            ipaddress.IPv6Network("0:abcd::/32"),
        ):
            self.address_space.describe(
                description="dull description", ip_parameter=existing_net
            )

        for outside_network in (
            "192.0.3.128/25",
            ipaddress.ip_network("203.0.113.128/26"),
            ipaddress.IPv4Network("10.128.0.0/9"),
            "0.0.0.0/0",
            ipaddress.ip_network("fe80:123::/32"),
            ipaddress.IPv6Network("2001:db8:abcd::/48"),
            "::/0",
        ):
            with self.subTest(outside_network=outside_network):
                self.assertIs(
                    self.address_space.description(outside_network), None
                )
