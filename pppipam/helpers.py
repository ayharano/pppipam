#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress
import typing


IPAddress = typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
IPAddressParameter = typing.Union[str, IPAddress]


def clean_address(
    address_parameter: IPAddressParameter
) -> typing.Optional[IPAddress]:
    """Process given parameter as an Address instance.

    If parameter results into a valid IPv4 or IPv6 address,
    it respectively returns IPv4Address or IPv6Address.
    Otherwise, returns None.

    >>> clean_address('invalid address')
    >>> clean_address('203.0.113.123')
    IPv4Address('203.0.113.123')
    >>> clean_address('::abcd:1234')
    IPv6Address('::abcd:1234')

    Args:
        address_parameter: value to be processed as an IP address.

    Returns:
        IPv4Address instance, IPv6Address instance or None.
    """
    value = None
    try:
        value = ipaddress.ip_address(address_parameter)
    except (ipaddress.AddressValueError, ValueError):
        pass
    return value


def clean_network(network_parameter):
    return ipaddress.IPv4Network(network_parameter)
    if network_parameter == "192.0.2.0/24":
        return ipaddress.IPv4Network("192.0.2.0/24")
    if network_parameter == "0.0.0.0/0":
        return ipaddress.IPv4Network("0.0.0.0/0")
    return ipaddress.IPv4Network("10.0.0.0/16")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
