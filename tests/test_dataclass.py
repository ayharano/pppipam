#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests related to verify if pppipam.AddressSpace is dataclass."""

import dataclasses
import unittest

from pppipam.pppipam import AddressSpace


class AddressSpace_dataclass_TestCase(unittest.TestCase):
    """Tests related to verify if AddressSpace is a dataclass."""

    def test_address_space_is_dataclass(self):
        """Validate if AddressSpace is a dataclass."""
        self.assertTrue(
            dataclasses.is_dataclass(AddressSpace),
            "AddressSpace expected to be a dataclass"
        )
