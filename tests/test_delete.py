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
        """Description of a deleted IP object should return None
           if no other IP object."""
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
                self.assertIs(
                    self.address_space.description(parameter_description[0]),
                    None,
                    "No IP object, so description should be None",
                )


class AddressSpace_more_data_delete_TestCase(unittest.TestCase):
    """Actual-like data to delete AddressSpace data."""

    def setUp(self):
        """Export AddressSpace's data."""
        self.delegated_tuples = (
            ("2001:db8::/32", "IPv6 documentation network space"),
            ("203.0.113.0/24", "one of IPv4 test net"),
            ("fdab:cdef:1234::/48", "an IPv6 unique-local net"),
            ("192.0.2.0/24", "another IPv4 test net"),
        )
        self.subnet_tuples = (
            ("2001:db8::/48", "zeroed doc subnet"),
            ("2001:db8:1234::/48", "digit doc subnet"),
            ("2001:db8:abcd::/48", "letter doc subnet"),
            ("203.0.113.0/26", "a 1/4 test subnet"),
            ("203.0.113.128/27", "1/8 subnet"),
            ("fdab:cdef:1234:5678::/64", "digit unique local subnet"),
            ("fdab:cdef:1234:abcd::/64", "letter unique local subnet"),
            ("192.0.2.64/26", "another 1/4 test subnet"),
            ("192.0.2.128/25", "1/2 of a test subnet"),
        )
        self.address_tuples = (
            ("2001:db8:9876:5432:10::", "direct IPv6 doc address"),
            ("203.0.113.200", "direct address of a IPv4 test net"),
            ("fdab:cdef:1234:c001::abcd", "direct IPv6 unique-local address"),
            ("192.0.2.12", "direct address of another IPv4 test net"),
            ("2001:db8::123", "digit address of zeroed doc subnet"),
            ("2001:db8::abc", "letter address of zeroed doc subnet"),
            ("2001:db8:1234::abc:123", "mixed address of digit doc subnet"),
            ("2001:db8:1234::f00:ba", "letter address of digit doc subnet"),
            ("2001:db8:abcd:abcd::abcd", "abcd address of letter doc subnet"),
            ("2001:db8:abcd:1234:1234::", "1234 address of letter doc subnet"),
            ("203.0.113.0", "first address of a 1/4 test subnet"),
            ("203.0.113.63", "last address of a 1/4 test subnet"),
            ("203.0.113.130", " almost at begining of 1/8 subnet"),
            ("203.0.113.150", " almost at the end of 1/8 subnet"),
            ("fdab:cdef:1234:5678::1234:5678", "12345678 address"),
            ("fdab:cdef:1234:5678::abcd:abcd", "abcdabcd address"),
            ("fdab:cdef:1234:abcd::7654:321", "reverse number address"),
            ("fdab:cdef:1234:abcd::fe:dcba", "reverse letter address"),
            ("192.0.2.64", "first of another 1/4 test subnet"),
            ("192.0.2.127", "last of another 1/4 test subnet"),
            ("192.0.2.200", "200 of 1/2 of a test subnet"),
            ("192.0.2.234", "234 of 1/2 of a test subnet"),
        )

        self.address_spaces = dict()

        for strict in (False, True):
            self.address_spaces[strict] = AddressSpace(strict_=strict)
            for delegated_data in self.delegated_tuples:
                self.address_spaces[strict].describe_new_delegated_network(
                    network_parameter=delegated_data[0],
                    description=delegated_data[1],
                )
            for subnet_data in self.subnet_tuples:
                self.address_spaces[strict].describe(
                    ip_parameter=subnet_data[0],
                    description=subnet_data[1],
                )
            for address_data in self.address_tuples:
                self.address_spaces[strict].describe(
                    ip_parameter=address_data[0],
                    description=address_data[1],
                )

    def test_address_space_delete_for_more_data_instance(self):
        pass
