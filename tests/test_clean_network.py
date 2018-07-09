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
        self.assertEqual(
            clean_network(""),
            None,
        )
