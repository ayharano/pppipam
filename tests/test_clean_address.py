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
        self.assertEqual(
            clean_address("192.0.2.1"),
            ipaddress.IPv4Address("192.0.2.1"),
        )
        self.assertEqual(
            clean_address("203.0.113.128"),
            ipaddress.IPv4Address("203.0.113.128"),
        )
