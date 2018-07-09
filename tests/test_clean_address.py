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
        self.assertEqual(
            clean_address(""),
            None,
        )
        self.assertEqual(
            clean_address("address"),
            None,
        )
        self.assertEqual(
            clean_address("192.0.2.256"),
            None,
        )

