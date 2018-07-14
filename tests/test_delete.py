#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests related to delete method in pppipam.AddressSpace."""

import unittest

from pppipam.pppipam import AddressSpace, IPObjectNotInSpaceError


class AddressSpace_delete_TestCase(unittest.TestCase):
    """Tests related to delete method in AddressSpace."""

    def setUp(self):
        self.address_space = AddressSpace(strict_=False)

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

    def test_delete_trying_to_delete_object_not_in_space_error_raise(self):
        """Trying to delete an IP object not in space should raise Error."""
        no_ip_object = False
        try:
            self.address_space.delete(
                ip_parameter="203.0.113.128",
                cascade=True,
            )
        except IPObjectNotInSpaceError:
            no_ip_object = True
        self.assertTrue(
            no_ip_object,
            "Cannot delete IP object without explicit description",
        )

    def test_delete_deleting_object_in_space_returns_true(self):
        """Deleting a described IP object should return True."""
        for parameter_description in (
            ("203.0.113.128", "an IPv4 test net address"),
            ("2001:db8:abcd::/48", "an IPv6 doc subnet"),
            ("123.123.123.123", "123 is nice"),
            ("203.0.113.129", "Second subnet gateway"),
            ("192.0.2.123", "123 is nice, test net"),
            ("2001:db8::abcd:ef12", "ipv6 doc address"),
            ("2000::", "first global address for now"),
            ("fe80::", "even link-local?"),
            ("10.0.0.0/16", "a private IPv4 network"),
            ("203.0.113.128/25", "part of a test net"),
            ("0.0.0.0/0", "whole IPv4 address space as network"),
            ("2001:db8:1234:5678::/64", "a documentation IPv6 network"),
            ("fe80::/64", "IPv6 link-local network"),
            ("fd01:2345:6789::/48", "a ~random~ IPv6 unique-local network"),
            ("::/0", "whole IPv6 address space as network"),
        ):
            with self.subTest(parameter_description=parameter_description):
                self.assertTrue(
                    self.address_space.describe(
                        ip_parameter=parameter_description[0],
                        description=parameter_description[1],
                    )
                )
                self.assertTrue(
                    self.address_space.delete(
                        ip_parameter=parameter_description[0],
                        cascade=True,
                    ),
                    "Deleting a described IP object should return True.",
                )


    def test_delete_after_deleting_object_description_should_be_none(self):
        """Deleting a described IP object should return True."""
        for parameter_description in (
            ("203.0.113.128", "an IPv4 test net address"),
        ):
            with self.subTest(parameter_description=parameter_description):
                self.assertTrue(
                    self.address_space.describe(
                        ip_parameter=parameter_description[0],
                        description=parameter_description[1],
                    )
                )
                self.assertTrue(
                    self.address_space.delete(
                        ip_parameter=parameter_description[0],
                        cascade=True,
                    ),
                    "Deleting a described IP object should return True.",
                )
                self.assertIs(
                    self.address_space.description(parameter_description[0]),
                    None,
                    "No IP object, so description should be None",
                )
