#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for functions from helpers module of `pppipam` package."""

import ipaddress
import unittest

from pppipam.helpers import clean_address, clean_network


class clean_address_TestCase(unittest.TestCase):
    """Tests for clean_address."""

    def test_clean_address_valid_ipv4_address_as_str(self):
        """Test for valid IPv4 Addresses correctly instantiated from str."""
        for ipv4_str in ("192.0.2.1", "203.0.113.128", "198.51.100.255"):
            with self.subTest(ipv4_str=ipv4_str):
                self.assertEqual(
                    clean_address(ipv4_str),
                    ipaddress.IPv4Address(ipv4_str),
                )

    def test_clean_address_valid_ipv6_address_as_str(self):
        """Test for valid IPv6 Addresses correctly instantiated from str."""
        for ipv6_str in (
            "2001:db8::f00",
            "2001:db8:0123:4567:89ab::",
            "::",
        ):
            with self.subTest(ipv6_str=ipv6_str):
                self.assertEqual(
                    clean_address(ipv6_str),
                    ipaddress.IPv6Address(ipv6_str),
                )

    def test_clean_address_invalid_ip_address_as_str(self):
        """Test for invalid IP Addresses from str to None."""
        for invalid_str in (
            "",
            "address",
            "20018:db8::",
            "192.0.2.256",
            "192.0.2.0/24",
            "2001:db8::/32",
        ):
            with self.subTest(invalid_str=invalid_str):
                self.assertEqual(
                    clean_address(invalid_str),
                    None,
                )

    def test_clean_address_valid_ipv4_address_as_instances(self):
        """Test for valid IPv4 Addresses instantiated from IPv4Address."""
        for ipv4_str in ("192.0.2.1", "203.0.113.128", "198.51.100.255"):
            with self.subTest(ipv4_str=ipv4_str):
                self.assertEqual(
                    clean_address(ipaddress.IPv4Address(ipv4_str)),
                    ipaddress.IPv4Address(ipv4_str),
                )

    def test_clean_address_valid_ipv6_address_as_instances(self):
        """Test for valid IPv6 Addresses instantiated from IPv6Address."""
        for ipv6_str in (
            "2001:db8::f00",
            "2001:db8:0123:4567:89ab::",
            "::",
        ):
            with self.subTest(ipv6_str=ipv6_str):
                self.assertEqual(
                    clean_address(ipaddress.IPv6Address(ipv6_str)),
                    ipaddress.IPv6Address(ipv6_str),
                )


class clean_network_TestCase(unittest.TestCase):
    """Tests for clean_network."""

    def test_clean_network_valid_ipv4_network_as_str(self):
        """Test for valid IPv4 Network correctly instantiated from str."""
        for ipv4_str in ("10.0.0.0/16", "0.0.0.0/0", "192.0.2.0/24"):
            with self.subTest(ipv4_str=ipv4_str):
                self.assertEqual(
                    clean_network(ipv4_str),
                    ipaddress.IPv4Network(ipv4_str),
                )

    def test_clean_network_valid_ipv6_network_as_str(self):
        """Test for valid IPv6 Network correctly instantiated from str."""
        for ipv6_str in ("::/0", "2001:db8::/32", "fedc:ba98:7654:3210::/64"):
            with self.subTest(ipv6_str=ipv6_str):
                self.assertEqual(
                    clean_network(ipv6_str),
                    ipaddress.IPv6Network(ipv6_str),
                )

    def test_clean_network_invalid_ip_network_as_str(self):
        """Test for invalid IP Networks from str to None."""
        for invalid_str in (
            "",
            "address",
            "192.0.2.256",
            "20018:db8::",
        ):
            with self.subTest(invalid_str=invalid_str):
                self.assertEqual(
                    clean_network(invalid_str),
                    None,
                )

    def test_clean_network_valid_ipv4_network_as_instances(self):
        """Test for valid IPv4 Networks instantiated from IPv4Network."""
        for ipv4_str in ("10.0.0.0/16", "0.0.0.0/0", "192.0.2.0/24"):
            with self.subTest(ipv4_str=ipv4_str):
                self.assertEqual(
                    clean_network(ipaddress.IPv4Network(ipv4_str)),
                    ipaddress.IPv4Network(ipv4_str),
                )

    def test_clean_network_valid_ipv6_network_as_instances(self):
        """Test for valid IPv6 Networks instantiated from IPv6Network."""
        for ipv6_str in ("::/0", "2001:db8::/32", "fedc:ba98:7654:3210::/64"):
            with self.subTest(ipv6_str=ipv6_str):
                self.assertEqual(
                    clean_network(ipaddress.IPv6Network(ipv6_str)),
                    ipaddress.IPv6Network(ipv6_str),
                )
