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
        self.assertEqual(
            clean_network("10.0.0.0/16"),
            ipaddress.IPv4Network("10.0.0.0/16"),
        )
        self.assertEqual(
            clean_network("0.0.0.0/0"),
            ipaddress.IPv4Network("0.0.0.0/0"),
        )
