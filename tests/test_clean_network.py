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
            "2001:db8::/32",
        ):
            with self.subTest(invalid_str=invalid_str):
                self.assertEqual(
                    clean_network(invalid_str),
                    None,
                )

    def test_clean_network_valid_ipv6_network_as_str(self):
        """Test for valid IPv6 Network correctly instantiated from str."""
        self.assertEqual(
            clean_network("::/0"),
            ipaddress.IPv6Network("::/0"),
        )
        self.assertEqual(
            clean_network("2001:db8::/32"),
            ipaddress.IPv6Network("2001:db8::/32"),
        )
