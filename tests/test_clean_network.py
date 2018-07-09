#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for clean_network function of `pppipam` package."""

import ipaddress
import unittest

from pppipam.helpers import clean_network


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

    def test_clean_network_invalid_ipv4_network_as_str(self):
        """Test for invalid IPv4 Networks from str to None."""
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

    def test_clean_network_valid_ipv6_network_as_str(self):
        """Test for valid IPv6 Network correctly instantiated from str."""
        for ipv6_str in ("::/0", "2001:db8::/32", "fedc:ba98:7654:3210::/64"):
            with self.subTest(ipv6_str=ipv6_str):
                self.assertEqual(
                    clean_network(ipv6_str),
                    ipaddress.IPv6Network(ipv6_str),
                )

    def test_clean_network_invalid_ipv6_network_as_str(self):
        """Test for invalid IPv6 Networks from str to None."""
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
