#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for clean_address function of `pppipam` package."""

import ipaddress
import unittest

from pppipam.helpers import clean_address


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

    def test_clean_address_invalid_ipv4_address_as_str(self):
        """Test for invalid IPv4 Addresses from str to None."""
        for invalid_str in (
            "",
            "address",
            "192.0.2.256",
            "192.0.2.0/24",
            "2001:db8::",
            "2001:db8::/32",
        ):
            with self.subTest(invalid_str=invalid_str):
                self.assertEqual(
                    clean_address(invalid_str),
                    None,
                )

    def test_clean_address_valid_ipv6_address_as_str(self):
        """Test for valid IPv6 Addresses correctly instantiated from str."""
        self.assertEqual(
            clean_address("2001:db8::f00"),
            ipaddress.IPv6Address("2001:db8::f00"),
        )
