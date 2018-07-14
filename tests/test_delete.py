#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests related to delete method in pppipam.AddressSpace."""

import unittest

from pppipam.pppipam import AddressSpace, IPObjectNotInSpaceError


class AddressSpace_delete_TestCase(unittest.TestCase):
    """Tests related to delete method in AddressSpace."""

    def setUp(self):
        self.address_space = AddressSpace()

    def test_delete_no_empty_arguments(self):
        """delete method with no empty argument list."""
        no_empty_arguments = False
        try:
            self.address_space.delete()
        except TypeError:
            no_empty_arguments = True
        self.assertTrue(
            no_empty_arguments,
            "Empty arguments should not be accepted in delete",
        )

    def test_delete_keyword_only_no_positional_arguments(self):
        """delete method as keyword only, without positional parameters."""
        no_positional_arguments = False
        try:
            self.address_space.delete("203.0.113.128", True)
        except TypeError:
            no_positional_arguments = True
        self.assertTrue(
            no_positional_arguments,
            "No positional argument should be accepted in delete",
        )
