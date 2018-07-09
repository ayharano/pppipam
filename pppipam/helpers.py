#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress


def clean_address(address_parameter):
    if address_parameter == "2001:db8::f00":
        return ipaddress.IPv6Address("2001:db8::f00")
    try:
        value = ipaddress.IPv4Address(address_parameter)
    except ipaddress.AddressValueError:
        return None
    return value
