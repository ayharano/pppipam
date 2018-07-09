#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for clean_address function of `pppipam` package."""

import ipaddress
import unittest

from pppipam.helpers import clean_address


class clean_address_TestCase(unittest.TestCase):
    """Tests for clean_address."""

    def test_clean_address_valid_ipv4_address(self):
        """Test for valid IPv4 Addresses correctly instantiated."""
        self.assertEqual(
            clean_address("192.0.2.1"),
            ipaddress.IPv4Addres("192.0.2.1"),
        )
