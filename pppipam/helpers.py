#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress


def clean_address(address_parameter):
    """Process given parameter as an Address instance.

    If parameter results into a valid IPv4 or IPv6 address,
    it respectively returns IPv4Address or IPv6Address.
    Otherwise, returns None.

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
